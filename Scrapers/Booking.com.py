from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pandas as pd
from selenium.webdriver.common.by import By


def get_links():
    hotels = []

    # Loop through multiple pages of hotel search results
    for i in range(1, 40):
        # Construct the URL for hotel search in New Delhi
        url = f"https://www.booking.com/searchresults.en-gb.html?ss=New+Delhi&ssne=New+Delhi&ssne_untouched=New+Delhi&efdco=1&label=gen173nr-1BCAEoggI46AdIM1gEaGyIAQGYAQm4ARfIAQzYAQHoAQGIAgGoAgO4ApC0nKcGwAIB0gIkZWI3M2YwNGEtNjdiOC00ZmU1LWE0ODYtYzQ5MzFhOTUyYzQx2AIF4AIB&sid=8751dd3a40c19aea276ecfb406557a80&aid=304142&lang=en-gb&sb=1&src_elem=sb&src=searchresults&dest_id=-2106102&dest_type=city&checkin=2023-08-25&checkout=2023-08-26&group_adults=2&no_rooms=1&group_children=0&flex_window=1&offset={25 * i}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"
        }
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        container = soup.find("body")

        # Extract hotel information from each search result
        for items in container.find_all("div", {
            "class": "c82435a4b8 a178069f51 a6ae3c2b40 a18aeea94d d794b7a0f7 f53e278e95 da89aeb942"}):
            name = items.find("h3").find("div")
            location = items.find("span", {"class": "f4bd0794db b4273d69aa"})
            link = items.find("a")
            data = [name.text, location.text, link['href']]
            hotels.append(data)

        # Create a DataFrame from collected hotel data and save to CSV
        df = pd.DataFrame(hotels)
        df.rename(columns={0: "Name", 1: "Area", 2: "Link"}, inplace=True)
        df.to_csv(r"hotels.csv")


def get_reviews():
    # Read hotel data from CSV
    df = pd.read_csv(r"hotels.csv")
    hotel = []

    # Iterate through each hotel to collect reviews
    for row, item in df.iterrows():
        url = item['Link']
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        try:
            # Extract guest reviews for each hotel
            for items in soup.find_all("li", {"class": "a0661136c9"}):
                if items.text.split()[0] == "Guest":
                    driver.find_element(By.XPATH, "//a[@rel='reviews']").click()
                    time.sleep(2)
                    html = driver.page_source
                    soup = BeautifulSoup(html, "html.parser")
                    for items in soup.find_all("li", {"class": "review_list_new_item_block"}):
                        date = items.find("span", {"class": "c-review-block__date"})
                        date = date.text.strip()
                        rating = items.find("h3")
                        rating = rating.text.strip()
                        rating_num = items.find("div", {"class": "bui-review-score c-score"})
                        rating_num = rating_num.text.strip()
                        text = items.find("div", {"class": "c-review__row"})
                        text = text.text.strip()[9:]
                        data = [item['Name'], item['Area'], date, rating, rating_num, text]
                        hotel.append(data)
        except Exception:
            continue

        # Create a DataFrame from collected review data and save to CSV
        df1 = pd.DataFrame(hotel)
        df1.to_csv(r"hotel_reviews.csv")


if __name__ == '__main__':
    # Execute the functions to gather hotel links and reviews
    get_links()
    get_reviews()
