import sys
import os
import json
from queue import Queue

from rivernode_chat.system_base_theaded_single import SystemBaseThreadedSingle

class SystemConnectorWhatsapp(SystemBaseThreadedSingle):

    def __init__(self, system_whatsapp, system_chat_server):
        super(SystemConnectorWhatsapp, self).__init__()
        self.system_whatsapp = system_whatsapp
        self.system_chat_server = system_chat_server
        
        self.list_connection = []
        self.queue_send_wa = Queue()
        self.queue_send_cs = Queue()

        self.dict_conversation_wa = {}
        self.dict_conversation_cs = {}
        self.system_whatsapp.await_loaded()

        

    def add_connection(self, id_connection, id_conversation_wa, id_user_wa_read, id_conversation_cs, id_user_cs_write, id_user_cs_read):

        connection = {}
        connection['id_connection'] = id_connection
        connection['id_conversation_wa'] = id_conversation_wa
        connection['id_user_wa_read'] = id_user_wa_read
        connection['id_conversation_cs'] = id_conversation_cs
        connection['id_user_cs_write'] = id_user_cs_write
        connection['id_user_cs_read'] = id_user_cs_read
        self.list_connection.append(connection)

    def save(self, path_file):
        with open(path_file, 'w') as file:
            json.dump(self.state, file)


    def load(self, path_file):
        with open(path_file, 'r') as file:
            self.state = json.load(file)

    def prepare(self):
        pass

    # def enqueue_message(self, name_conversation, text):
    #     message_to_send = {}
    #     message_to_send['name_conversation'] = name_conversation
    #     message_to_send['text'] = text
    #     self.queue_message_to_send.put(message_to_send)

    def work(self):        
        print('checking messages wa')
        sys.stdout.flush()
        self.check_message_wa()

        print('checking messages cs')
        sys.stdout.flush()
        self.check_message_cs()
        # if not self.queue_message_to_send.empty():
        #     self.send_message(self.queue_message_to_send.get())
        #     return

        # if self.index_name_conversation == -1:
        #     self.check_message_server()

        # if 0 < len(self.list_name_conversation):
        #     name_conversation = self.list_name_conversation[self.index_name_conversation]
        #     self.check_messages(name_conversation)
        #     if self.index_name_conversation == len(self.list_name_conversation):
        #         self.index_name_conversation = -1

    
    # def send_message_wa(self, message_to_send):
    #     self.system_whatsapp.send_message(message_to_send['name_conversation'], message_to_send['text'])

    # def send_message_cs(self, message_to_send):
    #     self.system_chat_server.save_list_message(id_conversation_cs)
        
    def check_message_wa(self):
         for connection in self.list_connection:
            id_conversation_wa = connection['id_conversation_wa']
            id_user_wa_read = connection['id_user_wa_read']
            id_conversation_cs = connection['id_conversation_cs']
            id_user_cs_write = connection['id_user_cs_write']
            list_message = self.system_whatsapp.get_list_message_recent_for_id_conversation(id_conversation_wa)
            if id_conversation_wa in self.dict_conversation_wa:
                timestamp_last = self.dict_conversation_wa[id_conversation_wa]
            else:
                timestamp_last = 0

            list_text = []
            timestamp_last_new = 0
            for message in list_message:
                if timestamp_last < message['timestamp']:
                    # print('here 1')
                    # print(message['id_user'])
                    # print(id_user_wa_read)
                    if message['id_user'] == id_user_wa_read:
                        # print('here 2')
                        timestamp_last_new = message['timestamp']
                        list_text.append(message['text'])



            if 0 < len(list_text):
                self.dict_conversation_wa[id_conversation_wa] = timestamp_last_new
                print('found new messages')
                print(timestamp_last_new)
                print(list_text)


                list_message = []
                for text in list_text:
                    message = {}
                    message['id_user'] = id_user_cs_write
                    message['id_conversation'] = id_conversation_cs
                    message['text'] = text
                    list_message.append(message)
                print('sending new messages')
                sys.stdout.flush()
                self.system_chat_server.save_list_message(list_message)

    def check_message_cs(self):
        for connection in self.list_connection:
            id_conversation_wa = connection['id_conversation_wa']
            id_conversation_cs = connection['id_conversation_cs']
            id_user_cs_read = connection['id_user_cs_read']

            conversation = self.system_chat_server.load_conversation(id_conversation_cs)
            if id_conversation_cs in self.dict_conversation_cs: #TODO make sure there is always a conversation in there
                previous_message_count = len(self.dict_conversation_cs[id_conversation_cs]['list_message'])
            else:
                previous_message_count = 0

            print('prev_message_count: ' + str(previous_message_count))
            print('curr_message_count: ' + str(len(conversation['list_message'])))

            list_text = []
            for index, message in enumerate(conversation['list_message']):
                
                print(message['id_user'])
                print(id_user_cs_read)
                print(index)
                if previous_message_count <= index:
                    # print(message['id_user'])
                    # print(id_user_cs_read)
                    if message['id_user'] == id_user_cs_read:
                        list_text.append(message['text'])

            
            self.dict_conversation_cs[id_conversation_cs] = conversation
            if 0 < len(list_text):
                print('CON: recieved new message from cs')
                self.system_whatsapp.send_list_message(id_conversation_wa, list_text)
            