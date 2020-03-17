import sys
import os

sys.path.append(os.path.abspath('../../rivernode_chat'))

from rivernode_chat.system_chat_server import SystemChatServer

from rivernode_chat.bot_list.system_chat_bot_list import SystemChatBotList
from rivernode_chat.ui_chat_console import UIChatConsole
from rivernode_chat.ui_chat_tk import UIChatTK

server = SystemChatServer()
id_user_a = 'jaap'
id_user_b = 'bot'
id_conversation = 'jaap_bot_0'

if not server.has_id_user(id_user_a):
    server.create_user(id_user_a)
if not server.has_id_user(id_user_b):
    server.create_user(id_user_b)
if not server.has_id_conversation(id_conversation):
    server.create_conversation(id_conversation, [id_user_a, id_user_b])

chat_bot = SystemChatBotList(server, id_user_b)
chat_bot.start()

ui_chat = UIChatConsole(server, id_user_a, id_conversation)
ui_chat = UIChatTK(server, id_user_a, id_conversation)

ui_chat.start()
ui_chat.show()