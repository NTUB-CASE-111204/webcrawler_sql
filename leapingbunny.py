# -!- coding: utf-8 -!-  。
import psycopg2 
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
#import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
import time

conn = psycopg2.connect(host="ec2-54-209-221-231.compute-1.amazonaws.com", user="ikojmqzefffjen", password ="079aad0bfbbc125c2f41389d7d65a83fe63f775aa42799b01120e8edb480ab2f", dbname="d28e9f04ls9tcu")
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()
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

uptime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(db)

list_a = []
    
for i in range(1,2):
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(1)
    
soup = BeautifulSoup(driver.page_source, 'html.parser')
    
for block in soup.select('.field-content a'):
    #print(block.text)
    for name in block:
        cursor = conn.cursor()
        a_name = (name.text)
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
            cursor.execute("INSERT INTO public.brand(b_name, leapingbunny) VALUES (%s, %s);",(a_name, True))

            
        list_a.append(a_name)     
j=0   
while (j < len(db)):
    te = str(db[j]).strip('(,)')  #去除資料庫前後的(,)符號
    te = te.replace("'", "")    #將'改為空白
    te = te.replace('"', '')    #將"改為空白
    if(te not in list_a):       #若資料庫的資料不存在於list_a
        print(te)
        cursor.execute("UPDATE public.brand SET leapingbunny = False where b_name like '%s'"%(te))      #更新資料peta為False
    j+=1   
print(list_a) 
driver.quit()
 


#print(df.strftime('%Y-%m-%d %H:%M:%S'))
#sql_insert=sql_insert="INSERT into public.brand(updatetime) values(str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'))" %(df.strftime("%Y-%m-%d %H:%M:%S"))
#cursor.execute("INSERT INTO public.brand(updatetime) VALUES (%s)",(now))
#cursor.execute("UPDATE public.brand SET leapingbunny SET updatetime = '%s'"%(now))

# 取得現在時間

#txt = '上次更新時間為：' + str(now)

#轉成df
#df = pandas.DataFrame([txt], index=['UpdateTime'])

# 存出檔案
#df.to_csv('log.csv', header=False)