from bs4 import BeautifulSoup
import requests

all_books = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
for page_link in ["https://www.amazon.in/gp/bestsellers/digital-text/ref=zg_bs_nav_0","https://www.amazon.in/gp/bestsellers/digital-text/ref=zg_bs_pg_2_digital-text?ie=UTF8&pg=2"]:
    webpage = requests.get(page_link,headers=headers).text
    soup = BeautifulSoup(webpage, "lxml")
    books_container = soup.find("div", {"class": "p13n-gridRow _cDEzb_grid-row_3Cywl"})
    for items in books_container.find_all("div", {"id": "gridItemRoot"}):
        title = items.find("div", {"class": "_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"}).text
        stars = items.find("span", {"class": "a-icon-alt"})
        if stars is None:
            stars = "Rating not available"

        else:
            stars = stars.text.split()[0]
        price = items.find("span", {"class": "a-size-base"}).text
        link = items.find("a", {"class": "a-link-normal"}, href=True)
        url = "https://www.amazon.in/" + link['href']
        books = {
            "Title":title,
            "Rating(out of 5)":stars,
            "Price(in rupees)":price,
            "Link":url,
        }
        all_books.append(books)
print(all_books,len(all_books))