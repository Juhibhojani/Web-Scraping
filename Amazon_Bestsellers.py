from bs4 import BeautifulSoup
import requests

# User input for the product category, e.g., "baby"
type = "baby"

# Setting the User-Agent to simulate a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win 64; x64) AppleWeKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36"
}

# URL for the Amazon Bestsellers page of the given category
url = "https://www.amazon.in/gp/bestsellers/" + type + "/ref=zg_bs_nav_0"

# Sending a GET request to the URL and getting the HTML content of the page
html_text = requests.get(url, headers=headers).text

# Creating a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(html_text, "lxml")

# List to store the bestsellers' information
bestsellers = []

# Finding the container element that holds the information of each bestseller product
container = soup.find("div", {"class": "p13n-gridRow _cDEzb_grid-row_3Cywl"})

# Looping through each item in the container to extract the required details
for item in container.find_all("div", {"id": "gridItemRoot"}):
    # Extracting the title of the product
    title = item.find("div", {"class": "_cDEzb_p13n-sc-css-line-clamp-4_2q2cc"})
    # Extracting the price of the product
    price = item.find("span", {"class": "a-size-base a-color-price"})
    
    # If the title or price information is not available in the first class, checking for alternative class names
    if not title:
        title = item.find("div", {"class": "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"})
        price = item.find("span", {"class": "a-size-base"})
    
    # Extracting the star rating of the product
    stars = item.find("span", {"class": "a-icon-alt"})
    # If the star rating is not available, setting it to "Rating not available"
    if stars is None:
        stars = "Rating not available"
    else:
        # Extracting only the numeric part of the star rating (e.g., "4.5 out of 5" -> "4.5")
        stars = stars.text.split()[0]
    
    # Extracting the URL link of the product
    link = item.find("a", {"class": "a-link-normal"}, href=True)
    url = "https://www.amazon.in/" + link['href']
    
    # If the price information is not available, setting it to "Information not available"
    if not price:
        price = "Information not available"
    else:
        price = price.text
    
    # Creating a dictionary for the product and adding it to the bestsellers list
    product = {
        "Title": title.text,
        "Rating(out of 5)": stars,
        "Price(in rupees)": price,
        "Link": url,
    }
    bestsellers.append(product)
