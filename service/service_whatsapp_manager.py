# !flask/bin/python
import sys
import os
import json

from flask import Flask
from flask import request
from flask import jsonify


sys.path.append(os.path.abspath('../../rivernode_core'))
from rivernode_core.system_service import SystemService
from rivernode_core.system_config import SystemConfig
from rivernode_core.persistency.table_object_loader_disk import TableObjectLoaderDisk
from rivernode_core.persistency.route_table_object import RouteTableObject


sys.path.append(os.path.abspath('../../rivernode_chat'))
from rivernode_chat.interface.whatsapp.system_chat_whatsapp import SystemChatWhatsapp
from rivernode_chat.interface.whatsapp.route_chat_whatsapp import RouteChatWhatsapp

#
# load config
#
name_config = os.getenv('NAME_CONFIG', 'config-win-default')
#TODO get this by esb
system_config = SystemConfig(name_config)
# loader_table_object = TableObjectLoaderDisk(system_config.load_path_dir_database())

system_chat_whatsapp = SystemChatWhatsapp()
route_chat_whatsapp = RouteChatWhatsapp(system_chat_whatsapp)
#
# end config
#

# start components
app = Flask(__name__)
system_service = SystemService('chat_server', '0.4.0', '127.0.0.1', '5000')
system_service.add_routes(app)
system_service.add_route(app, route_chat_whatsapp)

#TODO move this to manager service?
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=5000)