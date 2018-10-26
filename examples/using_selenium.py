# coding=utf-8

from selenium import webdriver

from serlist.scraper import SerpScraper

chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(10)
driver.get('https://www.sogou.com/web?query=Tom+Hanks')
text = driver.page_source
driver.quit()
results = SerpScraper().scrap(text)
for r in results:
    print(r)
