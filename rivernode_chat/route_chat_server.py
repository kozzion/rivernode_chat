import sys
import os
import json
import base64

# sys.path.append(os.path.abspath('../../rivernode_core'))

#TODO this should just be a persistance
class RouteChatServer(object):
    def __init__(self, system_chat_server):
        super(RouteChatServer, self).__init__()
        self.system_chat_server = system_chat_server

    def get_dict_route(self):
        dict_route = {}

        dict_route['create_user'] = {}
        dict_route['create_user']['function'] = self.create_user
        dict_route['create_user']['schema'] = {
            'id_user':True}

        dict_route['create_conversation'] = {}
        dict_route['create_conversation']['function'] = self.create_conversation
        dict_route['create_conversation']['schema'] = {
            'id_conversation':True,
            'list_id_user':True}

        dict_route['has_id_user'] = {}
        dict_route['has_id_user']['function'] = self.has_id_user
        dict_route['has_id_user']['schema'] = {
            'id_user':True}

        dict_route['has_id_conversation'] = {}
        dict_route['has_id_conversation']['function'] = self.has_id_conversation
        dict_route['has_id_conversation']['schema'] = {
            'id_conversation':True}

        dict_route['load_list_id_user'] = {}
        dict_route['load_list_id_user']['function'] = self.load_list_id_user
        dict_route['load_list_id_user']['schema'] = {}

        dict_route['load_list_id_conversation'] = {}
        dict_route['load_list_id_conversation']['function'] = self.load_list_id_conversation
        dict_route['load_list_id_conversation']['schema'] = {}


        dict_route['load_list_conversation_for_id_user'] = {}
        dict_route['load_list_conversation_for_id_user']['function'] = self.load_list_conversation_for_id_user
        dict_route['load_list_conversation_for_id_user']['schema'] = {
            'id_user':True}

        dict_route['save_list_message'] = {}
        dict_route['save_list_message']['function'] = self.save_list_message
        dict_route['save_list_message']['schema'] = {
            'list_message':True}

        return dict_route


    def create_user(self, json_request):
        id_user = json_request['id_user']
        self.system_chat_server.create_user(id_user)

        json_response = {'message':'succes'}
        return True, json_response

    def create_conversation(self, json_request):
        id_conversation = json_request['id_conversation']
        list_id_user = json_request['list_id_user']
        self.system_chat_server.create_conversation(id_conversation, list_id_user)

        json_response = {'message':'succes'}
        return True, json_response

    def has_id_user(self, json_request):
        id_user = json_request['id_user']
        return True, {'result':self.system_chat_server.has_id_user(id_user)}

    def has_id_conversation(self, json_request):
        id_conversation = json_request['id_conversation']
        return True, {'result':self.system_chat_server.has_id_conversation(id_conversation)}

    def load_list_id_user(self, json_request):
        return True, {'result':self.system_chat_server.load_list_id_user()}

    def load_list_id_conversation(self, json_request):
        return True, {'result':self.system_chat_server.load_list_id_conversation()}

    def load_list_conversation_for_id_user(self, json_request):
        id_user = json_request['id_user']
        return True, {'result':self.system_chat_server.load_list_conversation_for_id_user(id_user)}

    def save_list_message(self, json_request):
        list_message = json_request['list_message']
        self.system_chat_server.save_list_message(list_message)
        json_response = {'message':'succes'}
        return True, json_response
        


    # def update(self, json_request):
    #     id_user = json_request['id_user']
    #     list_message = json_request['list_message']
    #     list_conversation = self.system_chat_server.update(id_user, list_message)

    #     json_response = {'list_conversation':list_conversation}
    #     return True, json_response
