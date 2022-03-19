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
from selenium import webdriver
import time, re
from bs4 import BeautifulSoup


# 透過Browser Driver 開啟 Chrome
driver = webdriver.Chrome()
driver.implicitly_wait(3)
# 前往特定網址
default_url = "https://www.leapingbunny.org/shopping-guide"
driver.get(default_url)

cursor.execute("SELECT b_name FROM public.brand")
db = cursor.fetchall()
print(db)

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
                a_name =a_name.replace("'", "")
                cursor.execute("UPDATE public.brand SET leapingbunny = %s where b_name like '%s'"%(True, a_name))
                print(a_name)
            else:
                cursor.execute("UPDATE public.brand SET leapingbunny = %s where b_name = '%s'"%(True, a_name))
                #print("found/" + a_name)
        else:
            print(a_name)
            cursor.execute("INSERT INTO public.brand(b_name, leapingbunny) VALUES (%s, %s);",(a_name, True))

print('資料新增成功！')
