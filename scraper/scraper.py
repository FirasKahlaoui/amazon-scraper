import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import time
import os
import random
from urllib.robotparser import RobotFileParser

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
]

# List of proxies
proxies = [
    "http://116.125.141.115:80",
    "http://116.73.243.169:80",
    "http://101.109.119.24:80",
    "http://1.179.148.9:80"
]

# Check robots.txt
robots_url = "https://www.amazon.com/robots.txt"
rp = RobotFileParser()
rp.set_url(robots_url)
rp.read()
if not rp.can_fetch("*", "https://www.amazon.com/s?k=cpu"):
    print("Scraping not allowed by robots.txt")
    exit()

def get_products(url, category):
    headers = {
        "User-Agent": random.choice(user_agents)
    }
    proxy = {
        "http": random.choice(proxies),
        "https": random.choice(proxies)
    }

    try:
        response = requests.get(url, headers=headers, proxies=proxy)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        data = []
        for product in products:
            title_tag = product.find('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})
            if title_tag is None:
                title_tag = product.find('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-4'})

            if title_tag is None:
                continue

            a_tag = title_tag.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
            if a_tag is None:
                continue

            title = a_tag.text.strip()
            product_url = 'https://www.amazon.com' + a_tag['href']

            price_tag = product.find('span', {'class': 'a-offscreen'})
            if price_tag is None:
                continue

            price = float(price_tag.text.replace('$', '').replace('£', '').replace(',', ''))

            data.append((title, category, product_url, price, str(datetime.now())))

        return data

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

urls = {
    'CPU': 'https://www.amazon.com/s?k=cpu',
    'RAM': 'https://www.amazon.com/s?k=ram',
    'GPU': 'https://www.amazon.com/s?k=gpu'
}

def scrape_DB_save():
    conn = sqlite3.connect('../db/amazon_prices.db')
    cursor = conn.cursor()

    for category, base_url in urls.items():
        for page in range(1, 21):  # Change the range as needed
            url = f"{base_url}&page={page}"
            products_data = get_products(url, category)
            if products_data:
                cursor.executemany(
                    'INSERT INTO products (name, category, url, price, created_at) VALUES (?, ?, ?, ?, ?)', products_data)
            # Sleep for 5 seconds to avoid getting blocked
            time.sleep(random.uniform(5, 10))  # Random delay between 5 and 10 seconds

    conn.commit()
    conn.close()

if __name__ == "__main__":
    scrape_DB_save()
