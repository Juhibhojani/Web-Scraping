from bs4 import BeautifulSoup
import requests
import pandas as pd
import unicodedata

airline_names = []
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36"
}
#scraping names of all airlines
for letter in range(ord('A'), ord('Z') + 1):
    l = chr(letter)
    url = f"https://www.airlinequality.com/review-pages/a-z-airline-reviews/#a2z-ldr-{l}"
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, "lxml")
    uri = f"a2z-ldr-{l}"
    container = soup.find("div", {"id":uri})
    for items in container.find_all("li"):
        airline_names.append(items.text)


# to convert names of airlines into url
start = "https://www.airlinequality.com/airline-reviews/"
end = "?sortby=post_date%3ADesc&pagesize=100"
airline_url = []
for items in airline_names:
    #converting names to lower case
    items = items.lower()
    # Replace special characters with their ASCII equivalents
    items = unicodedata.normalize('NFKD', items).encode('ASCII', 'ignore').decode('utf-8')
    # Replacing space with hypen
    items = items.replace(" ", "-")
    #creating URL
    airline_url.append(start + items + "/"+end)

df_airline = pd.DataFrame({"Name":airline_names,"Links":airline_url})

columns = ["Aircraft","Type Of Traveller","Seat Type","Route","Date Flown","Seat Comfort","Cabin Staff Service","Food & Beverages","Ground Service","Inflight Entertainment","Wifi & Connectivity","Value For Money","Recommended"]
df_columns = ["Airline Name","Overall_Rating","Review_Title","Review Date","Verified","Review","Aircraft","Type Of Traveller","Seat Type","Route","Date Flown","Seat Comfort","Cabin Staff Service","Food & Beverages","Ground Service","Inflight Entertainment","Wifi & Connectivity","Value For Money","Recommended"]

reviews = []
for index,row in df_airline.iterrows():
    html = requests.get(row['Links'], headers=headers).text
    bs = BeautifulSoup(html, "html.parser")
    container = bs.find("article", {"class": "comp comp_reviews-airline querylist position-content"})
    if container:
        for items in container.find_all("article"):
            verified = False
            rating = items.find("div", {"class": "rating-10"})
            if rating:
                rating = rating.text.strip()[:1]
            else:
                rating = None
            title = items.find("h2")
            if title:
                title = title.text
            else:
                title = None
            time = items.find("h3").find("time")
            if time:
                time = time.text
            else:
                time = None
            text = items.find("div", {"class": "text_content"}).text
            text = text.split("|")
            if len(text)==1:
                review = text[0]
            else:
                if text[0] =='✅ Trip Verified ':
                    verified = True
                review = text[1]
            table = items.find("table")
            tab = [None]*13
            for item in table.find_all("tr"):
                i = 0
                for td in item.find_all("td"):
                    if i == 0:
                        condition = td.text
                        #Finding index of given condition
                        ind = columns.index(condition)
                        i = 1
                    else:
                        #checking if its rating or not
                        if td.find("span") is None:
                            value = td.text
                            tab[ind] = value
                        #in case its rating, counting stars filled i.e starts given
                        else:
                            value = 0
                            for star in td.find_all("span", {"class": "star fill"}):
                                value += 1
                            tab[ind] = value
            data = [row['Name'],rating, title, time, verified,review] + tab
            reviews.append(data)
        else:
            continue

df = pd.DataFrame(reviews, columns=df_columns)
df.to_csv("Airline_review.csv")