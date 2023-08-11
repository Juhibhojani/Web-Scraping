import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
url = "https://www.sih.gov.in/sih2022PS"
driver.get(url)
rows = []
j = 1
while len(rows)<563:
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("table",{"id":"dataTablePS"})

    if j == 1:
        j+=1
        columns = []
        thead = container.find("thead")
        for items in thead.find_all("th"):
            columns.append(items.text.strip())

    tbody = container.find("tbody")
    for items in tbody.find_all("tr",{"class":"even"}):
        i = 1
        for item in items.find_all("td"):
          if i==1:
            sr_no = item.text
          if i==2:
            org = item.text
          if i==3:
            des = item.find("div",{"class":"style-2"}).text.strip().replace("\n"," ")
          if i==10:
            category = item.text
          if i==11:
            num = item.text
          if i ==12:
            idea = item.text
          if i==13:
            domain = item.text
            break
          i+=1
        data = [sr_no,org,des,category,num,idea,domain]
        rows.append(data)

    for items in tbody.find_all("tr",{"class":"odd"}):
        i = 1
        for item in items.find_all("td"):
          if i==1:
            sr_no = item.text
          if i==2:
            org = item.text
          if i==3:
            des = item.find("div",{"class":"style-2"}).text.strip().replace("\n"," ")
          if i==10:
            category = item.text
          if i==11:
            num = item.text
          if i ==12:
            idea = item.text
          if i==13:
            domain = item.text
            break
          i+=1
        data = [sr_no,org,des,category,num,idea,domain]
        rows.append(data)

    next = driver.find_element(By.XPATH,"//li[@id='dataTablePS_next']")
    next.click()


df = pd.DataFrame(rows,columns=columns)
df.to_csv("sih.csv")