'''
Author: SmallDragon Chen
City:   Chiayi
Url:    http://data.nantou.gov.tw/
'''
import requests
from bs4 import BeautifulSoup
import json, csv

import lib
from thread_pool import Pool

def loadAndGet():
    global data

    temp_list = []
    i = 1
    offset = 0
    while True:
        print(offset)
        res = requests.get('http://data.chiayi.gov.tw/opendata/api/datasetQuery?offset={}'.format(offset))
        res = json.loads(res.text)

        for each in res['datasets']:
            print(i, each['title'])
            temp = {}
            temp['編號'] = i
            temp['資料集名稱'] = each['title']
            temp['主要欄位'] = each['fieldDescription']
            temp['資料來源(部會單位)'] = each['publisher']
            temp['第一層級'] = '嘉義市政府'
            temp['資料量'] = each['numberOfData']
            temp_list.append(temp)

            i += 1
        if len(res['datasets']) != 100:
            break
        offset += 100

    data = temp_list

if __name__ == '__main__':
    f_name = '12_chiayi'

    # ===== Load and Get data =====
    loadAndGet()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
