'''
Author: SmallDragon Chen
City:   New Taipei
Url:    http://data.ntpc.gov.tw
'''
import requests
from bs4 import BeautifulSoup
import json

import lib
from thread_pool import Pool

def load():
    global fields, data
    res = requests.get('http://data.ntpc.gov.tw/api/v1/rest/dataset?limit=3000')
    id_list = json.loads(res.text)

    url = 'http://data.ntpc.gov.tw/api/v1/rest/dataset/' + id_list[0]
    print(url)
    res = requests.get(url)
    res = json.loads(res.text)
    # print(res)
    print(res.keys())


def process():
    global data
    temp_list = []
    for row in data:
        temp = {}
        temp["編號"] = row["編號"]
        temp["資料來源(部會單位)"] = row["資料集提供機關"]
        temp["第一層級"] = "台北市政府"
        temp["資料集名稱"] = row["資料名稱"]
        temp["資料量"] = row["資料量"]
        temp["下載次數"] = ""
        temp["主要欄位"] = row["主要欄位說明"]
        temp_list.append(temp)

    data = temp_list

if __name__ == '__main__':
    list_url = 'https://beta.data.taipei/api/dataset/downloadList?format=csv'
    f_name = '02_newtaipei'

    # ===== Download or Load data =====
    load()

    # ===== process =====
    # process()

    # ===== save =====
    # lib.saveCSV(f_name, data)
    # lib.saveJSON(f_name, data)
