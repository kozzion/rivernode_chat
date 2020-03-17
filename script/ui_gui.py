import sys
import os

sys.path.append(os.path.abspath('../../rivernode_chat'))

from rivernode_chat.client_chat_server import ClientChatServer
from rivernode_chat.ui_chat_tk import UIChatTK

server = ClientChatServer.create_client('XXXX')


id_user_gui = 'jaap'
# id_user_bot = 'bot_list'
# id_user_bot = 'bot_eliza'
id_user_bot = 'bot_keras_option'

id_conversation = id_user_gui + '_' + id_user_bot

if not server.has_id_user(id_user_bot):
    raise RuntimeError('No such bot')

if not server.has_id_user(id_user_gui):
    server.create_user(id_user_gui)
if not server.has_id_conversation(id_conversation):
    server.create_conversation(id_conversation, [id_user_gui, id_user_bot])

ui_chat = UIChatTK(server, id_user_gui, id_conversation)
ui_chat.start()
ui_chat.show()