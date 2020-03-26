import sys
import os
import json

class WhatsappMessage(object):


    # @staticmethod
    # def create_text(id_user, text):
    #     message
    #     message['type']

    @staticmethod
    def print_message(message):
        if message['type'] == 'message_text':
            print(str.decode("utf-8").replace(u"\u2022", "*").encode("utf-8"))
        elif message['type'] == 'message_file':
            print('message_file')
        elif message['type'] == 'message_audio':
            print('message_audio')
        elif message['type'] == 'message_image':
            print('message_image')
        else:
            raise RuntimeError()