import sys
import os
import json

# Can save contact with their phone Number

# Import required packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#

from selenium.common.exceptions import WebDriverException
# import httplib
# import socket


sys.path.append(os.path.abspath('../../rivernode_chat'))
from rivernode_chat.interface.whatsapp.system_webcontroller_whatsapp import SystemWebcontrollerWhatsapp
from rivernode_chat.interface.whatsapp.system_connector_whatsapp import SystemConnectorWhatsapp
# from rivernode_chat.client_chat_server import ClientChatServer
from rivernode_chat.system_chat_server import SystemChatServer
# from rivernode_chat.bot_list.system_chat_bot_list import SystemChatBotList
# from rivernode_chat.bot_eliza.system_chat_bot_eliza import SystemChatBotEliza
from rivernode_chat.bot_meta.system_chat_bot_meta import SystemChatBotMeta


# id_conversation_wa = 'Jaap Pieter Eliza'
# id_user_wa_write = 'Jaap Oosterbroek'
# id_user_wa_read = 'Pieter Oosterbroek'
# id_connection = 'myself_to_bot_list'
# id_conversation_cs = 'myself_cs_to_bot_list_cs'
# id_user_cs_write = 'myself_cs'
# id_user_cs_read = 'bot_list_cs'
# path_file_session = 'session.json'

# id_conversation_wa = 'Jaap Jori Eliza'
# id_user_wa_write = 'Jaap Oosterbroek'
# id_user_wa_read = 'Jori Huisman'
# id_connection = 'myself_to_bot_list'
# id_conversation_cs = 'myself_cs_to_bot_list_cs'
# id_user_cs_write = 'myself_cs'
# id_user_cs_read = 'bot_list_cs'
# path_file_session = 'session.json'

id_conversation_wa = 'Myself'
id_user_wa_write = 'Jaap Oosterbroek'
id_user_wa_read = 'Jaap Oosterbroek'
id_connection = 'myself_to_bot_list'
id_conversation_cs = 'myself_cs_to_bot_list_cs'
id_user_cs_write = 'myself_cs'
id_user_cs_read = 'bot_list_cs'
path_file_session = 'session.json'

# id_conversation_wa = 'Ward van Hoof'
# id_user_wa_write = 'Jaap Oosterbroek'
# id_user_wa_read = 'Ward van Hoof'
# id_connection = 'myself_to_bot_list'
# id_conversation_cs = 'myself_cs_to_bot_list_cs'
# id_user_cs_write = 'myself_cs'
# id_user_cs_read = 'bot_list_cs'
# path_file_session = 'session.json'

# server = ClientChatServer.create_client('XXXX')
server = SystemChatServer()

if not server.has_id_user(id_user_cs_write):
    server.create_user(id_user_cs_write)
if not server.has_id_user(id_user_cs_read):
    server.create_user(id_user_cs_read)
if not server.has_id_conversation(id_conversation_cs):
    server.create_conversation(id_conversation_cs, [id_user_cs_write, id_user_cs_read])

chat_bot = SystemChatBotMeta(server, id_user_cs_read)

# chat_bot = SystemChatBotList(server, id_user_cs_read)

# chat_bot.start()

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
connector = SystemConnectorWhatsapp(controller, server)

connector.add_connection(id_connection, id_conversation_wa, id_user_wa_write, id_user_wa_read, id_conversation_cs, id_user_cs_write, id_user_cs_read)

manual = True
if manual:
    input_str = ''
    while(not input_str == 'exit'):
        connector.work()
        chat_bot.work()
        input_str = input() 
else:
    connector.start()
    input_str = input() 
