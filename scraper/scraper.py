import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os


def get_products(url, category):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    data = []
    for product in products:
        title_tag = product.find(
            'h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})

        # Skip products without a title
        if title_tag is None:
            continue

        # Skip products without a link
        a_tag = title_tag.find(
            'a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        if a_tag is None:
            continue
        title = a_tag.text.strip()
        url = 'https://www.amazon.com' + a_tag['href']

        price_tag = product.find('span', {'class': 'a-offscreen'})
        if price_tag is None:
            continue

        price = float(price_tag.text.replace('$', '').replace(',', ''))

        data.append((title, url, price, str(datetime.now())))

    return data


urls = {
    'CPU': 'https://www.amazon.com/s?k=cpu',
    'RAM': 'https://www.amazon.com/s?k=ram',
    'GPU': 'https://www.amazon.com/s?k=gpu'
}


def scrape():
    for category, base_url in urls.items():
        for page in range(1, 21):  # Change the range as needed
            url = f"{base_url}&page={page}"
            products_data = get_products(url, category)

            # Check if data directory exists, if not, create it
            if not os.path.exists('data'):
                os.makedirs('data')

            # Append data to csv file
            file_path = f'data/{category}.csv'
            file_exists = os.path.exists(file_path)
            with open(file_path, 'a', encoding='utf-8') as f:
                if not file_exists:
                    f.write('name,url,price,created_at\n')
                for product in products_data:
                    f.write(','.join(map(str, product)) + '\n')


if __name__ == "__main__":
    scrape()
