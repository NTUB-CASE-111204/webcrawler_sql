# -!- coding: utf-8 -!-  。
import psycopg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from bs4 import BeautifulSoup
import requests
from datetime import datetime

conn = psycopg2.connect(host="ec2-54-209-221-231.compute-1.amazonaws.com", user="ikojmqzefffjen", password ="079aad0bfbbc125c2f41389d7d65a83fe63f775aa42799b01120e8edb480ab2f", dbname="d28e9f04ls9tcu")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
cursor2 = conn.cursor()
print("資料庫連線成功！")

#------------------------
url = "https://crueltyfreeinternational.org/choose-cruelty-free-ccf-list-brands"
r = requests.get("https://crueltyfreeinternational.org/choose-cruelty-free-ccf-list-brands")
soup = BeautifulSoup(r.text, "html.parser")   #將網頁資料以html.parser
sel =soup.select("table a") #選取 table a ，並存入sel
cursor.execute("SELECT b_name FROM public.brand")
db = list(cursor.fetchall())
print(db)
cursor2.execute("SELECT b_name FROM public.brand WHERE ccf = True")
ccfdb = list(cursor2.fetchall())
print (len(ccfdb))
list_a = []

for name in sel:
        a_name = (name.text)
        uptime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if a_name =='':      #跳過空白的資料
            continue
        elif any(a_name in s for s in db):  #確認標題是否已存在資料庫
            if(a_name.count("'") >= 1):  #標題裡有'符號
                a_name =a_name.replace("'","%")
                cursor.execute("UPDATE public.brand SET ccf = %s, updatetime = '%s' where b_name like '%s'"%(True, uptime, a_name))    #更新資料ccf為True
                #print("update///" + a_name)
            else:
                cursor.execute("UPDATE public.brand SET ccf = %s, updatetime = '%s' where b_name like '%s'"%(True, uptime, a_name))   #更新資料ccf為True
                #print("found/" + a_name)
        else:
            cursor.execute("INSERT INTO public.brand(b_name, ccf, updatetime) VALUES (%s, %s, %s);",(a_name, True, uptime))    #新增資料
        list_a.append(a_name)     #將a_name放進list最後
        #print(list_a)
        
j=0   
while (j < len(ccfdb)):
    te = str(ccfdb[j]).strip('(,)')  #去除資料庫前後的(,)符號
    te = te.replace("'", "")    #將'改為空白
    te = te.replace('"', '')    #將"改為空白
    if(te not in list_a):       #若資料庫的資料不存在於list_a
        print(te)
        cursor.execute("UPDATE public.brand SET ccf = False where b_name like '%s'"%(te))      #更新資料ccf為False
    j+=1    
   
print('資料新增成功！')