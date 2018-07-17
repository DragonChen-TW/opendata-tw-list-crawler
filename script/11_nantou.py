'''
Author: SmallDragon Chen
City:   Nantou
Url:    http://data.nantou.gov.tw/
'''
import requests
from bs4 import BeautifulSoup
import json, csv

import lib
from thread_pool import Pool

def load(list_url):
    global id_list
    res = requests.get(list_url)
    id_list = json.loads(res.text)['result']

def getEach(i, id):
    url = 'http://data.nantou.gov.tw/api/3/action/package_show?id=' + id
    res = requests.get(url)
    res = json.loads(res.text)['result']

    temp = {}
    temp['編號'] = i + 1

    temp['資料集名稱'] = res['title']
    temp['資料來源(部會單位)'] = res['organization']['title']

    temp['最後更新時間'] = res['metadata_modified']
    temp['資料量'] = res['num_resources']

    print(i, temp['資料集名稱'])
    return temp
def getAll():
    global data

    pool = Pool(size=10)
    pool.add_tasks([ ( getEach, (i, id,))  for i, id in enumerate(id_list)])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

    print(len(list(pool.error_queue.queue)))

if __name__ == '__main__':
    list_url = 'http://data.nantou.gov.tw/api/3/action/package_list?limit=500&offset=0'
    f_name = '11_nantou'

    # ===== Download or Load data =====
    load(list_url)

    # ===== process =====
    getAll()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
