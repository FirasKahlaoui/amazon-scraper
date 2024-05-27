import scrapy
import random
from datetime import datetime

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

    def start_requests(self):
        urls = {
            'CPU': 'https://www.amazon.com/s?k=cpu',
            'RAM': 'https://www.amazon.com/s?k=ram',
            'GPU': 'https://www.amazon.com/s?k=gpu'
        }
        for category, url in urls.items():
            for page in range(1, 21):
                url = f"{url}&page={page}"
                yield scrapy.Request(url=url, callback=self.parse, cb_kwargs=dict(category=category))

    def parse(self, response, category):
        products = response.css('div[data-component-type="s-search-result"]')
        for product in products:
            title_tag = product.css('h2')
            if not title_tag:
                continue
            a_tag = title_tag.css('a')
            if not a_tag:
                continue
            title = a_tag.css('::text').get().strip()
            url = 'https://www.amazon.com' + a_tag.css('::attr(href)').get()

            price_tag = product.css('span.a-offscreen')
            if not price_tag:
                continue
            price = float(price_tag.css('::text').get().replace('$', '').replace('£', '').replace(',', ''))
            yield {
                'title': title,
                'category': category,
                'url': url,
                'price': price,
                'timestamp': str(datetime.now())
            }