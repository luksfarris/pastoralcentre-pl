import json
from time import sleep
from bs4 import BeautifulSoup

from splinter import Browser
from selenium.webdriver.chrome.service import Service
import requests

# UNDESIRED_MIME_TYPES = ['application/rss+xml', 'application/javascript', 'application/json', 'application/mp3',
#                         'application/vnd.ms-fontobject', 'text/plain', 'text/javascript', 'image/vnd.microsoft.icon',
#                         'image/svg+xml', 'text/calendar', 'text/css']

IMAGE_TYPES = ['image/jpeg', 'image/gif', 'image/png', 'image/bmp']


if __name__ == '__main__':
    browser = Browser('chrome', service=Service(executable_path='/usr/local/bin/chromedriver'))
    with open('all_pages.json') as f:
        urls = json.load(f)

    image_urls = sorted([k for k, v in urls.items() if v in IMAGE_TYPES])
    print(f"Found {len(image_urls)} image urls to process")
    for i in range(len(image_urls)):
        url = f"https://web.archive.org/web/*/{image_urls[i]}*"
        browser.visit(url)
        sleep(10)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        table_items = soup.find_all('tr')
        latest_backup = table_items[1]
        link = latest_backup.find_all('a')[0].get('href').replace('*', '')
        browser.visit(f'https://web.archive.org{link}')
        sleep(10)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        if soup.find_all('iframe'):
            image_link = soup.find_all('iframe')[0].get('src')
        elif soup.find_all('img'):
            image_link = soup.find_all('img')[0].get('src')
        else:
            image_link = None
        if not image_link:
            print(f"Could not find image link for {image_urls[i]}")
            continue
        img_data = requests.get(image_link).content
        image_name = image_link.split('/')[-1]
        with open(f'img/{image_name}', 'wb') as handler:
            handler.write(img_data)
        print(f"Downloaded {image_name} with index {i}")
