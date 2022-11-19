 # -!- coding: utf-8 -!-  。
import psycopg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
#import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from datetime import datetime

conn = psycopg2.connect(host="db.zvkaicfdjrsrevzuzzxh.supabase.co", user="postgres", password ="TiBmTydtbNZ6YfiZ", dbname="postgres")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
cursor2 = conn.cursor()
print("資料庫連線成功！")

#------------------------
# 透過Browser Driver 開啟 Chrome
driver = webdriver.Chrome()
driver.implicitly_wait(3)
# 前往特定網址
default_url = "https://www.922.org.tw/response/"
driver.get(default_url)
    
cursor.execute("SELECT b_name FROM public.brand")
db = list(cursor.fetchall())
print(db)
list_a = []
cursor2.execute("SELECT b_name FROM public.brand WHERE nmcb = True")
nmcbdb = list(cursor2.fetchall())
print (len(nmcbdb))

for i in range(1,2):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
    
soup = BeautifulSoup(driver.page_source, 'html.parser')
    
for block in soup.select('.Img a'):
    for name in block:
        title = block.find('img').get('alt')
        uptime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #print(title)
        if title =='':
            continue
        elif any(title in s for s in db):
            if(title.count("'") >= 1):
                title = title.replace("'", "%")
                cursor.execute("UPDATE public.brand SET nmcb = %s, updatetime = '%s' where b_name like '%s'"%(True, uptime, title))
                #print(title)
            else:
                cursor.execute("UPDATE public.brand SET nmcb = %s, updatetime = '%s' where b_name = '%s'"%(True, uptime, title))
                #print("found/" + title)
        else:
            print(title)
            cursor.execute("INSERT INTO public.brand(b_name, nmcb, updatetime) VALUES (%s, %s, %s);",(title, True, uptime))
        list_a.append(title)     
j=0   
while (j < len(nmcbdb)):
    te = str(nmcbdb[j]).strip('(,)')  #去除資料庫前後的(,)符號
    te = te.replace("'", "")    #將'改為空白
    te = te.replace('"', '')    #將"改為空白
    if(te not in list_a):       #若資料庫的資料不存在於list_a
        #print(te)
        cursor.execute("UPDATE public.brand SET nmcb = False where b_name like '%s'"%(te))      #更新資料peta為False
    j+=1   
#print(list_a) 
driver.quit()
print('資料新增成功！')

