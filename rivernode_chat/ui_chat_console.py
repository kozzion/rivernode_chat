import sys
import os
import time

class UIChatConsole(object):

    def __init__(self, system_chat_server, id_user, id_conversation):
        super(UIChatConsole, self).__init__()
        self.system_chat_server = system_chat_server
        self.id_user = id_user
        self.id_conversation = id_conversation

    def run(self):
        while(True):
            self.work()

    def work(self): 
        list_conversation = self.system_chat_server.load_list_conversation_for_id_user(self.id_user)
        self.show_list_conversation(list_conversation)
        text = input()
        if text == 'exit':
            exit()
        message = {}
        message['id_conversation'] = self.id_conversation
        message['id_user'] = self.id_user
        message['text'] = text
        self.system_chat_server.save_list_message([message])
        time.sleep(0.5)

    def show_list_conversation(self, list_conversation):
        print()
        for conversation in list_conversation:
            if conversation['id_conversation'] == self.id_conversation:
                self.show_list_message(conversation['list_message'])

    def show_list_message(self, list_message):
        for message in list_message:
            print(message['id_user'] + ': ' + message['text'])
            sys.stdout.flush()

            
