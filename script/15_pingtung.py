'''
Author: SmallDragon Chen
City:   Pingtung
Url:    https://www.pthg.gov.tw/Cus_OpenData_Default.aspx?n=481C53E05C1D2D97
'''
import requests
from bs4 import BeautifulSoup
import json

import lib
from thread_pool import Pool

def load(list_url):
    global id_list
    res = requests.get(list_url)
    id_list = json.loads(res.text)['result']

def getEach(i, id):
    try:
        url = 'http://opendata.penghu.gov.tw/api/3/action/package_show?id=' + id
        res = requests.get(url)
        res = json.loads(res.text)['result']

        temp = {}
        temp['編號'] = i + 1
        temp['資料集名稱'] = res['title']
        for each in res['extras']:
            key = each['key']
            value = each['value']
            if key == '主要欄位說明':
                temp['主要欄位'] = value
            elif key == '資料量':
                temp['資料量'] = value
            elif key == '資料集提供機關名稱':
                temp['資料來源(部會單位)'] = value

        print(temp['編號'], temp['資料集名稱'])
    except:
        temp = {}
        temp['編號'] = i + 1
        temp['資料集名稱'] = 'error'
        temp['資料來源(部會單位)'] = id

    return temp
def getAll():
    global data

    pool = Pool(size=10)
    pool.add_tasks([ ( getEach, (i, id,))  for i, id in enumerate(id_list)])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

    print('Error: ', len(list(pool.error_queue.queue)))

if __name__ == '__main__':
    list_url = 'http://opendata.penghu.gov.tw/api/3/action/package_list'
    f_name = '13_penghu'

    # ===== Download or Load data =====
    load(list_url)

    # ===== process =====
    getAll()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
