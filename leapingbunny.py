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
default_url = "https://www.leapingbunny.org/shopping-guide"
driver.get(default_url)
    
cursor.execute("SELECT b_name FROM public.brand")
db = list(cursor.fetchall())
print(db)
cursor2.execute("SELECT b_name FROM public.brand WHERE leapingbunny = True")
leapingbunnydb = list(cursor2.fetchall())
print (len(leapingbunnydb))
list_a = []

    
for i in range(1,91):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
    
soup = BeautifulSoup(driver.page_source, 'html.parser')
    
for block in soup.select('.field-content a'):
    #print(block.text)
    for name in block:
        a_name = (name.text)
        uptime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if a_name =='':
            continue
        elif any(a_name in s for s in db):
            if(a_name.count("'") >= 1):
                a_name = a_name.replace("'", "%")
                cursor.execute("UPDATE public.brand SET leapingbunny = %s, updatetime = '%s' where b_name like '%s'"%(True, uptime, a_name)) 
                #print(a_name)
            else:
                cursor.execute("UPDATE public.brand SET leapingbunny = %s, updatetime = '%s' where b_name like '%s'"%(True, uptime, a_name)) 
                #print("found/" + a_name)
        else:
            print(a_name)
            cursor.execute("INSERT INTO public.brand(b_name, leapingbunny, updatetime) VALUES (%s, %s, %s);",(a_name, True, uptime))  
        list_a.append(a_name)     
j=0   
while (j < len(leapingbunnydb)):
    te = str(leapingbunnydb[j]).strip('(,)')  #去除資料庫前後的(,)符號
    te = te.replace("'", "")    #將'改為空白
    te = te.replace('"', '')    #將"改為空白
    if(te not in list_a):       #若資料庫的資料不存在於list_a
        print(te)
        cursor.execute("UPDATE public.brand SET leapingbunny = False where b_name like '%s'"%(te)) #更新資料leapingbunny為False
    j+=1   
#print(list_a) 
cursor.execute("DELETE FROM public.brand WHERE peta = False AND leapingbunny = False AND nmcb = False")
driver.quit()
print('資料新增成功！')