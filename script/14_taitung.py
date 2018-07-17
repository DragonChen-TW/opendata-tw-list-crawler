'''
Author: SmallDragon Chen
City:   Taitung
Url:    http://www.taitung.gov.tw/opendata/
'''
import requests
from bs4 import BeautifulSoup
import json

import lib
from thread_pool import Pool

def load():
    global temp_list

    with open('../out/raw/14_taitung.html') as html_f:
        soup = BeautifulSoup(html_f.read(),'html.parser')
        lis = soup.select('ol > li')

        temp_list = []
        for each in lis:
            temp = {}
            temp['id'] = each.find('a')['href']
            temp['資料集名稱'] = each.find('h4').text
            temp['最後更新時間'] = each.find('span').text[27:36]
            temp['下載次數'] = each.find(class_='case').find('span').text
            temp_list.append(temp)

def delSpace(string):
    return string.replace('\r','').replace('\n','').replace(' ','')
def getEach(i, temp):
    id = temp['id']
    url = 'http://www.taitung.gov.tw/opendata/' + id
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        trs = soup.find(class_='page_directory').find_all('tr')

        temp['編號'] = i + 1
        temp['資料來源(部會單位)'] = delSpace(trs[8].find('td').text)
        temp['資料量'] = delSpace(trs[7].select('td:nth-of-type(2)')[0].text)
        temp['主要欄位'] = delSpace(trs[4].find('td').text)
        temp['第一層級'] = '臺東縣政府'
        del(temp['id'])
    except:
        temp['編號'] = i + 1
        temp['資料集名稱'] = 'error'
        temp['資料來源(部會單位)'] = temp['id']
        del(temp['id'])

    print(temp['編號'], temp['資料集名稱'])
    return temp
def getAll():
    global data, temp_list

    pool = Pool(size=10)
    pool.add_tasks([ ( getEach, (i, temp, ))  for i, temp in enumerate(temp_list[0:500])])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

    print('Error: ', len(list(pool.error_queue.queue)))

if __name__ == '__main__':
    list_url = 'http://opendata.penghu.gov.tw/api/3/action/package_list'
    f_name = '14_taitung'

    # ===== Download or Load data =====
    load()

    # ===== process =====
    # print([getEach(i, id_list[i]) for i in range(len(id_list[0:10]))])
    getAll()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
