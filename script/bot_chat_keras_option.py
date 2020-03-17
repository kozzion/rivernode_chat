import sys
import os
import json
import pickle

sys.path.append(os.path.abspath('../../rivernode_chat'))

from rivernode_chat.client_chat_server import ClientChatServer
from rivernode_chat.bot_keras_option.system_chat_bot_keras_option import SystemChatBotKerasOption

server = ClientChatServer.create_client('XXXX')

id_user = 'bot_keras_option'
if not server.has_id_user(id_user):
    server.create_user(id_user)

chat_bot = SystemChatBotKerasOption(server, id_user, os.path.join('keras_option','model.h5'), os.path.join('keras_option','context.json'))
# chat_bot.prepare()
# chat_bot.work()
chat_bot.start()
chat_bot.await_stop()