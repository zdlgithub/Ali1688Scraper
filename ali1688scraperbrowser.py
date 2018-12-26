"""
title:Get a web page html by webdriver of firefox or chrome
date:2018-11-12
author:doug zhnag
description:

"""

import settings
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class ScraperBrowser(object):

    @property
    def web_page_url(self):
        return self.__web_page_url

    @web_page_url.setter
    def web_page_url(self , value):
        self.__web_page_url = value

    def __init__(self):
        self.__base_dir_driver = settings.LIBRARY_BASE_PATH
        self.__scraper_sleep_time = settings.SCRAPER_SLEEP_TIME
        self.__web_page_url = None
        self.__browser=None
        if settings.BASE_BROWSER == settings.Browser.CHROME:
            self.__get_browser_by_chrome()
        elif settings.BASE_BROWSER == settings.Browser.FIREFOX:
            self.__get_browser_by_firefox()

    def __get_browser_by_firefox(self):
        options=webdriver.FirefoxOptions()
        options.headless= settings.browser_handless_default
        self.__browser=webdriver.Firefox(options=options,executable_path=os.path.join(self.__base_dir_driver
                                                                                      , 'geckodriver.exe'))

    def __get_browser_by_chrome(self):
        options = webdriver.ChromeOptions()
        options.headless = settings.browser_handless_default
        options.add_argument('--start-maximized')
        # options.add_argument('--disable-gpu')
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,
                # 'javascript': 1,
                # 'geolocation': 1
            }
        }
        options.add_experimental_option('prefs', prefs)
        self.__browser = webdriver.Chrome(options=options,executable_path=os.path.join(self.__base_dir_driver
                                                                                       , 'chromedriver.exe'))

    def get_html_text(self):
        self.__browser.get(self.__web_page_url)
        print('url:',self.__web_page_url)

        # ahref = self.__browser.find_element_by_link_text('Product Details')
        # ahref.send_keys(Keys.TAB)
        #
        # i = 0
        # # 判断内容是否在加载中
        # while i < 10:
        #     i += 1
        #     ahref.send_keys(Keys.ARROW_DOWN)
        #     print('down1')
        #     ahref.send_keys(Keys.ARROW_DOWN)
        #     print('down2')
        #     print('while sleep:', self.__scraper_sleep_time)
        #     time.sleep(self.__scraper_sleep_time)
        #     try:
        #         loading32 = self.__browser.find_element_by_css_selector('.product-description-main .loading32')
        #         # self.__browser.execute_script('window.scrollTo(100, document.getElementsByClassName("product-description-main")[0].offsetTop);')
        #         print('loading32:', loading32)
        #     except:
        #         print('not loading32')
        #         break;

        return self.__browser.page_source

    def __del__(self):
        if self.__browser:
            self.__browser.quit()
            self.__browser = None
