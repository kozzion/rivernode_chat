from __future__ import absolute_import

import requests
import urllib3

class ClientBase(object): #ClientBas
    def __init__(self, descriptor_service):
        super(ClientBase, self).__init__()
        self.api_key = descriptor_service['api_key']
        if descriptor_service['is_https']:
            self.name_protocol = 'https:/'
        else:
            self.name_protocol = 'http:/'
            
        self.name_host = descriptor_service['name_host']
        self.name_port = descriptor_service['name_port']
        self.url_base = self.name_protocol + '/' + self.name_host + ':' + self.name_port

        self.name_service = descriptor_service['name_service']
        self.name_version = descriptor_service['name_version']
        self.url_service = self.url_base + '/' + self.name_service + '/' + self.name_version
        urllib3.disable_warnings() # We do a lot of self-signed sertificates this disable connection warnings

    def health(self):
        url_request = self.url_base + '/health'
        response = requests.get(url_request, verify=False)#TODO the verify part matters only to https
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None

    def load_status(self):
        json_request = {}
        json_request['api_key'] = self.api_key
        url_request = self.url_base + '/load_status'
        response = requests.post(url_request, json=json_request, verify=False)#TODO the verify part matters only to https
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None

    def load_descriptor_service(self):
        json_request = {}
        json_request['api_key'] = self.api_key
        url_request = self.url_base + '/load_descriptor_service'
        response = requests.post(url_request, json=json_request, verify=False) #TODO the verify part matters only to https
        if response.status_code == 200:
            return True, response.json()
        else:
            return False, None
