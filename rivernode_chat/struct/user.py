import sys
import os
import json
import time
import datetime
import copy

class User(object):
    
    @staticmethod
    def create(id_user):
        converstation = {}
        converstation['id_user'] = id_user
        converstation['list_id_conversation'] = []