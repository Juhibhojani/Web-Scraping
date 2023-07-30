from bs4 import BeautifulSoup
import requests

type = "baby" #user input
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36"}
url = "https://www.amazon.in/gp/bestsellers/" +type+"/ref=zg_bs_nav_0"
html_text = requests.get(url, headers=headers).text
soup = BeautifulSoup(html_text, "lxml")

bestsellers = []
container = soup.find("div",{"class":"p13n-gridRow _cDEzb_grid-row_3Cywl"})


for items in container.find_all("div",{"id":"gridItemRoot"}):
    title = items.find("div", {"class": "_cDEzb_p13n-sc-css-line-clamp-4_2q2cc"})
    price = items.find("span", {"class": "a-size-base a-color-price"})
    if not title:
        title = items.find("div", {"class": "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"})
        price = items.find("span", {"class": "a-size-base"})
    stars = items.find("span", {"class": "a-icon-alt"})
    if stars is None:
        stars = "Rating not available"

    else:
        stars = stars.text.split()[0]
    link = items.find("a", {"class": "a-link-normal"}, href=True)
    url = "https://www.amazon.in/" + link['href']
    if not price:
        price = "Information not available"
    else:
        price = price.text
    products = {
        "Title":title.text,
        "Rating(out of 5)":stars,
        "Price(in rupees)":price,
        "Link":url,
    }
    bestsellers.append(products)
print(bestsellers)