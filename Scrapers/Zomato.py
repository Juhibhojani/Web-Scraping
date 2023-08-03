import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

# Set up the Chrome webdriver
driver = webdriver.Chrome()

url = "https://zomato.com/ahmedabad/restaurants/cafes?category=2"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Get the HTML of the page after waiting for some time
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

container = soup.find("div", {"id": "root"})

# Loop through the containers to extract restaurant information
while True:
    i = 0
    for items in container.find_all("div", class_=re.compile("sc-1mo3ldo-0 sc-")):
        if i == 0:
            i = 1
            continue
        print(items.text)
        first_child = items.find("div")
        for item in first_child:
            link = item.find("a", href=True)['href']
            print(link)
            name = item.find("h4")
            print(name.text)
            rating = item.find("div", {"class": "sc-1q7bklc-1 cILgox"})
            print(rating.text)
            cusine = item.find("p")
            print(cusine.text)
            rate = item.find("p").next_sibling
            print(rate.text)
