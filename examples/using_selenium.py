# coding=utf-8

from selenium import webdriver

from serlist.scraper import SerpScraper

chrome_options = webdriver.ChromeOptions()
prefs = {
    'profile.managed_default_content_settings.images': 2,
    'profile.managed_default_content_settings.javascript': 2,
    'profile.default_content_setting_values.cookies': 2,
}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.set_page_load_timeout(20)
driver.get('https://www.sogou.com/web?query=Tom+Hanks')
text = driver.page_source
driver.quit()
results = SerpScraper().scrape(text)
for r in results:
    print(r)
