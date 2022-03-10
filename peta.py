 # -!- coding: utf-8 -!-  。

import psycopg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import requests
from bs4 import BeautifulSoup

conn = psycopg2.connect(host="ec2-54-209-221-231.compute-1.amazonaws.com", user="ikojmqzefffjen", password ="079aad0bfbbc125c2f41389d7d65a83fe63f775aa42799b01120e8edb480ab2f", dbname="d28e9f04ls9tcu")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
print("資料庫連線成功！")

#------------------------
r = requests.get("https://crueltyfree.peta.org/companies-dont-test/") #將此頁面的HTML GET下來
soup = BeautifulSoup(r.text,"html.parser") #將網頁資料以html.parser
sel = soup.select("ul.search-results a") #選取 ul.search-results a ，並存入sel
url = "https://crueltyfree.peta.org/companies-dont-test/"

cursor.execute("SELECT b_name FROM public.brand")
db = cursor.fetchall()
print(db)

for i in range(2,4): #2~13頁
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    sel = soup.select("ul.search-results a") #標題
    print ("本頁的URL為"+url)
    url = "https://crueltyfree.peta.org/companies-dont-test/page/" + str(i) #下一頁的網址
    for name in sel:
        cursor = conn.cursor()
        a_name = (name.text)
        if a_name =='':
            continue
        elif any(a_name in s for s in db):
            cursor.execute("UPDATE public.brand SET peta = True where b_name = '%s'"%(a_name))
            print("found/" + a_name)
        else:
            #print(a_name)
            cursor.execute("INSERT INTO public.brand(b_name, peta) VALUES (%s, %s);",(a_name, True))

print('資料新增成功！')

