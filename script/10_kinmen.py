'''
Author: SmallDragon Chen
City:   Kinmen
Url:    http://data.kinmen.gov.tw/
'''
import requests
from bs4 import BeautifulSoup
import json

import lib
from thread_pool import Pool

def load(list_url):
    global link_list
    res = requests.get(list_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    link_list = soup.find(class_='newlist').findAll('tr')
    link_list = ['http://data.kinmen.gov.tw' + link.find('a')['href'] for link in link_list]

def getEach(i, url):
    temp = {}
    temp['編號'] = i + 1
    temp['第一層級'] = '金門縣政府'

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    rows = soup.find(class_='contentword').findAll('tr')

    for row in rows:
        try:
            key = row.find('th').text
            value = row.find('td').text.replace('\n','').replace('\r','')

            if key == '資料集名稱':
                temp['資料集名稱'] = value
            elif key == '資料提供機關':
                temp['資料來源(部會單位)'] = value
            elif key == '主要欄位說明':
                temp['主要欄位'] = value
        except:
            pass

    print(temp['編號'], temp['資料集名稱'])
    # except:
    #     temp['資料集名稱'] = 'error'
    #     temp['資料來源(部會單位)'] = url

    return temp
def getAll():
    global data

    pool = Pool(size=10)
    pool.add_tasks([ ( getEach, (i, url,))  for i, url in enumerate(link_list)])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

    print(len(list(pool.error_queue.queue)))

if __name__ == '__main__':
    list_url = 'http://data.kinmen.gov.tw/od/last'
    f_name = '10_kinmen'

    # ===== Download or Load data =====
    load(list_url)

    # ===== process =====
    getAll()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
