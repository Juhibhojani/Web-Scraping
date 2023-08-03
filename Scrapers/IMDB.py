from bs4 import BeautifulSoup
import requests

headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win 64 ; x64) Apple WeKit /537.36(KHTML , like Gecko) Chrome/80.0.3987.162 Safari/537.36'}
url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
html_text = requests.get(url,headers=headers).text
soup = BeautifulSoup(html_text, "lxml")
movies_container = soup.find("ul", {"class":"ipc-metadata-list ipc-metadata-list--dividers-between sc-3a353071-0 wTPeg compact-list-view ipc-metadata-list--base"})
movies = []

for items in movies_container.find_all("li"):
    title = items.find("h3").text
    years = items.find("span",{"class":"sc-14dd939d-6 kHVqMR cli-title-metadata-item"})
    years = years.text
    duration = years.next_sibling
    duration = duration.text
    age_criteria = duration.next_sibling
    age = age_criteria.text
    rating = items.find("span",{"class":"ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"})
    rating = rating.text
    data = {
        "Title":title,
        "Year":years,
        "Duration":duration,
        "Age Criteria":age,
        "Rating":rating
    }
    movies.append(data)
