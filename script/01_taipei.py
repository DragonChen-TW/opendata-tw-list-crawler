'''
Author: SmallDragon Chen
City:   Taipei
Url:    http://data.taipei
'''
import requests
from bs4 import BeautifulSoup
import csv

import lib

def downloadList(list_url, f_name):
    res = requests.get(list_url)
    temp = res.content
    with open(f'../out/raw/{f_name}.csv', 'wb') as csv_f:
        csv_f.write(temp)

def load():
    global fields, data
    temp = []
    with open(f'../out/raw/{f_name}.csv', encoding='big5', errors='ignore') as csv_f:
        reader = csv.DictReader(csv_f)
        fields = reader.fieldnames
        data = [line for line in reader]

def process():
    global data, fields
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
    f_name = '01_taipei'

    # ===== Download or Load data =====
    # downloadList(list_url, f_name)
    load()

    # ===== process =====
    process()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
