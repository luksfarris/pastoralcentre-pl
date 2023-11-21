from time import sleep
import json
from bs4 import BeautifulSoup
from splinter import Browser
from selenium.webdriver.chrome.service import Service

if __name__ == '__main__':
    url = 'https://web.archive.org/web/*/https://www.pastoralcentre.pl*'
    browser = Browser('chrome', service= Service(executable_path='/usr/local/bin/chromedriver'))
    browser.visit(url)
    # wait for initial page load, could take longer
    sleep(10)
    all_links = {}
    # we repeat the process for each page until we can't anymore
    for i in range(26):
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        table_items = soup.find_all('tr')
        for t in table_items[1:]:
            link = t.find_all('a')[0].contents[0]
            mime_type = t.contents[1].contents[0]
            all_links[link] = mime_type
        browser.find_by_text('Next').first.click()
        sleep(0.5)
    print(f'Found {len(all_links)} links')
    with open('all_pages.json', 'w') as f:
        json.dump(all_links, f, indent=4)
