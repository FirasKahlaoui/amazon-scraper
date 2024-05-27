import requests
from bs4 import BeautifulSoup
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
    # Add more user agents as needed
]

def scrape_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    proxies = []
    
    for row in soup.find('tbody').find_all('tr'):
        cols = row.find_all('td')
        if cols[6].text.strip() == 'yes':  # Only HTTPS proxies
            proxies.append(f"{cols[0].text.strip()}:{cols[1].text.strip()}")
    
    return proxies

def verify_proxy(proxy):
    url = 'https://www.amazon.com/s?k=cpu'
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }
    try:
        response = requests.get(url, headers=headers, proxies={'http': f'http://{proxy}', 'https': f'https://{proxy}'}, timeout=5)
        if response.status_code == 200:
            return True
    except:
        return False

def get_working_proxies(proxies):
    working_proxies = []
    for proxy in proxies:
        if verify_proxy(proxy):
            working_proxies.append(proxy)
            print(f"Working proxy: {proxy}")
        else:
            print(f"Failed proxy: {proxy}")
        time.sleep(1)  # Delay to prevent getting blocked
    return working_proxies

def save_proxies(proxies, file_path):
    with open(file_path, 'w') as file:
        for proxy in proxies:
            file.write(proxy + '\n')

def load_proxies(file_path):
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            proxies.append(line.strip())
    return proxies

if __name__ == "__main__":
    proxies = scrape_proxies()
    working_proxies = get_working_proxies(proxies)
    save_proxies(working_proxies, 'working_proxies.txt')
    loaded_proxies = load_proxies('working_proxies.txt')
    print(f"Loaded proxies: {loaded_proxies}")
