import sys
import os
import json
import time
import datetime

# from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class DOMLocatorWhatsapp(object):


    @staticmethod 
    def get_message_box(driver):
        return driver.find_element(By.CSS_SELECTOR, '*[tabindex="-1"]')


    @staticmethod 
    def get_selected_list_message(driver):
        print('get_selected_list_message 0')
        sys.stdout.flush()
        message_box = DOMLocatorWhatsapp.get_message_box(driver)
        # list_element = message_box.find_elements(By.TAG_NAME,  "div")

        # By byXpath = By.xpath("//input[(@id='id_Start') and (@class = 'blabla')]")
        # list_element = message_box.find_elements(By.XPATH, "//input[@class='message-out' or @type='div']")
        list_element_message = message_box.find_elements(By.XPATH, "//div[contains(@class, 'message-out') or contains(@class, 'message-in')]")
        print('get_selected_list_message 1')
        print(len(list_element_message))
        sys.stdout.flush()
        return list_element_message

    # @staticmethod 
    # def get_selected_list_message(driver):
    #     list_element_message = []
    #     list_element = driver.find_elements(By.TAG_NAME,  "div")
    #     for element in list_element:
    #         try:
    #             if 'message-out' in element.get_attribute('class'):
    #                 list_element_message.append(element)
    #         except Exception:
    #             pass
    #         try:
    #             if 'message-in' in element.get_attribute('class'):
    #                 list_element_message.append(element)
    #         except Exception:
    #             pass
    #     return list_element_message