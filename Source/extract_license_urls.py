from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import re


res_dict = {}


def web_init(oss_component):
    
    url_list = []

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless') #Headless browser.
        driver = webdriver.Chrome(chrome_options=options)
    except Exception:
        raise Exception("Error loading headerless browser package (Chrome browser).")
    else:
        url = "https://www.google.com/search?ei=cFNMW7CjA8LQvgSQsICIBA&q=license+of+%s+or+%s+github"%(oss_component, oss_component) 

    driver.get(url)
    results = driver.find_elements_by_css_selector('div.g')

    for res in range(0, 3):
        link = results[res].find_element_by_tag_name("a")
        href = link.get_attribute("href")
        url_list.append(href)

    driver.quit()
    return url_list



if __name__ == "__main__":
    print(web_init("abbrev"))
