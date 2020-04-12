import sys
import os
import json
import time
import datetime

# from datetime import datetime
from bs4 import BeautifulSoup

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class HelperMessage(object):


    @staticmethod 
    def get_message_box(driver):
        return driver.find_element(By.CSS_SELECTOR, '*[tabindex="-1"]')


    @staticmethod 
    def get_selected_list_message(driver):
        # print('get_selected_list_message 0')
        # sys.stdout.flush()
        message_box = HelperMessage.get_message_box(driver)
        list_element_message = message_box.find_elements(By.XPATH, "//div[contains(@class, 'message-out') or contains(@class, 'message-in')]")
        # print('get_selected_list_message 1')
        # print(len(list_element_message))
        sys.stdout.flush()
        return list_element_message

    @staticmethod 
    def get_list_message_recent(driver, id_user_write, id_user_read):
        # print('get_list_message_recent 0')
        sys.stdout.flush()
        list_element_message = HelperMessage.get_selected_list_message(driver)   
        # print('get_list_message_recent 1')
        sys.stdout.flush()  
        list_message = []
        for element_message in list_element_message:
            list_message.append(HelperMessage.parse_element_message(driver, element_message, id_user_write, id_user_read))
        # print('get_list_message_recent 2')
        sys.stdout.flush()  
        return list_message

    @staticmethod 
    def has_message_header(driver, bs_obj):
        return not bs_obj.find('div', attrs={'class' : 'copyable-text'}) == None

    @staticmethod 
    def has_message_download(driver, bs_obj):
        return not bs_obj.find('span', attrs={'data-icon' : 'audio-download'}) == None

    @staticmethod 
    def has_message_play(driver, bs_obj):
        return not bs_obj.find('span', attrs={'data-icon' : 'audio-play'}) == None

    @staticmethod 
    def has_message_text(driver, bs_obj):
        list_element = bs_obj.find_all('div')
        for element in list_element:
            list_class = element.get('class')
            if not list_class:
                continue
            if not 'selectable-text' in list_class:
                continue
            if not 'invisible-space' in list_class:
                continue
            if not 'copyable-text' in list_class:
                continue
            return True  
        list_element = bs_obj.find_all('span')
        for element in list_element:
            list_class = element.get('class')
            if not list_class:
                continue
            if not 'selectable-text' in list_class:
                continue
            if not 'invisible-space' in list_class:
                continue
            if not 'copyable-text' in list_class:
                continue
            return True
        return False

    @staticmethod 
    def has_message_image(driver, bs_obj):
        return not bs_obj.find('img') == None

    @staticmethod 
    def has_message_video(driver, bs_obj):
        return not bs_obj.find('video') == None
  

    @staticmethod 
    def get_message_type(driver, bs_obj):
        if HelperMessage.has_message_download(driver, bs_obj):
            return 'message_file'
        if HelperMessage.has_message_play(driver, bs_obj):
            return 'message_audio'
        if HelperMessage.has_message_text(driver, bs_obj):
            return 'message_text'
        if HelperMessage.has_message_image(driver, bs_obj):
            return 'message_image'
        if HelperMessage.has_message_video(driver, bs_obj):
            return 'message_video'
        return 'message_unknown'



    @staticmethod 
    def parse_message_header(driver, bs_obj):
        element_header = bs_obj.find('div', attrs={'class' : 'copyable-text'})
        header_text = element_header.get('data-pre-plain-text')
        id_user = header_text.split(']')[1][1:-2]
        str_datetime = header_text.split(']')[0][1:]
        datetime_message = datetime.datetime.strptime(str_datetime, '%H:%M, %m/%d/%Y')
        timestamp_message = int(datetime.datetime.timestamp(datetime_message))
        return id_user, timestamp_message

    @staticmethod 
    def parse_message_text(driver, bs_obj):
        message = {}
        message['type'] = 'message_text'
        if HelperMessage.has_message_header(driver, bs_obj):
            id_user, timestamp_message = HelperMessage.parse_message_header(driver, bs_obj)
            message['id_user'] = id_user
            message['timestamp'] = timestamp_message

        element_text =  bs_obj.find('span', attrs={'class' : 'copyable-text'})
        if not(element_text):
            # print('no text')
            message['text'] = ''
        else:
            message['text'] = element_text.find('span').text
        return message

    @staticmethod 
    def parse_message_file(driver, bs_obj): 
        element_icon =  bs_obj.find('span', attrs={'data-icon' : 'audio-download'})
        if not element_icon:
            print('no download')
            content = ''

        message = {}
        message['type'] = 'message_file'
        if HelperMessage.has_message_header(driver, bs_obj):
            id_user, timestamp_message = HelperMessage.parse_message_header(driver, bs_obj)
            message['id_user'] = id_user
            message['timestamp'] = timestamp_message

        message['content'] = ''
        return message

    @staticmethod 
    def parse_message_image(driver, bs_obj): 
        uri =  bs_obj.find('img').get('src')
        try:
            content = HelperMessage.get_blob_as_stringbase64(driver, uri)
        except Exception as exception:
            print(exception)
            content = ''

        message = {}
        message['type'] = 'message_image'
        if HelperMessage.has_message_header(driver, bs_obj):
            id_user, timestamp_message = HelperMessage.parse_message_header(driver, bs_obj)
            message['id_user'] = id_user
            message['timestamp'] = timestamp_message
        message['content'] = 'content'
        return message

    @staticmethod 
    def parse_message_audio(driver, bs_obj):   
        uri =  bs_obj.find('audio').get('src')
        try:
            content = HelperMessage.get_blob_as_stringbase64(driver, uri)
        except Exception as exception:
            print(exception)
            content = ''

        message = {}
        message['type'] = 'message_audio'
        if HelperMessage.has_message_header(driver, bs_obj):
            id_user, timestamp_message = HelperMessage.parse_message_header(driver, bs_obj)
            message['id_user'] = id_user
            message['timestamp'] = timestamp_message

        message['content'] = 'content'
        return message

    @staticmethod 
    def parse_message_video(driver, bs_obj):   
        uri =  bs_obj.find('video').get('src')
        try:
            content = HelperMessage.get_blob_as_stringbase64(driver, uri)
        except Exception as exception:
            print(exception)
            content = ''
        
        message = {}
        message['type'] = 'message_audio'
        if HelperMessage.has_message_header(driver, bs_obj):
            id_user, timestamp_message = HelperMessage.parse_message_header(driver, bs_obj)
            message['id_user'] = id_user
            message['timestamp'] = timestamp_message

        message['content'] = 'content'
        return message

    @staticmethod 
    def parse_element_message(driver, element_message, id_user_write, id_user_read):
        html = element_message.get_attribute('outerHTML')   
        bs_obj = BeautifulSoup(html, 'html.parser')

        message_type = HelperMessage.get_message_type(driver, bs_obj)
        # print(message_type)
        # message_source = 
        # class, 'message-out'
    
        if message_type == 'message_text':
            message = HelperMessage.parse_message_text(driver, bs_obj)
        elif message_type == 'message_file':
            message = HelperMessage.parse_message_file(driver, bs_obj)
        elif message_type == 'message_audio':
            message = HelperMessage.parse_message_audio(driver, bs_obj)
        elif message_type == 'message_image':
            message = HelperMessage.parse_message_image(driver, bs_obj)
        elif message_type == 'message_video':
            message = HelperMessage.parse_message_video(driver, bs_obj)
        else:
            raise RuntimeError('unknown message type')

        # filling in the blanks
        if not 'id_user' in message:
            # print('add id_user')
            if 'message-out' in bs_obj.get('class'):
                message['id_user'] = id_user_write
            else:
                message['id_user'] = id_user_read

        if not 'timestamp' in message:
            message['timestamp'] = -1
        return message

    @staticmethod 
    def get_blob_as_stringbase64(driver, uri):
        result = driver.execute_async_script("""
            var uri = arguments[0];
            var callback = arguments[1];
            var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
            var xhr = new XMLHttpRequest();
            xhr.responseType = 'arraybuffer';
            xhr.onload = function(){ callback(toBase64(xhr.response)) };
            xhr.onerror = function(){ callback(xhr.status) };
            xhr.open('GET', uri);
            xhr.send();
            """, uri)
        if type(result) == int :
            raise Exception("Request failed with status %s" % result)
        return result