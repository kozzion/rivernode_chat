import sys
import os
import random
import time

from rivernode_chat.system_base_theaded_single import SystemBaseThreadedSingle
class SystemChatBotList(SystemBaseThreadedSingle):

    def __init__(self, system_chat_server, id_user):
        super(SystemChatBotList, self).__init__()
        self.system_chat_server = system_chat_server
        self.id_user = id_user
        self.index_message_last = -1
        self.timeout_seconds = 1.0


        self.index_response = 0
        self.list_reponse = []
        self.list_reponse.append('you')
        self.list_reponse.append('are')
        self.list_reponse.append('cool')

        self.list_reponse.append('I love you')
        self.list_reponse.append('fuck that')
        self.list_reponse.append('cool')
        

    def prepare(self):
        pass
       
    def work(self):
        list_conversation = self.system_chat_server.load_list_conversation_for_id_user(self.id_user)
        # print(len(list_conversation))
        list_message_send = []
        for conversation in list_conversation:
            # print(conversation)
            if 0 < len(conversation['list_message']):
                if not conversation['list_message'][-1]['id_user'] == self.id_user:
                    message = {}
                    message['id_user'] = self.id_user
                    message['id_conversation'] = conversation['id_conversation']
                    message['text'] = self.response()
                    list_message_send.append(message)

        self.system_chat_server.save_list_message(list_message_send)
        time.sleep(1.0)
            
    def response(self):
        response = self.list_reponse[self.index_response]
        self.index_response += 1
        if len(self.list_reponse) == self.index_response:
            self.index_response = 0
        return response