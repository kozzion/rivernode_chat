import sys
import os

sys.path.append(os.path.abspath('../../rivernode_chat'))

from rivernode_chat.client_chat_server import ClientChatServer
from rivernode_chat.bot_eliza.system_chat_bot_eliza import SystemChatBotEliza

server = ClientChatServer.create_client('XXXX')

id_user = 'bot_eliza'
if not server.has_id_user(id_user):
    server.create_user(id_user)
print(server.load_list_id_user())
chat_bot = SystemChatBotEliza(server, id_user, os.path.join('eliza','doctor.txt'))
chat_bot.start()
chat_bot.await_stop()