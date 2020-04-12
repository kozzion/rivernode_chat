import sys
import os
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

sys.path.append(os.path.abspath('../../rivernode_chat'))
from rivernode_chat.interface.whatsapp.system_webcontroller_whatsapp import SystemWebcontrollerWhatsapp
from rivernode_chat.interface.whatsapp.system_chat_whatsapp import SystemChatWhatsapp

id_conversation_base = 'Myself'
id_conversation_new = 'Incident 2345'
id_user_wa_write = 'Jaap Oosterbroek'
id_user_wa_read = 'Ward van Hoof'

path_file_session = 'session.json'

executable_path = 'C:\\tools\\chromedriver\\chromedriver_80_0_3987_106.exe'

def session_reconnect(path_file_session):
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


def session_create_new(path_file_session):
    
    print('session_create_new 0')
    sys.stdout.flush()
    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=selenium") 
    driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
    print('session_create_new 1')
    sys.stdout.flush()
    session = {}
    session['url'] = driver.command_executor._url
    session['session_id'] = driver.session_id
    with open(path_file_session, 'w') as file:
        json.dump(session, file)
    return driver

def is_alive(driver):
    if driver == None:
        return False
    try:
        print(driver.title)
        return True
    except WebDriverException:
        return False



driver = session_reconnect(path_file_session)
if not is_alive(driver):
    driver = session_create_new(path_file_session)

        

controller = SystemWebcontrollerWhatsapp(driver)
chat_whatsapp = SystemChatWhatsapp(controller)
chat_whatsapp.create_conversation_group(id_conversation_new, [id_user_wa_write, id_user_wa_read])



# manual = True
# if manual:
#     input_str = ''
#     while(not input_str == 'exit'):
#         connector.work()
#         chat_bot.work()
#         input_str = input() 
# else:
#     connector.start()
#     input_str = input() 
