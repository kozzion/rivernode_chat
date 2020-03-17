import sys
import os

sys.path.append(os.path.abspath('../../rivernode_chat'))

from rivernode_chat.system_chat_server import SystemChatServer
from rivernode_chat.ui_chat_console import UIChatConsole
from rivernode_chat.system_chat_bot import SystemChatBot


server = SystemChatServer()
id_user_a = 'jaap'
id_user_b = 'bot'
id_conversation = 'jaap_bot_0'
server.create_user(id_user_a)
server.create_user(id_user_b)
server.create_conversation(id_conversation, [id_user_a, id_user_b])

chat_bot = SystemChatBot(server, id_user_b, id_conversation)
chat_bot.start()

ui_chat_console = UIChatConsole(server, id_user_a, id_conversation)
ui_chat_console.run()
# while(True):
#     print('work_user')
#     sys.stdout.flush()
#     ui_chat_console.work()


