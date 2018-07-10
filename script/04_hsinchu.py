'''
Author: SmallDragon Chen
City:   Hsinchu
Url:    http://opendata.hccg.gov.tw/
'''
import requests
from bs4 import BeautifulSoup
import json

import lib
from thread_pool import Pool

def load():
    global id_list
    url = 'http://opendata.hccg.gov.tw/api/3/action/package_list?limit=500&offset=0'
    res = requests.get(url)
    id_list = json.loads(res.text)['result']
    # print(id_list[0:10])

def getEach(i, id):
    url = 'http://opendata.hccg.gov.tw/api/3/action/package_show?id=' + id
    res = requests.get(url)
    res = json.loads(res.text)['result']

    temp = {}

    for each in res['extras']:
        key = each['key']

        if key == '資料集提供機關名稱':
            temp["資料來源(部會單位)"] = each['value']
        elif key == '資料量':
            temp["資料量"] = each['value']

    temp['資料集名稱'] = res['title']
    temp['主要欄位'] = res['resources'][0]['description']
    temp['編號'] = i + 1

    print(i, temp['資料集名稱'], 'finish')

    return temp
def getAll():
    global data

    pool = Pool(size=5)
    pool.add_tasks([ ( getEach, (i, id,))  for i, id in enumerate(id_list)])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

def process():
    global data, id_list
    temp_list = []
    for temp in data:
        temp['第一層級'] = '新竹市政府'

        temp_list.append(temp)

    data = temp_list

if __name__ == '__main__':
    f_name = '04_hsinchu'

    # ===== Download or Load data =====
    load()

    # ===== process =====
    getAll()
    process()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
