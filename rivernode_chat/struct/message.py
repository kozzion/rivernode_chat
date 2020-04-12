import sys
import os
import json
import time
import datetime
import copy

class Message(object):
    
    @staticmethod
    def print_message(message):
        if message['type'] == 'message_text':
            print(message['id_user'] + ' : ' + message['text'])
        elif message['type'] == 'message_file':
            print('message_file')
        elif message['type'] == 'message_audio':
            print('message_audio')
        elif message['type'] == 'message_image':
            print('message_image')
        else:
            raise RuntimeError()

    @staticmethod
    def create_text(id_conversation, id_user, timestamp, text):
        converstation = {}
        converstation['type'] = 'message_text'
        converstation['id_conversation'] = id_conversation
        converstation['id_user'] = id_user
        converstation['timestamp'] = timestamp
        converstation['text'] = text

    @staticmethod
    def equals(message_a, message_b):
        if message_a['id_message'] != message_b['id_message']:
            return False
        if message_a['id_conversation'] != message_b['id_conversation']:
            return False

        return Message.equals_content(message_a, message_b)

    @staticmethod
    def equals_content(message_a, message_b):
        if message_a['id_user'] != message_b['id_user']:
            return False
        if message_a['timestamp'] != message_b['timestamp']:
            return False
        if message_a['type'] != message_b['type']:
            return False
        if message_a['type'] == 'message_text':
            if message_a['text'] != message_b['text']:
                return False
        return True