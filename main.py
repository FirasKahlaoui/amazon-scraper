import os
import subprocess
from scraper.price_comparator import compare_prices


def main():

    # Change the current working directory
    os.chdir('amazon_scrapy')

    # Run the Scrapy spider
    result = subprocess.run(
        ['scrapy', 'crawl', 'amazon_product_spider'], capture_output=True, text=True)

    # Compare prices and display changes
    price_changes = compare_prices()
    for change in price_changes:
        print(
            f"Product: {change['name']}\nCategory: {change['category']}\nToday's Price: {change['today_price']}\nYesterday's Price: {change['yesterday_price']}\n")


if __name__ == '__main__':
    main()
