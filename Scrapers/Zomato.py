import re
import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

def scroll_to_bottom(driver):
    # Scroll to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Adjust the wait time based on your network speed and content loading speed

def parse_and_print_items(container,city):
    data = []
    for items in container.find_all("div", class_=re.compile("sc-1mo3ldo-0 sc-")):
        if items.find("h4"):
            link = "https://www.zomato.com" + items.find("a", href=True)['href']
            print("Link:", link)
            name = items.find("h4").text
            print("Name:", name)
            rating = items.find("div", {"class": "sc-1q7bklc-1 cILgox"}).text
            print("Rating:", rating)
            cuisine = items.find("p").text
            print("Cuisine:", cuisine)
            rate = items.find("p").next_sibling.text
            print("Rate:", rate)
            print("-" * 50)
            print(city)
            li = [name,rating,cuisine,rate,link,city]
            data.append(li)
    return data



def infinite_scroll(url,city):
    driver = webdriver.Chrome()
    driver.get(url)
    x = []
    try:
        while True:
            scroll_to_bottom(driver)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            container = soup.find("div", {"id": "root"})
            x += parse_and_print_items(container,city)
    except:
        print("Scraping interrupted by the user.")
        return x
    finally:
        driver.quit()

if __name__ == "__main__":
    x = []
    cites = ["ahmedabad","mumbai","pune","bangalore","udaipur","jaipur","surat","indore","chennai","chandigarh"]
    for city in cites:
        url_to_scrape = f"https://zomato.com/{city}/restaurants/cafes?category=2"
        x += infinite_scroll(url_to_scrape,city)
    df = pd.DataFrame(x)
    df.to_csv(r"zomato.csv")
