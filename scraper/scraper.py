import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import random
import os

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    # Add more user agents as needed
]


def get_products(url, category):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

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
        url = 'https://www.amazon.com' + a_tag['href']

        price_tag = product.find('span', {'class': 'a-offscreen'})
        if price_tag is None:
            continue

        price = float(price_tag.text.replace(
            '$', '').replace('£', '').replace(',', ''))
        data.append((title, category, url, price, str(datetime.now())))

    return data


urls = {
    'CPU': 'https://www.amazon.com/s?k=cpu',
    'RAM': 'https://www.amazon.com/s?k=ram',
    'GPU': 'https://www.amazon.com/s?k=gpu'
}


def scrape_DB_save():
    conn = sqlite3.connect('../db/amazon_prices.db')
    cursor = conn.cursor()

    for category, base_url in urls.items():
        for page in range(1, 21):
            url = f"{base_url}&page={page}"
            products_data = get_products(url, category)
            cursor.executemany(
                'INSERT INTO products (name, category, url, price, created_at) VALUES (?, ?, ?, ?, ?)', products_data)
            # Random delay between 5 to 10 seconds
            time.sleep(random.uniform(5, 10))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    scrape_DB_save()
