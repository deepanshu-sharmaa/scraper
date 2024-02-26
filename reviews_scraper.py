# -*- coding: utf-8 -*-
"""Reviews Scraper.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a4d_G5cCJ21TzNJZVicBiGFQ7vQy45V6
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Product Title
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})

        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()

    except AttributeError:
        title_string = ""

    return title_string

# Function to extract Product Price
def get_price(soup):

    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price

# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"

    return available

def get_reviews(soup):
    try:
        reviews_list = []

        # Try finding reviews with the first class
        all_reviews = soup.find_all("div", attrs={'class':'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'})

        if not all_reviews:
            # If no reviews found with the first class, try with an alternative class
            all_reviews = soup.find_all("div", attrs={'class':'review-text-sub-contents'})

        for review in all_reviews:
            # review = all_reviews[i].find("span").string.strip()
            reviews_list.append(review.find("span").get_text(strip=True))

    except AttributeError:
        reviews_list = ["Not Available"]

    return reviews_list

# def get_reviews(soup):
#     try:
#         reviews_list = []
#         all_reviews = soup.find_all("div", attrs={'class':'a-expander-content reviewText review-text-content a-expander-partial-collapse-content'})

#         for review in all_reviews:
#             # review = all_reviews[i].find("span").string.strip()
#             reviews_list.append(review.find("span").string.strip())

#     except AttributeError:
#         reviews_list = ["Not Available"]

#     return reviews_list

if __name__ == '__main__':

    # add your user agent
    HEADERS = ({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

    # The webpage URL
    URL = "https://www.amazon.in/s?k=mamaearth&crid=YAFFN0HQLE2X&sprefix=mamae%2Caps%2C1230&ref=nb_sb_ss_ts-doa-p_3_5"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag Objects
    for link in links:
            links_list.append(link.get('href'))

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    # Loop for extracting product details from each link
    for link in links_list:
        print(link)
        if link[0] == "/":
          new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

          new_soup = BeautifulSoup(new_webpage.content, "html.parser")

          # Function calls to display all necessary product information
          d['title'].append(get_title(new_soup))
          d['price'].append(get_price(new_soup))
          d['rating'].append(get_rating(new_soup))
          d['reviews'].append(get_review_count(new_soup))
          d['availability'].append(get_availability(new_soup))


    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'].replace('', np.nan, inplace=True)
    amazon_df = amazon_df.dropna(subset=['title'])
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)

reviews = []
d = {"title":[], "reviews":[]}
for link in links_list:
    if link[0] == "/":
        webpage = requests.get("https://www.amazon.in/" + link, headers=HEADERS)
        soup = BeautifulSoup(webpage.content, "html.parser")
        d['title'].append(get_title(soup))
        d['reviews'].append(get_reviews(soup))

amazon_new_df = pd.DataFrame.from_dict(d)
amazon_new_df['title'].replace('', np.nan, inplace=True)
amazon_new_df = amazon_new_df.dropna(subset=['title'])
amazon_new_df.to_csv("amazon_review_data.csv", header=True, index=False)
# reviews

amazon_new_df

amazon_df