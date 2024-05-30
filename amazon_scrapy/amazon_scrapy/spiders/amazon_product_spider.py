import scrapy
import random
from datetime import datetime
import sqlite3


class AmazonProductSpider(scrapy.Spider):
    name = 'amazon_product_spider'
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
        # Add more user agents as needed
    ]
    custom_settings = {
        'USER_AGENT': random.choice(USER_AGENTS)
    }

    def __init__(self):
        self.conn = sqlite3.connect(
            'C:/Users/Kahla/amazon_scraper_project/db/amazon_prices.db')
        self.cursor = self.conn.cursor()

    def start_requests(self):
        urls = {
            'CPU': ('https://www.amazon.com/s?k=cpu', 20),
            'RAM': ('https://www.amazon.com/s?k=ram', 20),
            'GPU': ('https://www.amazon.com/s?k=gpu', 20),
            'Laptop': ('https://www.amazon.com/s?k=laptop', 20),
            'Smartphone': ('https://www.amazon.com/s?k=smartphone', 20),
            'Smartwatch': ('https://www.amazon.com/s?k=smartwatch', 20),
            'parfum': ('https://www.amazon.fr/b?node=2805688031&ref=lp_210965031_nr_n_2', 98),
            'solaire': ('https://www.amazon.fr/gp/browse.html?rw_useCurrentProtocol=1&node=2953222031&ref_=beauty_leftnav_produitsbronzantssolaires', 15),
            'coffres': ('https://www.amazon.fr/b?node=211031031&ref=lp_211020031_nr_n_0', 17)
        }

        for category, (base_url, num_pages) in urls.items():
            for page in range(1, num_pages + 1):
                url = f"{base_url}&page={page}"
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(category=category))

    def parse(self, response, category):
        products = response.css('div[data-component-type="s-search-result"]')
        for product in products:
            title_tag = product.css('h2')
            a_tag = title_tag.css('a') if title_tag else None
            title = a_tag.css('::text').get().strip() if a_tag else 'NaN'
            url = 'https://www.amazon.com' + \
                a_tag.css('::attr(href)').get() if a_tag else 'NaN'

            price_tag = product.css('span.a-offscreen')
            price = price_tag.css('::text').get() if price_tag else 'NaN'

            # Skip if price is 'NaN'
            if price == 'NaN':
                continue

            self.save_to_db(title, category, url, price)

    def save_to_db(self, title, category, url, price):
        self.cursor.execute("""
            INSERT INTO products (name, category, url, price, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (title, category, url, price, str(datetime.now().date())))
        self.conn.commit()

    def close(self, reason):
        self.conn.close()
