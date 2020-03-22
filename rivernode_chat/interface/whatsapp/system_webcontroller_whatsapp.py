import sys
import os
import json
import time
import datetime

# from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

    def await_loaded(self):
        while(not self.is_loaded()):
            print('not loaded')
            sys.stdout.flush()
            time.sleep(0.5)
        print('loaded')
        sys.stdout.flush()
        time.sleep(0.5)


    def get_list_message_recent_for_id_conversation(self, id_conversation):
        if not self.get_id_conversation_selected() == id_conversation:
            self.select_searched_conversation(id_conversation)
        return self.get_list_message_recent()

    def get_list_message_recent(self):
        # hasclass copyable-text
        list_element_message = []
        list_element = self.driver.find_elements(By.TAG_NAME,  "div")
        for element in list_element:
            try:
                if 'message-out' in element.get_attribute('class'):
                    list_element_message.append(element)
            except Exception:
                pass
            try:
                if 'message-in' in element.get_attribute('class'):
                    list_element_message.append(element)
            except Exception:
                pass
        # print('list_element_message')
        # print(len(list_element_message))

                # list_child_element = element.find_elements_by_xpath(".//*")
                # print(len(list_child_element))
                # if len(list_child_element) == 1:
                #     print(list_child_element[0].get_text())        
        list_message = []
        for element_message in list_element_message:
            try:
                list_message.append(self.parse_element_message(element_message))
            except Exception:
                print('parse failed')
        return list_message

    def parse_element_message(self, element_message):
        id_user = None
        timestamp_message = None
        text = None

        list_element = element_message.find_elements(By.TAG_NAME,  "div")
        for element in list_element:
            if 'copyable-text' in element.get_attribute('class'):
                id_user = element.get_attribute('data-pre-plain-text').split(']')[1][1:-2]
                str_datetime = element.get_attribute('data-pre-plain-text').split(']')[0][1:]
                datetime_message = datetime.datetime.strptime(str_datetime, '%H:%M, %m/%d/%Y')
                timestamp_message = int(datetime.datetime.timestamp(datetime_message))
                break

        list_element = element_message.find_elements(By.TAG_NAME,  "span")
        for element in list_element:
            if 'copyable-text' in element.get_attribute('class'):
                element_child = element.find_elements_by_xpath(".//*")[0]
                text = element_child.get_attribute("innerHTML")
                break
        if not id_user:
            print('no user')
            raise RuntimeError('no user')
        if not text:
            print('no text')
            raise RuntimeError('no text')

        message = {}
        message['id_user'] = id_user
        message['timestamp'] = timestamp_message
        message['text'] = text
        return message

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
                    print('selected_conversation:')
                    print(attribute)                
                    return attribute

        print('title not found')
        return '' 

    def select_searched_conversation(self, name_conversation):
        search_box = self.get_element_search_box()
        search_box.clear()
        search_box.send_keys(name_conversation)
        time.sleep(0.5)
        self.select_present_conversation(name_conversation)

    def select_present_conversation(self, name_conversation):
        list_element = self.find_elements_by_title(name_conversation)
        if not len(list_element) == 1:
            raise RuntimeError()
        element = list_element[0]
        element.click()
        time.sleep(1) #TODO await selection
        self.name_conversation = name_conversation    

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

    def send_list_message(self, id_conversation, list_text):
        if not self.get_id_conversation_selected() == id_conversation:
            self.select_searched_conversation(id_conversation)
        for text in list_text:
            self.send_selected_user(text)
        
    def send_selected_user(self, text):

        
        input_box = self.get_element_send_box()
        time.sleep(1)
        # Send message
        # taeget is your target Name and msgToSend is you message
        # input_box.send_keys("Hello, " + target + "."+ Keys.SHIFT + Keys.ENTER + text) # + Keys.ENTER (Uncomment it if your msg doesnt contain '\n')
        input_box.send_keys(text) # + Keys.ENTER (Uncomment it if your msg doesnt contain '\n')
        # Link Preview Time, Reduce this time, if internet connection is Good
        time.sleep(3)
        input_box.send_keys(Keys.ENTER)


    def find_elements_by_title(self, title):
        # driver.find_element_by_xpath(
        return self.driver.find_elements(By.XPATH, '//*[@title="' + title + '"]')
