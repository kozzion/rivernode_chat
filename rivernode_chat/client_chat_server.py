from __future__ import absolute_import

import os
import sys
import requests
import json
import urllib3

from rivernode_chat.client_base import ClientBase

class ClientChatServer(ClientBase): #ClientBas
    def __init__(self, descriptor_service):
        super(ClientChatServer, self).__init__(descriptor_service)
        self.name_service = descriptor_service['name_service']
        self.name_version = descriptor_service['name_version']
        self.url_service = self.url_base + '/' + self.name_service + '/' + self.name_version
        urllib3.disable_warnings()

    def create_conversation(self, id_conversation, list_id_user):
        json_request = {}
        json_request['api_key'] = self.api_key
        json_request['id_conversation'] = id_conversation
        json_request['list_id_user'] = list_id_user
        url_request = self.url_service + '/create_conversation'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError('status_code not 200 but: ' + str(response.status_code))

    def create_user(self, id_user):
        json_request = {}
        json_request['api_key'] = self.api_key
        json_request['id_user'] = id_user
        url_request = self.url_service + '/create_user'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError('status_code not 200 but: ' + str(response.status_code))

    def has_id_user(self, id_user):
        json_request = {}
        json_request['api_key'] = self.api_key
        json_request['id_user'] = id_user
        url_request = self.url_service + '/has_id_user'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return response.json()['result']
        else:
            raise RuntimeError('status_code not 200 but: ' + str(response.status_code))

    def has_id_conversation(self, id_conversation):
        json_request = {}
        json_request['api_key'] = self.api_key
        json_request['id_conversation'] = id_conversation
        url_request = self.url_service + '/has_id_conversation'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return response.json()['result']
        else:
            raise RuntimeError('status_code not 200 but: ' + str(response.status_code))

    def load_list_id_user(self):
        json_request = {}
        json_request['api_key'] = self.api_key
        url_request = self.url_service + '/load_list_id_user'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return response.json()['result']
        else:
            raise RuntimeError('status_code not 200 but: ' + str(response.status_code))

    def load_list_id_conversation(self):
        json_request = {}
        json_request['api_key'] = self.api_key
        url_request = self.url_service + '/load_list_id_conversation'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return response.json()['result']
        else:
            raise RuntimeError('status_code not 200 but: ' + str(response.status_code))


    def load_list_conversation_for_id_user(self, id_user):
        json_request = {}
        json_request['api_key'] = self.api_key
        json_request['id_user'] = id_user
        url_request = self.url_service + '/load_list_conversation_for_id_user'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return response.json()['result']
        else:
            raise RuntimeError('status_code not 200 but: ' + str(response.status_code))

    def save_list_message(self, list_message):
        json_request = {}
        json_request['api_key'] = self.api_key
        json_request['list_message'] = list_message
        url_request = self.url_service + '/save_list_message'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError('status_code not 200 but: ' + str(response.status_code))


    # def update(self, id_user, list_message):
    #     json_request = {}
    #     json_request['api_key'] = self.api_key
    #     json_request['id_user'] = id_user
    #     json_request['list_message'] = list_message
    #     url_request = self.url_service + '/update_chat'
    #     # print(url_request)
    #     response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
    #     if response.status_code == 200:
    #         return response.json()['list_conversation']
    #     else:
    #         raise RuntimeError('status_code not 200 but: ' + str(response.status_code))

    @staticmethod
    def create_client(api_key, name_host='127.0.0.1', name_port='5000', is_https=False):
        descriptor_service = ClientChatServer.load_descriptor_service(api_key, name_host, name_port)
        return ClientChatServer(descriptor_service)

    @staticmethod
    def load_descriptor_service(api_key, name_host, name_port, is_https=False):
        urllib3.disable_warnings()
        #TODO this is the same for all clients
        if is_https:
            name_protocol = 'https:/'
        else:
            name_protocol = 'http:/'
        url_request = name_protocol + '/' + name_host + ':' + name_port +  '/load_descriptor_service' 
        print(url_request)
        sys.stdout.flush()

        json_request = {}
        json_request['api_key'] = api_key

        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if not response.status_code == 200:
            print(response.content)
            raise RuntimeError(str(response.json()))

        return response.json()