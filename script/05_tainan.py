'''
Author: SmallDragon Chen
City:   Tainan
Url:    http://data.tainan.gov.tw/
'''
import requests
from bs4 import BeautifulSoup
import json

import lib
from thread_pool import Pool

def load():
    global id_list
    url = 'http://data.tainan.gov.tw/api/3/action/package_list?limit=1000&offset=0'
    res = requests.get(url)
    id_list = json.loads(res.text)['result']
    # print(id_list[0:10])

def getEach(i, id):
    url = 'http://data.tainan.gov.tw/api/3/action/package_show?id=' + id
    res = requests.get(url)
    res = json.loads(res.text)['result']

    temp = {}
    temp['編號'] = i + 1
    temp['資料集名稱'] = res['title']
    temp['資料來源(部會單位)'] = res['organization']['title']
    temp['資料量'] = res['num_resources']
    temp['瀏覽次數'] = res['tracking_summary']['total']
    try:
        temp['主要欄位'] = res['resources'][0]['description'].replace('\r\n',' ').replace(' ',' ')
    except:
        pass

    down_count = 0
    for each in res['resources']:
        down_count += each['tracking_summary']['total']
    temp['下載次數'] = down_count

    print(i, temp['資料集名稱'], 'finish')

    return temp
def getAll():
    global data

    pool = Pool(size=10)
    pool.add_tasks([ ( getEach, (i, id,))  for i, id in enumerate(id_list)])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

def process():
    global data
    temp_list = []
    for temp in data:
        temp['第一層級'] = '台南市政府'

        temp_list.append(temp)
    data = temp_list

if __name__ == '__main__':
    f_name = '05_tainan'

    # ===== Download or Load data =====
    load()

    # ===== process =====
    getAll()
    process()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
