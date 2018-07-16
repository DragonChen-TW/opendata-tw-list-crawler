'''
Author: SmallDragon Chen
City:   Kaohsiung
Url:    https://data.kcg.gov.tw
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
    # print(len(id_list))
    # print(id_list[0:10])

def getWeb(id):
    try:
        url = 'http://data.kcg.gov.tw/dataset/' + id
        res = requests.get(url)
        soup = BeautifulSoup(res.text,'html.parser')

        dd = soup.find(class_='secondary').find(class_='nums').findAll('dd')[1].text

        return dd
    except:
        return 0
def getEach(i, id):
    try:
        url = 'http://data.kcg.gov.tw/api/3/action/package_show?include_tracking=1&id=' + id
        res = requests.get(url)
        res = json.loads(res.text)['result']

        temp = {}

        temp['編號'] = i + 1

        temp['資料集名稱'] = res['title']
        temp['資料來源(部會單位)'] = res['author']
        temp['第一層級'] = '高雄市政府'

        temp['瀏覽次數'] = res['tracking_summary']['total']
        if len(res['resources']) > 0:
            temp['主要欄位'] = res['resources'][0]['description'].replace('\n','').replace('\r','')

        temp['資料量'] = 0
        for e in res['extras']:
            if e['key'] == '資料量':
                temp['資料量'] = e['value']

        temp['下載次數'] = getWeb(id)

        print(i, temp['資料集名稱'], temp['下載次數'])
    except:
        temp = {}
        temp['編號'] = i
        temp['資料集名稱'] = 'error'

    return temp
def getAll():
    global data

    pool = Pool(size=10)
    pool.add_tasks([ ( getEach, (i, id,))  for i, id in enumerate(id_list)])
    pool.run()

    temp_list = list(pool.output_queue.queue)
    temp_list.sort(key=lambda e: e['編號'])
    data = temp_list

    print(list(pool.error_queue.queue))
def getError():
    global data
    with open('../out/csv/09_kaohsiung.csv') as csv_f:
        reader = csv.DictReader(csv_f)
        data = [l for l in reader]

    print(sum([d['資料集名稱'] == 'error' for d in data]))

    data = [d if d['資料集名稱'] != 'error' else getEach(i, id_list[i]) for i, d in enumerate(data)]

if __name__ == '__main__':
    list_url = 'http://data.kcg.gov.tw/api/3/action/package_list?limit=3000&offset=0'
    f_name = '09_kaohsiung'

    # ===== Download or Load data =====
    load(list_url)

    # ===== process =====
    # getAll()
    getError()

    # process()
    # print(data)
    # print(getEach(1, 'excellent-deer'))

    # ===== save =====
    lib.saveCSV(f_name, data)
    lib.saveJSON(f_name, data)
