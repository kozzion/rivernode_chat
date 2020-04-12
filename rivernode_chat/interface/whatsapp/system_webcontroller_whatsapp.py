import sys
import os
import json
import time
import datetime
from bs4 import BeautifulSoup

# from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from rivernode_chat.interface.whatsapp.helper_message import HelperMessage as dl

class SystemWebcontrollerWhatsapp(object):

    def __init__(self, driver:WebDriver):
        super(SystemWebcontrollerWhatsapp, self).__init__()
        self.driver = driver
        self.state = {}

  
    def save(self, path_file):
        with open(path_file, 'w') as file:
            json.dump(self.state, file)


    def load(self, path_file):
        with open(path_file, 'r') as file:
            self.state = json.load(file)

    def prepare(self):
        pass

    def work(self):
        pass

    def is_loaded(self):
        return 0 < len(self.driver.find_elements(By.TAG_NAME, 'header' ))

    
    def load_whatsapp(self):
        # if self.driver
        if not self.driver.current_url == 'https://web.whatsapp.com/':
            self.driver.get("https://web.whatsapp.com/") #TODO check and move to controller

    def await_load_whatsapp(self):
        while(not self.is_loaded()):
            # print('not loaded')
            # print(self.driver.current_url)
            sys.stdout.flush()
            time.sleep(0.1)

    def reset_to_base(self):
        list_element_cancel = self.driver.find_elements(By.XPATH, '//span[@data-icon="x-alt"]')
        if len(list_element_cancel) == 1:
            list_element_cancel[0].click()
            time.sleep(0.5)

    def create_conversation_group(self, id_conversation, list_id_user):
        
        # <div class="_2fq0t V42si copyable-area" style="transform: translateX(0%);">
        element_side = self.driver.find_element_by_id('side')
        element_icon = element_side.find_element(By.XPATH,  "//div[@title='New chat']")
        element_icon.click()
        time.sleep(0.2)
        element_group = element_side.find_element(By.XPATH,  "//span[@data-icon='new-group']").find_element(By.XPATH, './../../../..')
        element_group.click()
        time.sleep(0.2)
        element_search_contact = self.get_element_search_contact()
        for id_user in list_id_user:
            element_search_contact.clear()
            element_search_contact.send_keys(id_user)
            time.sleep(0.2)
            element_user = element_side.find_element(By.XPATH,  "//span[@title='" + id_user + "']")
            element_user.click()
            time.sleep(0.2)        
        element_forward = element_side.find_element(By.XPATH,  "//span[@data-icon='forward-light']")
        element_forward.click()
        time.sleep(0.2)

        element_group_subject = element_side.find_element(By.XPATH,  "//div[@contenteditable='true']")
        element_group_subject.send_keys(id_conversation)
        time.sleep(0.2)
        element_forward = element_side.find_element(By.XPATH,  "//span[@data-icon='checkmark-light']")
        element_forward.click()
        time.sleep(0.2)

    def get_list_message_recent_for_id_conversation(self, id_conversation, id_user_write, id_user_read):
        # print('get_list_message_recent_for_id_conversation 0')
        # sys.stdout.flush()
        if not self.get_id_conversation_selected() == id_conversation:
            # print('get_list_message_recent_for_id_conversation 1')
            # sys.stdout.flush()
            self.select_searched_conversation(id_conversation)
        # print('get_list_message_recent_for_id_conversation 2')
        # sys.stdout.flush()
        return dl.get_list_message_recent(self.driver, id_user_write, id_user_read)


    def get_id_conversation_selected(self):
        list_div_main = self.driver.find_elements_by_id('main')
        if len(list_div_main) == 0:
            print('main not found')
            return ''            
        list_element = list_div_main[0].find_elements(By.TAG_NAME, "span")
        for element in list_element:
            if element.get_attribute('title'):
                if element.get_attribute('title') == element.get_attribute("innerHTML"):
                    attribute = element.get_attribute('title')
                    # print('selected_conversation:')
                    # print(attribute)                
                    return attribute

        print('title not found')
        return '' 


    def select_searched_conversation(self, id_conversation):
        self.reset_to_base()

        search_box = self.get_element_search_box()
        search_box.clear()
        search_box.send_keys(id_conversation)
        time.sleep(1.0)
        self.select_present_conversation(id_conversation)




    def select_present_conversation(self, id_conversation):
        list_element_side = self.driver.find_elements_by_id('side')
        # print(len(list_element_side))
        element_side = list_element_side[0]
        # print(element_side.get_attribute('innerHTML'))


        # list_element = element_side.dir="auto"
        list_element = element_side.find_elements(By.XPATH, '//span[@title="' + id_conversation + '"]')
        # list_element = self.driver.find_elements(By.XPATH, '//*[@title="' + id_conversation + '"]')
        
        if len(list_element) == 0:
            raise RuntimeError('no element span with title: ' + id_conversation)
        # if 1 < len(list_element):
        #     print(len(list_element))
        #     for element in list_element:
        #         print(element.get_attribute('innerHTML'))
        #     raise RuntimeError('to many elements')
        element = list_element[0]
        element.click()
        time.sleep(1) #TODO await selection
        # self.id_conversation = id_conversation   

    def get_element_send_box(self):
        list_element = self.driver.find_elements(By.XPATH,  "//div[@contenteditable='true']")
        for element in list_element:
            if element.get_attribute('data-tab') == '1':
                return element
        raise RuntimeError()

    def get_element_search_box(self):
        list_element = self.driver.find_elements(By.XPATH,  "//div[@contenteditable='true']")
        for element in list_element:
            if element.get_attribute('data-tab') == '3':
                return element
        raise RuntimeError()


    def get_element_search_contact(self):
        return self.driver.find_element(By.XPATH,  "//input[@placeholder='Type contact name']")


    def send_list_message(self, id_conversation, list_text):
        if not self.get_id_conversation_selected() == id_conversation:
            self.select_searched_conversation(id_conversation)
        for text in list_text:
            self.send_selected_user(text)


    def send_for_id_conversation(self, id_conversation, text):  
        self.select_searched_conversation(id_conversation)
        self.send_selected_user(text)

    def send_selected_user(self, text):
        input_box = self.get_element_send_box()
        input_box.clear()
        input_box.send_keys(text) # + Keys.ENTER (Uncomment it if your msg doesnt contain '\n')
        
        index = 0
        while not( input_box.get_attribute('innerHTML') == text) or (index == 10):
            sys.stdout.flush()
            time.sleep(0.1)

        input_box.send_keys(Keys.ENTER)
        #TODO for more speedup webdriver.executeScript("document.getElementById('elementID').setAttribute('value', 'new value for element')");


    def find_elements_by_title(self, title):
        # driver.find_element_by_xpath(
        return self.driver.find_elements(By.XPATH, '//*[@title="' + title + '"]')
