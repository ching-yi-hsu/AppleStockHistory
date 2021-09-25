from time import time_ns
import urllib.request as req
import bs4
import datetime ,time
import pandas as pd
import json

#字串日期轉日期格式
def cov_str_to_date(aa):
    yy= aa.split("年")[0]
    mm=aa.split("年")[1].split("月")[0]
    dd =aa.split("年")[1].split("月")[1].split("日")[0]
    ymd = yy+"-"+mm+"-"+dd
    ymd = datetime.datetime.strptime(ymd,"%Y-%m-%d")
    return ymd

#抓日期範圍(預設七天)
def range_date(day, rows):
    today = datetime.date.today()
    half_year_ago = today - datetime.timedelta(days = day)
    half_year_ago = datetime.datetime.strptime(str(half_year_ago),"%Y-%m-%d")


    range_data = []

    for m_rows in rows:
        date_row = cov_str_to_date(m_rows[0:1][0])
        if date_row >= half_year_ago:
            range_data.append(m_rows)

    return range_data

#連接網頁與擷取資料
url ="https://cn.investing.com/equities/apple-computer-inc-historical-data"
request = req.Request(url, headers ={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
})

with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

root = bs4.BeautifulSoup(data, "html.parser")
all_dates= root.find("table", class_= "genTbl closedTbl historicalTbl")
finddates = root.find_all("td", class_= "first left bold noWrap")
columns = [th.text.replace('\n', '') for th in all_dates.find('tr').find_all('th')]

trs = all_dates.find_all('tr')[1:]
rows = list()
day = 7
for tr in trs:
    rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])

days_row = range_date( day,rows)
df = pd.DataFrame(data = days_row , columns = columns)

#以json存入資料
file_name = "applestockhistory.json"
with open(file_name,'w') as file :
    json.dump(days_row,file)

with open(file_name,'r') as file :
    contents = json.load(file)
    print(contents)