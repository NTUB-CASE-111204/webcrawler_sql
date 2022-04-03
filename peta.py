 # -!- coding: utf-8 -!-  。

import psycopg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import requests
from bs4 import BeautifulSoup
#from jedi.inference.value import iterable
#from test.test_xmlrpc import alist

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
db = list(cursor.fetchall())
print(db)
list_a = []

for i in range(2,15): #2~13頁
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    sel = soup.select("ul.search-results a") #標題
    print ("本頁的URL為"+url)
    url = "https://crueltyfree.peta.org/companies-dont-test/page/" + str(i) #下一頁的網址
    for name in sel:
        a_name = (name.text)
        if a_name =='':      #跳過空白的資料
            continue
        elif any(a_name in s for s in db):  #確認標題是否已存在資料庫
            if(a_name.count("'") >= 1):  #標題裡有'符號
                a_name =a_name.replace("'","%")
                cursor.execute("UPDATE public.brand SET peta = %s where b_name like '%s'"%(True, a_name))   #更新資料peta為True
                #print("update///" + a_name)
            else:
                cursor.execute("UPDATE public.brand SET peta = %s where b_name = '%s'"%(True, a_name))  #更新資料peta為True
                #print("found/" + a_name)
        else:
            print(a_name)
            cursor.execute("INSERT INTO public.brand(b_name, peta) VALUES (%s, %s);",(a_name, True))    #新增資料
        list_a.append(a_name)     #將a_name放進list最後
        #print(list_a)
        
j=0   
while (j < len(db)):
    te = str(db[j]).strip('(,)')  #去除資料庫前後的(,)符號
    te = te.replace("'", "")    #將'改為空白
    te = te.replace('"', '')    #將"改為空白
    if(te not in list_a):       #若資料庫的資料不存在於list_a
        print(te)
        cursor.execute("UPDATE public.brand SET peta = False where b_name like '%s'"%(te))      #更新資料peta為False
    j+=1    
print('資料新增成功！')

