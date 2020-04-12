import sys
import os
import random
import time
import copy

from rivernode_chat.struct.conversation import Conversation
from rivernode_chat.struct.message import Message
from rivernode_chat.struct.user import User

class SystemChatServer(object):

    def __init__(self):
        super(SystemChatServer, self).__init__()
        self.dict_conversation = {}
        self.dict_user = {}
        self.id_message_last = -1

    def create_id_message(self):
        self.id_message_last += 1
        return self.id_message_last

    def create_id_user(self):
        return str(random.randint(100000000,999999999))

    def create_id_conversation(self):
        return str(random.randint(100000000,999999999))

    def create_user(self, id_user):
        if id_user in self.dict_user:
            raise RuntimeError('Duplcate id_user: ' + id_user)
        self.dict_user[id_user] = User.create(id_user)

    def create_conversation(self, id_conversation, list_id_user):
        if id_conversation in self.dict_conversation:
            raise RuntimeError('Duplcate id_conversation: ' + id_conversation)

        for id_user in list_id_user:
            if not id_user in self.dict_user:
                raise RuntimeError('Unknown _id_user:' + id_user)
        
        for id_user in list_id_user:
            self.dict_user[id_user]['list_id_conversation'].append(id_conversation)

        self.dict_conversation[id_conversation] = Conversation.create(id_conversation, list_id_user)

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
        return [copy.deepcopy(self.dict_conversation[id_conversation]) for id_conversation in self.dict_user[id_user]['list_id_conversation']]

    def load_list_conversation_delta_for_id_user(self, id_user, id_message_last):
        list_conversation = [self.dict_conversation[id_conversation] for id_conversation in self.dict_user[id_user]['list_id_conversation']]
        list_conversation_delta = []
        for conversation in list_conversation:
            if id_message_last < conversation['list_message'][-1]['id_message']:
                conversation_delta = Conversation.load_conversation_delta(conversation, id_message_last)
                list_conversation_delta.append(conversation_delta)
        return list_conversation_delta

    def save_list_message(self, list_message):
        for message in list_message:
            self.save_message(message)

        
    def save_message(self, message):
        # TODO verify sender signature to autheticate
        conversation = self.dict_conversation[message['id_conversation']]
        if not message['id_user'] in conversation['list_id_user']:
            raise RuntimeError('User not in conversation')
        message['id_message'] = self.create_id_message()
        conversation['list_message'].append(message)
    
    def update(self, id_user, list_message):
        if not id_user in self.dict_user:
            raise RuntimeError('Unknown id_user: ' + id_user)

        for message in list_message:
            self.save_message(message)

        return [self.dict_conversation[id_conversation] for id_conversation in self.dict_user[id_user]['list_id_conversation']]
