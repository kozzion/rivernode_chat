import sys
import os
import json
import time
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

        self.system_whatsapp.load_whatsapp()
        self.system_whatsapp.await_load_whatsapp()

        self.timestamp_last = int(time.time())

    def tick(self, place):
        timestamp_curr = int(time.time() * 1000)
        diff = timestamp_curr - self.timestamp_last
        # print(place + ' : ' + str(diff))
        sys.stdout.flush()
        self.timestamp_last = timestamp_curr

    def add_connection(self, id_connection, id_conversation_wa, id_user_wa_write, id_user_wa_read, id_conversation_cs, id_user_cs_write, id_user_cs_read):

        connection = {}
        connection['id_connection'] = id_connection
        connection['id_conversation_wa'] = id_conversation_wa
        connection['id_user_wa_write'] = id_user_wa_write
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

    def work(self):        
        self.tick('work 0')
        sys.stdout.flush()
        self.check_message_wa()

        self.tick('work 1')
        sys.stdout.flush()
        self.check_message_cs()

    def message_equal_wa(self, message_a, message_b):
        if message_a['id_user'] != message_b['id_user']:
            return False
        if message_a['timestamp'] != message_b['timestamp']:
            return False
        if message_a['text'] != message_b['text']:
            return False
        return True

    def filter_message_new_wa(self, connection, list_message):
        # select only messages from the user we are reading
        id_user_wa_read = connection['id_user_wa_read']
        list_message = [message for message in list_message if message['id_user'] == id_user_wa_read]
        if len(list_message) == 0:
            return []
        
        # get conversation
        id_conversation_wa = connection['id_conversation_wa']
        if not id_conversation_wa in self.dict_conversation_wa:
            conversation = {}
            conversation['id_conversation'] = id_conversation_wa
            conversation['list_message'] = []
            self.dict_conversation_wa[id_conversation_wa] = conversation
        else:
            conversation = self.dict_conversation_wa[id_conversation_wa]
        
        if len(conversation['list_message']) == 0:
            pass
        elif conversation['list_message'][-1]['timestamp'] < list_message[0]['timestamp']: 
            pass
        else:
            #remove duplicates, TODO we can speed this up
            for message_old in conversation['list_message']:
                if self.message_equal_wa(message_old, list_message[0]):
                    list_message.remove(list_message[0])
                if len(list_message) == 0:
                    break

        list_message_new = list_message
        conversation['list_message'].extend(list_message_new)
        return list_message_new
        

    def check_message_wa(self):
        self.tick('check_message_wa 0')
        for connection in self.list_connection:
            id_conversation_wa = connection['id_conversation_wa']
            id_user_wa_write = connection['id_user_wa_write']
            id_user_wa_read = connection['id_user_wa_read']
            id_conversation_cs = connection['id_conversation_cs']
            id_user_cs_write = connection['id_user_cs_write']
            self.tick('check_message_wa 1')

            list_message = self.system_whatsapp.get_list_message_recent_for_id_conversation(id_conversation_wa, id_user_wa_write, id_user_wa_read)
            list_message_new = self.filter_message_new_wa(connection, list_message)

            if 0 < len(list_message_new):
                print('found new messages')
                print(list_message_new[-5:])

                list_message_send = []
                for message_new in list_message_new:
                    message = {}
                    message['type'] = 'message_text'
                    message['id_user'] = id_user_cs_write
                    message['id_conversation'] = id_conversation_cs
                    message['text'] = message_new['text']
                    list_message_send.append(message)

                print('sending new messages')
                sys.stdout.flush()
                self.tick('check_message_wa 2')
                self.system_chat_server.save_list_message(list_message_send)
                self.tick('check_message_wa 3')

    def check_message_cs(self):
        for connection in self.list_connection:
            id_conversation_wa = connection['id_conversation_wa']
            id_conversation_cs = connection['id_conversation_cs']
            id_user_cs_read = connection['id_user_cs_read']
            self.tick('check_message_wa 0')
            conversation = self.system_chat_server.load_conversation(id_conversation_cs)
            if id_conversation_cs in self.dict_conversation_cs: #TODO make sure there is always a conversation in there
                previous_message_count = len(self.dict_conversation_cs[id_conversation_cs]['list_message'])
            else:
                previous_message_count = 0
            self.tick('check_message_wa 1')

            list_text = []
            for index, message in enumerate(conversation['list_message']):
                if previous_message_count <= index:
                    if message['id_user'] == id_user_cs_read:
                        list_text.append(message['text'])

            self.tick('check_message_wa 2')
            self.dict_conversation_cs[id_conversation_cs] = conversation
            if 0 < len(list_text):
                print('CON: recieved new message from cs')
                self.system_whatsapp.send_list_message(id_conversation_wa, list_text)
            self.tick('check_message_wa 3')
            