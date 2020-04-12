import sys
import os
import json
import time
from queue import Queue

sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.system_base_theaded_single import SystemBaseThreadedSingle

from rivernode_chat.struct.message import Message
from rivernode_chat.struct.conversation import Conversation

class SystemChatWhatsapp(SystemBaseThreadedSingle):

    def __init__(self, webcontroller_whatsapp):
        super(SystemChatWhatsapp, self).__init__()
        self.webcontroller_whatsapp = webcontroller_whatsapp


        self.state = {}
        self.state['id_user_write'] = []
        self.state['list_queue_action'] = []
        self.state['dict_conversation'] = {}
        self.state['id_message_last'] = -1

        self.webcontroller_whatsapp.load_whatsapp()
        self.webcontroller_whatsapp.await_load_whatsapp()

        self.timestamp_last = int(time.time())


    def create_id_message(self):
        self.state['id_message_last'] += 1
        return self.state['id_message_last']

    def save(self, path_file):
        with open(path_file, 'w') as file:
            json.dump(self.state, file)

    def load(self, path_file):
        with open(path_file, 'r') as file:
            self.state = json.load(file)


    def create_conversation_group(self, id_conversation, list_id_user):
        self.webcontroller_whatsapp.create_conversation_group(id_conversation, list_id_user)
        
    def listen_converstation(self, id_conversation, list_id_user):
        # id_user_write, = lo
        # id_user_read
        self.state['dict_conversation'][id_conversation] = Conversation.create(id_conversation, list_id_user)
        #TODO get id_user_write and id_user_read from conversation


    def prepare(self):
        pass


    # section work
    def work(self):
        self.do_actions()
        self.check_messages()


    def send_message(self, id_conversation, text):
        action = {}
        action['type'] = 'action_send'     
        action['id_conversation'] = id_conversation
        action['text'] = text
        self.state['list_queue_action'].append(action)

    def do_actions(self):
        list_action = self.state['list_queue_action']
        self.state['list_queue_action'] = []
        for action in list_action:
            print('here3')
            print(action)
            if action['type'] == 'action_send':
                id_conversation = action['id_conversation']
                text = action['text']
                print('action_send')
                print(id_conversation)
                print(text)
                self.webcontroller_whatsapp.send_for_id_conversation(id_conversation, text)

    
    def check_messages(self):
        for conversation in self.state['dict_conversation'].values():
            id_conversation = conversation['id_conversation']
            id_user_write = conversation['list_id_user'][0]
            id_user_read = conversation['list_id_user'][0]


            list_message = self.webcontroller_whatsapp.get_list_message_recent_for_id_conversation(id_conversation, id_user_write, id_user_read)
            list_message_filtered = self.filter_message_new(conversation, list_message)
            
            for message in list_message_filtered:
                message['id_conversation'] = id_conversation
                message['id_message'] = self.create_id_message()
            Conversation.append_list_message(conversation, list_message_filtered)

    def filter_message_new(self, conversation, list_message):
        if len(conversation['list_message']) == 0:
            pass
        elif conversation['list_message'][-1]['timestamp'] < list_message[0]['timestamp']: 
            pass
        else:
            #remove duplicates, TODO we can speed this up
            for message_old in conversation['list_message']:
                if Message.equals_content(message_old, list_message[0]):
                    list_message.remove(list_message[0])
                if len(list_message) == 0:
                    break
        return list_message
        

    def load_conversation_delta(self, id_conversation, id_message_last):
        conversation = self.state['dict_conversation'][id_conversation]
        conversation_delta = Conversation.load_conversation_delta(conversation, id_message_last)
        for message in conversation_delta['list_message']:
            if id_message_last < message['id_message']:
                id_message_last = message['id_message']
        return conversation_delta, id_message_last

