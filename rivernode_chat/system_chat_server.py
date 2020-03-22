import sys
import os
import random
import time
import copy

class SystemChatServer(object):

    def __init__(self):
        super(SystemChatServer, self).__init__()
        self.dict_conversation = {}
        self.dict_user = {}
        
    def create_id_user(self):
        return str(random.randint(100000000,999999999))

    def create_id_conversation(self):
        return str(random.randint(100000000,999999999))

    def create_user(self, id_user):
        if id_user in self.dict_user:
            raise RuntimeError('Duplcate id_user: ' + id_user)
        user = {}
        user['id_user'] = id_user
        user['list_id_conversation'] = []
        self.dict_user[id_user] = user

    def create_conversation(self, id_conversation, list_id_user):
        if id_conversation in self.dict_conversation:
            raise RuntimeError('Duplcate id_conversation: ' + id_conversation)

        for id_user in list_id_user:
            if not id_user in self.dict_user:
                raise RuntimeError('Unknown _id_user:' + id_user)
        
        for id_user in list_id_user:
            self.dict_user[id_user]['list_id_conversation'].append(id_conversation)

        conversation = {}
        conversation['id_conversation'] = id_conversation 
        conversation['list_id_user'] = list_id_user
        conversation['list_message'] = []
        self.dict_conversation[id_conversation] = conversation

    def has_id_user(self, id_user):
        return id_user in self.dict_user

    def has_id_conversation(self, id_conversation):
        return id_conversation in self.dict_conversation

    def load_user(self, id_user):
        return copy.deepcopy(self.dict_user[id_user])

    def load_conversation(self, id_conversation):
        return copy.deepcopy(self.dict_conversation[id_conversation])

    def load_list_id_user(self):
        return list(self.dict_user.keys())

    def load_list_id_conversation(self):
        return list(self.dict_conversation.keys())

    def load_list_conversation_for_id_user(self, id_user):
        return [self.dict_conversation[id_conversation] for id_conversation in self.dict_user[id_user]['list_id_conversation']]

    def save_list_message(self, list_message):
        for message in list_message:
            self.save_message(message)

        
    def save_message(self, message):
        # TODO verify sender signature to autheticate
        conversation = self.dict_conversation[message['id_conversation']]
        if not message['id_user'] in conversation['list_id_user']:
            raise RuntimeError('User not in conversation')
        conversation['list_message'].append(message)
    
    def update(self, id_user, list_message):
        if not id_user in self.dict_user:
            raise RuntimeError('Unknown id_user: ' + id_user)

        for message in list_message:
            self.save_message(message)

        return [self.dict_conversation[id_conversation] for id_conversation in self.dict_user[id_user]['list_id_conversation']]





    # def update_client(self, last_poll, timeout_seconds, list_message_put, id_conversation):
    #     # print('server_update: ' + str(len(list_message_put)))
    #     # print('server_index_last_message: ' + str(index_last_message))
    #     # sys.stdout.flush()
    #     conversation = self.dict_conversation[id_conversation]
    #     for message in list_message_put:
    #         message['timestamp'] = time.tim
    #         conversation['list_message'].append(message)
        

    #     list_message_get = []
    #     for message in conversation['list_message']:
    #         if index_last_message < message['index_message']:
    #             list_message_get.append(message)

    #     if len(list_message_get) == 0:
    #         time.sleep(timeout_seconds)

    #     list_message_get = []
    #     for message in conversation['list_message']:
    #         if index_last_message < message['index_message']:
    #             list_message_get.append(message)
    #     # print('server_return: ' + str(len(list_message_get)))
    #     # sys.stdout.flush()
    #     return list_message_get

            
