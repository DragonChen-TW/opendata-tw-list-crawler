'''
Author: SmallDragon Chen
City:   Yaoyuan
Url:    https://data.tycg.gov.tw/
'''
import requests
from bs4 import BeautifulSoup
import csv

import lib
from thread_pool import Pool

def downloadList(list_url, f_name):
    res = requests.get(list_url)
    temp = res.content
    with open(f'../out/raw/{f_name}.csv', 'wb') as csv_f:
        csv_f.write(temp)

def load():
    global data
    temp = []
    with open(f'../out/raw/{f_name}.csv') as csv_f:
        reader = csv.DictReader(csv_f)
        data = [line for line in reader]

def getCount(row):
    url = row['資料連結網址']

    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    tr_list = soup.find_all('tr')

    v_count = tr_list[5].find_all('td')[1].string.replace(' ','').replace('\n','')
    d_count = tr_list[6].find_all('td')[1].string.replace(' ','').replace('\n','')

    print(row['編號'], row['資料名稱'][0:15], v_count, d_count)
    row['下載次數'] = d_count
    row['瀏覽次數'] = v_count
    return (row)
def returnTemp(d):
    d['編號'] = int(d['編號'])
    return d
def getAllCount():
    global data

    pool = Pool(size=10)
    pool.add_tasks([ ( getCount, (row,))  for row in data])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list = [returnTemp(each) for each in temp_list]
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

def process():
    global data
    temp_list = []
    for row in data:
        temp = {}
        temp["編號"] = row["編號"]
        temp_str = row["資料來源"]
        temp_str = temp_str[temp_str.find('【') + 1:temp_str.find('】')]
        temp["資料來源(部會單位)"] = temp_str

        temp['第一層級'] = '桃園市政府'
        temp["資料集名稱"] = row["資料名稱"]
        temp["資料量"] = ""
        temp["主要欄位"] = row["主要欄位"].replace('\n','')
        # ---
        print(temp["編號"], temp['資料集名稱'])

        temp["下載次數"] = row["下載次數"]
        temp["瀏覽次數"] = row["瀏覽次數"]

        temp_list.append(temp)
    data = temp_list

if __name__ == '__main__':
    list_url = 'https://data.tycg.gov.tw/opendata/rule/downloadList?output=csv'
    f_name = '03_taoyuan'

    # ===== Download ot Load data =====
    # downloadList(list_url, f_name)
    load()

    # ===== process =====
    getAllCount()
    process()

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
