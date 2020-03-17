import sys
import os

sys.path.append(os.path.abspath('../../rivernode_chat'))

from rivernode_chat.client_chat_server import ClientChatServer
from rivernode_chat.bot_list.system_chat_bot_list import SystemChatBotList

server = ClientChatServer.create_client('XXXX')

id_user = 'bot_list'
if not server.has_id_user(id_user):
    server.create_user(id_user)
print(server.load_list_id_user())
chat_bot = SystemChatBotList(server, id_user)
chat_bot.start()
chat_bot.await_stop()
# while(True):
#     print('work_user')
#     sys.stdout.flush()
#     ui_chat_console.work()


