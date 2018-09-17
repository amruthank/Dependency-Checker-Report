from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import re


res_dict = {}


def _get_driver():
    
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('headless') #Headless browser.
        driver = webdriver.Chrome(chrome_options=options)
    except ImportError:
        raise Exception("Error loading the package selenium!!\t Please install the package.\n")
    except Exception:
        raise Exception("Error loading headerless browser package (Chrome browser).")
    else:
        return driver


def web_init(oss_component):

    result_dict = {}
    result_dict["%s"%oss_component] = []
    
    url = "https://www.google.com/search?ei=cFNMW7CjA8LQvgSQsICIBA&q=license+of+%s+or+%s+github"%(oss_component, oss_component)

    driver = _get_driver()
    try:
        driver.get(url)
    except Exception as e:
        print(e)
    driver_sub_element = driver.find_elements_by_css_selector('div.g')

    for res in range(0, 3):
        link = driver_sub_element[res].find_element_by_tag_name("a")
        href = link.get_attribute("href")
        result_dict["%s"%oss_component].append(href)

    driver.quit()
    
    return result_dict


if __name__ == "__main__":
    print(web_init("abbrev"))
