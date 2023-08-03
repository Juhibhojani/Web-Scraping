from bs4 import BeautifulSoup
import requests

def get_restaurants(city):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) AppleWeKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"
        }
        url = "https://www.swiggy.com/city/" + city
        html_text = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_text, "lxml")

        container = soup.find("div", {"class": "sc-iBdmCd hPntbc"})
        restaurants = []
        for items in container.find_all("a", {"class": "RestaurantList__RestaurantAnchor-sc-1d3nl43-3 jrDRCS"}, href=True):
            name = items.find("div", {"class": "sc-dmyDGi bJRtXU"})
            rating = items.find("span", {"class": "sc-dmyDGi flXrCy"})
            cusine = items.find("div", {"class": "sc-dmyDGi jHWzLy"})
            location = cusine.next_sibling
            data = {
                "Name": name.text,
                "Rating": rating.text,
                "Cusine": cusine.text,
                "Location": location,
                "Link": items['href']
            }
            restaurants.append(data)
        return {"data": restaurants, "message": "Details are now fetched"}
    except:
        return {"data": None, "message": "Unable to fetch data"}
