import sys
import os
import json
import time
import datetime
import copy

class Conversation(object):
    
    @staticmethod
    def create(id_conversation, list_id_user=[]):
        converstation = {}
        converstation['id_conversation'] = id_conversation
        converstation['list_id_user'] = copy.deepcopy(list_id_user)
        converstation['list_message'] = []
        return converstation

    @staticmethod
    def load_conversation_delta(conversation, id_message_last):
        conversation_delta = {}
        conversation_delta['id_conversation'] = conversation['id_conversation']
        conversation_delta['list_id_user'] = copy.deepcopy(conversation['list_id_user'])
        conversation_delta['list_message'] = []
        for message in conversation['list_message']:
            if id_message_last < message['id_message']:
                conversation_delta['list_message'].append(message)
        return conversation_delta

    @staticmethod
    def append_list_message(conversation, list_message_new):
        #TODO check message validity and id_conversation 
        conversation['list_message'].extend(list_message_new)
