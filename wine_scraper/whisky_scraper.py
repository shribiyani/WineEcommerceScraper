import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


baseurl = 'https://www.thewhiskyexchange.com/'
headers = {
    "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
}

productlinks = []
for x in range(1, 50):
    r = requests.get(f'https://www.thewhiskyexchange.com/search?q=whisky&pg={x}&psize=120')
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('li', class_="product-grid__item")
    # print(productlist)
    for item in productlist:
        for link in item.find_all('a', href=True):
            productlinks.append(baseurl + link['href'])

# testlink = 'https://www.thewhiskyexchange.com/p/52345/mortlach-15-year-old-game-of-thrones-six-kingdoms'

whiskylist = []

for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    # Product details
    try:
        name = soup.find('h1', class_="product-main__name").text.strip() # Name of product
    except:
        name = 'None'

    try:
        offer_price = re.compile(r'\d+\.\d+').findall(
            soup.find('p', class_="product-action__price").text.strip())  # Auction price
    except:
        offer_price = None

    try:
        actual_price = re.compile(r'\d+\.\d+').findall(soup.find('p', class_="product-action__unit-price").text.strip())  # Original price per bottle
    except:
        actual_price = 'None'

    try:
        rating = soup.find('span', class_ = 'review-overview__rating star-rating star-rating--40').text.strip() # Available ratings

    except:
        rating = "None"

    try:
        reviews = re.compile(r'\d+').findall(soup.find('span', class_ = 'review-overview__count').text.strip()) # Review Counts only
    except:
        reviews = "None"

    try:
        offer_type = soup.find('span', class_ = "product-offer__text").text[0:13].strip() # discount type apply in auction
    except:
        offer_type = "None"

    # offer_amt = soup.find('span', class_ = "product-offer__text").text[14:20].strip() # discount amount
    try:
        product_description = soup.find('div', class_ = "product-main__description").text.strip()
    except:
        product_description = "None"

    whisky = {
        'product_name' : name
        , 'product_rating' : rating
        , 'product_reviews' : reviews
        , 'auction_price' : offer_price
        , 'original_price' : actual_price
        , 'offer_type' : offer_type
        # , 'discount_amt' : offer_amt
        , 'product_description' : product_description
    }
    whiskylist.append(whisky)

# print(whiskylist)

# Creating the DataFrame
df = pd.DataFrame(whiskylist)

print(df.head(5))
# Exporting the DataFrame as csv
df.to_csv('whisky_scrap.csv', index=False, sep=';')
