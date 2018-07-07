import requests
from bs4 import BeautifulSoup
import json, csv

def saveJSON(f_name, data):
    dir = f'../out/json/{f_name}.json'
    with open(dir, 'w') as json_f:
        json_f.write(json.dumps(data, ensure_ascii=False))

def saveCSV(f_name, data):
    dir = f'../out/csv/{f_name}.csv'
    fields = ['編號','資料集名稱','資料來源(部會單位)','第一層級','第二層級','第三層級','資料量','下載次數','瀏覽次數','主要欄位','最後更新時間']
    with open(dir, 'w') as csv_f:
        writer = csv.DictWriter(csv_f, fields)
        writer.writeheader()
        writer.writerows(data)
