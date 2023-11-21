import json
import pathlib
from time import sleep

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from splinter import Browser

PAGE_TYPES = ['text/html']
EXCLUDED_PAGES = ['gravatar.com', 'cgi-sys', 'ajax.php', 'robots.txt', 'pastoralcentre.pl/?p=']

if __name__ == '__main__':
    browser = Browser('chrome', service=Service(executable_path='/usr/local/bin/chromedriver'))
    with open('all_pages.json') as f:
        urls = json.load(f)

    page_urls = sorted([k for k, v in urls.items() if v in PAGE_TYPES])
    for exclude in EXCLUDED_PAGES:
        page_urls = [url for url in page_urls if exclude not in url]
    print(f"Found {len(page_urls)} pages to process")
    for i in range(272, len(page_urls)):
        url = f"https://web.archive.org/web/*/{page_urls[i]}"
        url += '*' if url.endswith('/') else '/*'
        browser.visit(url)
        link = None
        while not link:
            html = browser.html
            if browser.find_by_text('Wayback Machine has not archived that URL.'):
                break
            soup = BeautifulSoup(html, "html.parser")
            table_items = soup.find_all('tr')
            if not table_items:
                sleep(2)
                continue
            rows = [t.find('a') for t in table_items if t.find('a') is not None]
            links = [r.get('href') for r in rows if r.get('href').endswith(page_urls[i])]
            if links:
                link = links[0].replace('*', '')
            else:
                sleep(2)
        if not link:
            print(f"No backup found at index {i}, probably a 301 redirect")
            continue

        article_name = [s for s in link.split('/') if s][-1] + '.html'
        if pathlib.Path(f"articles/{article_name}").exists():
            print(f"Article {article_name} already exists, skipping")
            continue
        browser.visit(f'https://web.archive.org{link}')
        # sleep(10)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        # article = soup.find_all('div', {"class": "post-content"}) or soup.find_all('div', {"class": "pf-content"})
        article = soup.find_all('article')
        if article:
            article_source = article[0]
            article_images = article_source.find_all('img')
            for image_source in article_images:
                if 'src' in image_source:
                    image_source['src'] = '../img/' + image_source['src'].split('/')[-1]
            with open(f"articles/{article_name}", "w") as text_file:
                text_file.write(str(article_source))
        print(f"Processed page {article_name} with index {i}")
