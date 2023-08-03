from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

class MagicBricks:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36"
        }

    def get_ready_to_move_flats(self, city):
        try:
            details = [
                "Carpet Area",
                "Status",
                "Floor",
                "Transaction",
                "Furnishing",
                "Facing",
                "Overlooking",
                "Society",
                "Bathroom",
                "Balcony",
                "Car Parking",
                "Ownership",
                "Super Area",
                "Dimensions",
                "Plot Area",
            ]
            city_slug = city.replace(" ", "-").lower()
            url = f"https://www.magicbricks.com/ready-to-move-flats-in-{city_slug}-pppfs"
            html_text = requests.get(url, headers=self.headers).text
            soup = BeautifulSoup(html_text, "lxml")

            flats_data = []
            container = soup.find("div", {"class": "mb-srp__left"})
            total_results_text = container.find("li", {"class": "mb-srp__tabs__list--item"}).text
            total_results = int(re.findall(r"\d{1,3}(?:,\d{3})*", total_results_text)[0].replace(",", ""))
            num_of_pages = (total_results // 30) + 1

            for i in range(1, num_of_pages + 1):
                if i == 1:
                    url = f"https://www.magicbricks.com/ready-to-move-flats-in-{city_slug}-pppfs/"
                else:
                    url = f"https://www.magicbricks.com/ready-to-move-flats-in-{city_slug}-pppfs/page-{i}"

                html_text = requests.get(url, headers=self.headers).text
                soup = BeautifulSoup(html_text, "lxml")

                for item in soup.find_all("div", {"class": "mb-srp__list"}):
                    title = item.find("h2").text
                    labels = {key: None for key in details}
                    for detail_item in item.find_all("div", {"class": "mb-srp__card__summary__list--item"}):
                        label = detail_item.find("div", {"class": "mb-srp__card__summary--label"}).text
                        value = detail_item.find("div", {"class": "mb-srp__card__summary--value"}).text
                        if label in details:
                            labels[label] = value

                    description = item.find("div", {"class": "mb-srp__card--desc--text"})
                    description = description.text if description else None

                    amount = item.find("div", {"class": "mb-srp__card__price--amount"}).text

                    price_per_sqft = item.find("div", {"class": "mb-srp__card__price--size"})
                    price_per_sqft = price_per_sqft.text if price_per_sqft else None

                    flat_data =[title,description,amount.text,price_per_sqft,city]+labels
                    flats_data.append(flat_data)

            return flats_data
        except Exception as e:
            return None


# Scraping names of all cities
cities = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36"
}
url = "https://www.magicbricks.com/property-for-sale-rent-in-Pune/residential-real-estate-Pune"
html_text = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_text, "lxml")

container = soup.find("div", {"class": "city-drop-lt"})
for item in container.find_all("li"):
    cities.append(item.text.strip())

flats_info = []
for city in cities:
    ready_to_move_flats_data = MagicBricks().get_ready_to_move_flats(city)
    if ready_to_move_flats_data:
        flats_info.extend(ready_to_move_flats_data)
    else:
        print(f"No data found for {city}")

df = pd.DataFrame(flats_info)
df.to_csv(r"House_Price.csv")
