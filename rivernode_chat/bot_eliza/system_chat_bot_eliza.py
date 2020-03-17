import sys
import os
import random
import time

from rivernode_chat.system_base_theaded_single import SystemBaseThreadedSingle
from rivernode_chat.bot_eliza.eliza import Eliza

class SystemChatBotEliza(SystemBaseThreadedSingle):

    def __init__(self, system_chat_server, id_user, path_file_script):
        super(SystemChatBotEliza, self).__init__()
        self.system_chat_server = system_chat_server
        self.id_user = id_user
        self.path_file_script = path_file_script
        self.dict_state = {}

    def prepare(self):
        pass
       
    def work(self):
        list_conversation = self.system_chat_server.load_list_conversation_for_id_user(self.id_user)
        list_message_send = []
        for conversation in list_conversation:
            id_conversation = conversation['id_conversation']
            if id_conversation not in self.dict_state:
                eliza = Eliza()
                eliza.load(self.path_file_script)
                self.dict_state[id_conversation] = eliza
                message = {}
                message['id_user'] = self.id_user
                message['id_conversation'] = id_conversation
                message['text'] = eliza.initial()
                list_message_send.append(message)
            else:
                if 0 < len(conversation['list_message']):
                    if not conversation['list_message'][-1]['id_user'] == self.id_user:
                        eliza =  self.dict_state[id_conversation]
                        message = {}
                        message['id_user'] = self.id_user
                        message['id_conversation'] = id_conversation
                        message['text'] = eliza.respond(conversation['list_message'][-1]['text'])
                        list_message_send.append(message)
        self.system_chat_server.save_list_message(list_message_send)
        time.sleep(1.0)
            
