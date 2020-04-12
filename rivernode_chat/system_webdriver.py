import sys
import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

class SystemWebdriver(object):

    def __init__(self, path_file_executable):
        super(SystemWebdriver, self).__init__()
        self.path_file_executable = path_file_executable
        self.state = {}

    def save(self):
        pass

    def load(self):
        pass

    def add_webdriver(self, name, path_dir_folder):
        pass
   

    def session_reconnect(self, path_file_session):
        try:
            with open(path_file_session, 'r') as file:
                session = json.load(file)
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            driver = webdriver.Remote(command_executor=session['url'], desired_capabilities={}, options=chrome_options) # this opens a new windw
            driver.session_id = session['session_id']
            return driver
        except Exception:
            return None


    def session_create_new(self, path_file_session, path_dir_userdata):
        chrome_options = Options()
        chrome_options.add_argument("user-data-dir=" + path_dir_userdata) 
        driver = webdriver.Chrome(executable_path=self.path_file_executable, chrome_options=chrome_options)
        session = {}
        session['url'] = driver.command_executor._url
        session['session_id'] = driver.session_id
        with open(path_file_session, 'w') as file:
            json.dump(session, file)
        return driver

    def is_alive(self, driver):
        if driver == None:
            return False
        try:
            print(driver.title)
            return True
        except WebDriverException:
            return False


    def get_webdriver(self, path_file_session, path_dir_userdata):
        driver = self.session_reconnect(path_file_session)
        if not self.is_alive(driver):
            driver = self.session_create_new(path_file_session, path_dir_userdata)
        return driver