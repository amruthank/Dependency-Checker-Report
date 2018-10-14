from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import re



class SeleniumDriver:

    def __init__(self):
        self.browser = self.open_browser()
        

    def open_browser(self):
        #TODO: raise exceptions on newtwork issues
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless') #Headless browser.
            return webdriver.Chrome(chrome_options=options)
        except ImportError:
            raise Exception("Error loading the package selenium!!\t Please install the package.\n")
        except Exception:
            raise Exception("Error loading headerless browser package (Chrome browser).")


    def get_urls(self, oss_component):

        result_dict = {}

        result_dict["%s"%oss_component] = []
        
        url = "https://www.google.com/search?ei=cFNMW7CjA8LQvgSQsICIBA&q=license+of+%s+or+%s+github"%(oss_component, oss_component)

        try:
            self.browser.get(url)
        except Exception as e:
            print(e)
        driver_sub_element = self.browser.find_elements_by_css_selector('div.g')

        for res in range(0, 2):
            try:
                link = driver_sub_element[res].find_element_by_tag_name("a")
            except Exception:
                continue
            else:
                result_dict["%s"%oss_component].append(link.get_attribute("href"))

        return result_dict
    
            
    def close_browser(self):
        self.browser.quit()




if __name__ == "__main__":

    data = ["abbrev", "jquery", "angularjs"]
    automation = SeleniumDriver()
    print(automation)
    for d in data:
        print(automation.get_urls(d))
    automation.close_browser()
    
