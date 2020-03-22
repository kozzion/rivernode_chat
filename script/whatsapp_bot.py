import sys
import os
import json

# Can save contact with their phone Number

# Import required packages
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import time
import pickle

sys.path.append(os.path.abspath('../../rivernode_chat'))
from rivernode_chat.interface.whatsapp.system_webcontroller_whatsapp import SystemWebcontrollerWhatsapp
from rivernode_chat.interface.whatsapp.system_connector_whatsapp import SystemConnectorWhatsapp
# from rivernode_chat.client_chat_server import ClientChatServer
from rivernode_chat.system_chat_server import SystemChatServer
# from rivernode_chat.bot_list.system_chat_bot_list import SystemChatBotList
from rivernode_chat.bot_eliza.system_chat_bot_eliza import SystemChatBotEliza

id_conversation_wa = 'Jaap Jori Eliza'
id_user_wa_read = 'Jori Huisman'
# id_conversation_wa = 'Myself'
# id_user_wa_read = 'Jaap Oosterbroek'

id_connection = 'myself_to_bot_list'
id_conversation_cs = 'myself_cs_to_bot_list_cs'
id_user_cs_write = 'myself_cs'
id_user_cs_read = 'bot_list_cs'

# server = ClientChatServer.create_client('XXXX')
server = SystemChatServer()

if not server.has_id_user(id_user_cs_write):
    server.create_user(id_user_cs_write)
if not server.has_id_user(id_user_cs_read):
    server.create_user(id_user_cs_read)
if not server.has_id_conversation(id_conversation_cs):
    server.create_conversation(id_conversation_cs, [id_user_cs_write, id_user_cs_read])

chat_bot = SystemChatBotEliza(server, id_user_cs_read, os.path.join('eliza','doctor.txt'))
# chat_bot = SystemChatBotList(server, id_user_cs_read)
chat_bot.start()

executable_path = 'C:\\tools\\chromedriver\\chromedriver_80_0_3987_106.exe'
chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium") 
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.get("https://web.whatsapp.com/") #TODO check and move to controller

controller = SystemWebcontrollerWhatsapp(driver)
connector = SystemConnectorWhatsapp(controller, server)

connector.add_connection(id_connection, id_conversation_wa, id_user_wa_read, id_conversation_cs, id_user_cs_write, id_user_cs_read)
while(True):
    connector.work()
