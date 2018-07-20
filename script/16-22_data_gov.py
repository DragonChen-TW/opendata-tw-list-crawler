'''
Author: SmallDragon Chen
City:   data.gov datasets
Url:    https://data.gov.tw
'''
import requests
from bs4 import BeautifulSoup
import csv

import lib

def downloadList(list_url, download_url, f_name):
    res = requests.get(list_url)
    temp = res.content
    with open(f'../out/raw/{f_name}_list.csv', 'wb') as csv_f:
        csv_f.write(temp)
    with open(f'../out/raw/{f_name}_list.csv') as csv_f:
        temp = csv_f.read()
    with open(f'../out/raw/{f_name}_list.csv', 'w') as csv_f:
        csv_f.write(temp.replace('\x00', ''))

    res = requests.get(download_url)
    temp = res.content
    with open(f'../out/raw/{f_name}_download.csv', 'wb') as csv_f:
        csv_f.write(temp)
def combineCSV(f_name):
    with open(f'../out/raw/{f_name}_list.csv') as csv_f:
        reader = csv.DictReader(csv_f)
        all_list = [line for line in reader]
    with open(f'../out/raw/{f_name}_download.csv') as csv_f:
        reader = csv.DictReader(csv_f)
        down_list = [line for line in reader]

    count = 0
    new_list = []
    for data in all_list:
        for i in range(len(down_list)):
            if data['資料集名稱'] == down_list[i]['資料集名稱']:
                data.update(down_list[i])
                count += 1
                down_list.pop(i)
                break

    with open(f'../out/raw/{f_name}_mix.csv', 'w') as csv_f:
        writer = csv.DictWriter(csv_f, all_list[0].keys())
        writer.writeheader()
        writer.writerows(all_list)

def load():
    global data
    temp = []
    with open(f'../out/raw/{f_name}_mix.csv') as csv_f:
        reader = csv.DictReader(csv_f)
        data = [line for line in reader]

def process():
    global data, org_data
    temp_list = []
    for row in data:
        temp = {}
        temp["資料來源(部會單位)"] = row["提供機關"]
        temp["資料集名稱"] = row["資料集名稱"]
        temp["下載次數"] = row['下載次數'].replace(',','')
        temp["瀏覽次數"] = row['瀏覽人次'].replace(',','')
        temp["主要欄位"] = row["主要欄位說明"]
        temp_list.append(temp)

    data = temp_list

    count = [1, 1, 1, 1, 1, 1, 1, 1]
    org_name = ['屏東','基隆','苗栗','彰化','雲林','嘉義','花蓮','連江']
    org_gov_name = ['屏東縣政府', '基隆市政府', '苗栗縣政府', '彰化縣政府', '雲林縣政府', '嘉義縣政府', '花蓮縣政府', '連江縣政府']
    temp = {org:[] for org in org_name}
    for row in data:
        for i, org in enumerate(org_name):
            if org in row['資料來源(部會單位)']:
                row['編號'] = count[i]
                count[i] += 1
                row['第一層級'] = org_gov_name[i]

                temp[org].append(row)

                break
    org_data = temp

    for t in temp:
        print(t, len(temp[t]))

if __name__ == '__main__':
    list_url = 'https://data.gov.tw/datasets/export/csv'
    download_url = 'https://data.gov.tw/statistics/datasets/datasets/export/csv'
    f_name = '16-22_data_gov'

    # ===== Download and Combine =====
    # downloadList(list_url, download_url, f_name)
    # combineCSV(f_name)

    # ===== Load data =====
    load()

    # ===== process =====
    process()

    # ===== save =====
    org_name = ['屏東','基隆','苗栗','彰化','雲林','嘉義','花蓮','連江']
    org_f_name = ['15_pingtung', '16_keelung', '17_miaoli', '18_changhua', '19_yunlin', '20_chiayi_cuntry', '21_hualien', '22_lianjiang']
    for i in range(len(org_f_name)):
        lib.saveCSV(org_f_name[i], org_data[org_name[i]])
        lib.saveJSON(org_f_name[i], org_data[org_name[i]])
