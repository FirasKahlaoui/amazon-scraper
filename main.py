import subprocess
from scraper.price_comparator import compare_prices

def main():
    # Run the Scrapy spider
    subprocess.check_output(['scrapy', 'crawl', 'amazon_product_spider'])

    # Compare prices and display changes
    price_changes = compare_prices()
    for change in price_changes:
        print(f"Product: {change['name']}\nCategory: {change['category']}\nToday's Price: {change['today_price']}\nYesterday's Price: {change['yesterday_price']}\n")

if __name__ == "__main__":
    main()