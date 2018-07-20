# 台灣各縣市Open Data網站—資料清冊爬蟲

## 比較
| No | City   | Name            | Frame    | auto?    | Status |
|----|--------|-----------------|:--------:|:--------:|:------:|
| 1  | 台北市  | Taipei          | No       | Yes      | Finish |
| 2  | 新北市  | NewTaipei       | CKAN     | No       | No     |
| 3  | 桃園市  | Taoyuan         | No       | Yes      | Finish |
| 4  | 新竹市  | Hsinchu         | CKAN     | Yes      | Finish |
| 5  | 台南市  | Tainan          | CKAN     | Yes      | Finish |
| 6  | 宜蘭縣  | Ilan            | CKAN     | Yes      | Finish |
| 7  | 新竹縣  | Hsinchu Country | No       | Yes      | No     |
| 8  | 台中市  | Taichung        | CKAN?    | Yes      | Finish |
| 9  | 高雄市  | Kaohsiung       | CKAN     | Yes      | Finish |
| 10 | 金門縣  | Kinmen          | No       | Yes      | FInish |
| 11 | 南投縣  | Nantou          | CKAN     | Yes      | Finish |
| 12 | 嘉義市  | Chiayi          | No       | Yes      | Finish |
| 13 | 澎湖縣  | Penghu          | CKAN     | Yes      | Finish |
| 14 | 台東縣  | Taitung         | NO       | Yes      | Finish |
| 15 | 屏東縣  | Pingtung        | data.gov | Yes      | Finish |
| 16 | 基隆市  | Keelung         | data.gov | Yes      | Finish |
| 17 | 苗栗縣  | Miaoli          | data.gov | Yes      | Finish |
| 18 | 彰化縣  | Changhua        | data.gov | Yes      | Finish |
| 19 | 雲林縣  | Yunlin          | data.gov | Yes      | Finish |
| 20 | 嘉義縣  | Chiayi Country  | data.gov | Yes      | Finish |
| 21 | 花蓮縣  | Hualien         | data.gov | Yes      | Finish |
| 22 | 連江縣  | Lianjiang       | data.gov | Yes      | Finish |

## 詳細
1.  [台北市 Taipei](#台北市-taipei)
2.  [新北市 NewTaipei](#新北市-newtaipei)
3.  [桃園市 Taoyuan](#桃園市-taoyuan)
4.  [新竹市 Hsinchu](#新竹市-hsinchu)
5.  [台南市 Tainan](#台南市-tainan)
6.  [宜蘭縣 Ilan](#宜蘭縣-ilan)
7.  [新竹縣 Hsinchu Country](#新竹縣-hsinchu-country)
8.  [台中市 Taichung](#台中市-taichung)
9.  [高雄市 Kaohsiung](#高雄市-kaohsiung)
10. [金門縣 Kinmen](#金門縣-kinmen)
11. [南投縣 Nantou](#南投縣-nantou)
12. [嘉義市 Chiayi](#嘉義市-chiayi)
13. [澎湖縣 Penghu](#澎湖縣-penghu)
14. [台東縣 Taitung](#台東縣-taitung)
15. [屏東縣 Pingtung](#屏東縣-pingtung)
16. [基隆市 Keelung](#基隆市-keelung)
17. [苗栗縣 Miaoli](#苗栗縣-miaoli)
18. [彰化縣 Changhua](#彰化縣-changhua)
19. [雲林縣 Yunlin](#雲林縣-yunlin)
20. [嘉義縣 Chiayi Country](#嘉義縣-chiayi-country)
21. [花蓮縣 Hualien](#花蓮縣-hualien)
22. [連江縣 Lianjiang](#連江縣-lianjiang)

### 台北市 Taipei
清冊資料完整  
介面好上手 開發教學簡單  
缺少瀏覽、下載次數  

### 新北市 NewTaipei
清冊資料太少  
網站顯示資料和存在CKAN API裡不符  
因為存在「子資料集」的設定，清冊和API兩個對比網站上數量不合，容易令人困惑  

### 桃園市 Taoyuan
清冊資料完整，除了瀏覽、下載次數在網頁端沒有放進去  
介面簡單、清楚

### 新竹市 Hsinchu
清冊資料過少
缺少下載、瀏覽次數  
有些重要資訊存放在CKAN的「extras」欄位裡面

### 台南市 Tainan
無清冊
介面乾淨好看、教學完整（分成使用者和開發者）
有利用CKAN存瀏覽、下載次數，讚

### 宜蘭縣 Ilan
存放資訊過少（僅有部分有資料量和主要欄位）
有些重要資訊存放在CKAN的「extras」欄位裡面

### 新竹縣 Hsinchu Country
pass

### 台中市 Taichung
清冊缺少下載瀏覽（但網站有）
資料完整度大幅度上升（全部都有！）  
不過前端API似乎改用swagger  
但CKAN裡面的資料數量和id搭不上swagger  
不太確定他們的架構  
開發說明需更新才能讓開發者使用

### 高雄市 Kaohsiung
CKAN有存瀏覽次數，但沒存下載次數  
伺服器不夠穩定

### 金門縣 Kinmen
自有平台，普通web儲存
缺少大量欄位

### 南投縣 Nantou
pass

### 嘉義市 Chiayi
自有平台、似乎是自有API
介面、資料顯示頗清楚
API應該有更多功能，但不知如何存取
開發者指引現在是空的

### 澎湖縣 Penghu
pass

### 台東縣 Taitung
伺服器不穩定
資料集分類很差

### 屏東縣 Pingtung
（另有自有平台，且有新舊兩個，有點混亂）
### 基隆市 Keelung
### 苗栗縣 Miaoli
### 彰化縣 Changhua
### 雲林縣 Yunlin
### 嘉義縣 Chiayi Country
### 花蓮縣 Hualien
### 連江縣 Lianjiang

都放在data.gov上，清冊可用但是下載是另外一個清冊
建議可把兩個合併
