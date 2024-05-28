from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess

def run_spider():
    subprocess.check_output(['scrapy', 'crawl', 'amazon_product_spider'])

scheduler = BlockingScheduler()
scheduler.add_job(run_spider, 'interval', days=1)
scheduler.start()