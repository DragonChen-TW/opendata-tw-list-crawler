'''
Author: SmallDragon Chen
City:   Taichung
Url:    http://opendata.taichung.gov.tw
'''
import requests
from bs4 import BeautifulSoup
import json, csv

import lib
from thread_pool import Pool

def downloadList(list_url, f_name):
    res = requests.get(list_url)
    temp = res.content
    with open(f'../out/raw/{f_name}.csv', 'wb') as csv_f:
        csv_f.write(temp)

def load():
    global data
    with open(f'../out/raw/{f_name}.csv') as csv_f:
        reader = csv.DictReader(csv_f)
        data = [line for line in reader]

def getEach(row):
    url = row['資料集連結網址']
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    row['編號'] = int(row['\ufeff編號'])

    # soup
    dl = soup.find('aside')
    dd = dl.find_all('dd')
    row['瀏覽次數'] = dd[0].text
    row['下載次數'] = dd[2].text

    # choose that row in table where last-update at
    tr = soup.select('tbody > tr')[1]
    if tr.find('th').text == '最後更新':
        row['最後更新時間'] = tr.find('span').text.replace('\n', '').replace(' ', '')

    print(row['編號'], row['資料集名稱'][0:15], row['最後更新時間'])

    return row
def getAll():
    global data

    pool = Pool(size=10)
    pool.add_tasks([ ( getEach, (row,))  for row in data])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

def process():
    global data

    print(data[0].keys())

    temp_list = []
    for row in data:
        temp = {}
        temp['編號'] = row['編號']
        temp['資料集名稱'] = row['資料集名稱']
        temp['主要欄位'] = row['主要欄位說明']

        temp['第一層級'] = '台中市政府'
        temp['資料量'] = row['資料量']
        temp['資料來源(部會單位)'] = row['資料集提供機關']

        temp['瀏覽次數'] = row['瀏覽次數']
        temp['下載次數'] = row['下載次數']
        temp['最後更新時間'] = row['最後更新時間']

        temp_list.append(temp)
    data = temp_list

if __name__ == '__main__':
    list_url = 'http://opendata.taichung.gov.tw/dataset/download_all'
    f_name = '08_taichung'

    # ===== Download or Load data =====
    # downloadList(list_url, f_name)
    load()

    # ===== process =====
    getAll()
    process()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
