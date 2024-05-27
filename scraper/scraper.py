import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def get_products(url, category):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    data = []
    for product in products:
        title_tag = product.find('h2')
        if title_tag is None:
            continue 

        a_tag = title_tag.find('a')
        if a_tag is None:
            continue 

        title = a_tag.text.strip()
        url = a_tag['href']

        price_tag = product.find('span', {'class': 'a-offscreen'})
        if price_tag is None:
            continue

        price = float(price_tag.text.replace('$', '').replace(',', ''))

        data.append((title, url, price, str(datetime.now())))

    return data