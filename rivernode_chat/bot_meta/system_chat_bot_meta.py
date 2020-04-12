import sys
import os
import random
import time

import requests
from bs4 import BeautifulSoup

from rivernode_chat.system_base_theaded_single import SystemBaseThreadedSingle
class SystemChatBotMeta(SystemBaseThreadedSingle):

    def __init__(self, system_chat_server, id_user):
        super(SystemChatBotMeta, self).__init__()
        self.system_chat_server = system_chat_server
        self.id_user = id_user
        self.timeout_seconds = 1.0
        self.dict_conversation = {}
        self.id_message_last = -1

        self.state = {}


    def prepare(self):
        pass
       
    def work(self):
        list_conversation_new = self.system_chat_server.load_list_conversation_delta_for_id_user(self.id_user,  self.id_message_last)
        
        list_message_send = []
        for conversation in list_conversation_new:
            id_conversation = conversation['id_conversation']
            if id_conversation not in self.dict_conversation:
                self.dict_conversation[id_conversation] = conversation
            else:
                self.dict_conversation[id_conversation]['list_message'].extend(conversation['list_message'])
        
            list_message_new = conversation['list_message']
            self.id_message_last = max(self.id_message_last, list_message_new[-1]['id_message'])

            list_message_send.extend(self.response(id_conversation, list_message_new))

            # print(conversation)

        if 0 < len(list_message_send):
            self.system_chat_server.save_list_message(list_message_send)
        time.sleep(1.0)


    def response(self, id_conversation, list_message_new):
        list_message_send = []
        for message_new in list_message_new:
            # if it is a text message
            if message_new['type'] == 'message_text':
                # if i did not send it
                if not message_new['id_user'] == self.id_user:
                    # if it is not empty
                    if 0 < len(message_new['text']):
                        # if it is an command
                        if message_new['text'][0] == '!':
                            list_text = message_new['text'].split(' ')
                            command = list_text[0]
                            if not command == '':
                                list_argrument = list_text[1:]
                                message = self.command(id_conversation, command, list_argrument)
                                list_message_send.append(message)
        return list_message_send

    def command(self, id_conversation, command, list_argrument):
        if command == '!help':
            return self.command_help(id_conversation, list_argrument)
        elif command == '!nupuntnl':
            return self.command_nupuntnl(id_conversation, list_argrument)
        else:
            message = {}
            message['type'] = 'message_text'
            message['id_user'] = self.id_user
            message['id_conversation'] = id_conversation
            message['text'] = '#Unknown command: "' + command + '" Use "!help" to get a list of possible commands'
            return message

    def command_help(self, id_conversation, list_argrument):
            message = {}
            message['type'] = 'message_text'
            message['id_user'] = self.id_user
            message['id_conversation'] = id_conversation

            text = ''
            text += '#The following commands are availeble:\r'
            text += '#!help for this help menu\r'
            text += '#!nupuntnl for todays headlines\r'
            message['text'] = text
            return message

    def command_nupuntnl(self, id_conversation, list_argrument):
        
        message = {}
        message['type'] = 'message_text'
        message['id_user'] = self.id_user
        message['id_conversation'] = id_conversation


        url_request = 'https://www.nu.nl/'
        response = requests.get(url_request)
        doc = BeautifulSoup(response.text, 'html.parser')
        if len(list_argrument) == 0:
            list_element = [element for element in doc.find_all('li') if not element.get('data-sac-marker') == None]
            list_headline = [element.find('span', attrs={'class' : 'title'}).text for element in list_element]
            list_url = [element.find('a').get('href') for element in list_element]
            
            if not id_conversation in self.state:
                self.state[id_conversation] = {}
            
            self.state[id_conversation]['nupuntnlurl'] = list_url
            text = "#nu.nl's headlines\n"
            for index, headline in enumerate(list_headline):
                text += '# (' + str(index) + ')' + headline + '\r'

            message['text'] = text
            return message
        else:
            if not self.state[id_conversation]['nupuntnlurl']:
                message['text'] = 'call without aguments first'
                return message
            try:
                index = int(list_argrument[0])
                if len(self.state[id_conversation]['nupuntnlurl']) <= index:
                    message['text'] = 'agument out of range'
                    return message

                message['text'] = self.get_item_nupuntnl(self.state[id_conversation]['nupuntnlurl'][index])
                return message
            except Exception:
                message['text'] = 'argument must be a numer index'
                return message
        
    def get_item_nupuntnl(self, url_request):
        #TODO get via selenium
        url_request = 'https://www.nu.nl/'
        response = requests.get(url_request)
        doc = BeautifulSoup(response.text, 'html.parser')
        
        text = ''
        list_paragraph = doc.find_all('p')
        for paragraph in list_paragraph:
            text += paragraph.text + '\n'

        return text