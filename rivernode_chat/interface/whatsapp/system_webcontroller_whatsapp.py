import sys
import os
import json
import time
import datetime
from bs4 import BeautifulSoup

# from datetime import datetime

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from rivernode_chat.interface.whatsapp.domlocator_whatsapp import DOMLocatorWhatsapp as dl

class SystemWebcontrollerWhatsapp(object):

    def __init__(self, driver:WebDriver):
        super(SystemWebcontrollerWhatsapp, self).__init__()
        self.driver = driver
        self.state = {}

  
    def save(self, path_file):
        with open(path_file, 'w') as file:
            json.dump(self.state, file)


    def load(self, path_file):
        with open(path_file, 'r') as file:
            self.state = json.load(file)

    def prepare(self):
        pass

    def work(self):
        pass

    def is_loaded(self):
        return 0 < len(self.driver.find_elements(By.TAG_NAME, 'header' ))

    
    def load_whatsapp(self):
        # if self.driver
        if not self.driver.current_url == 'https://web.whatsapp.com/':
            self.driver.get("https://web.whatsapp.com/") #TODO check and move to controller

    def await_load_whatsapp(self):
        while(not self.is_loaded()):
            print('not loaded')
            print(self.driver.current_url)
            sys.stdout.flush()
            time.sleep(0.1)



    def get_list_message_recent_for_id_conversation(self, id_conversation, id_user_write, id_user_read):
        # print('get_list_message_recent_for_id_conversation 0')
        # sys.stdout.flush()
        if not self.get_id_conversation_selected() == id_conversation:
            # print('get_list_message_recent_for_id_conversation 1')
            # sys.stdout.flush()
            self.select_searched_conversation(id_conversation)
        # print('get_list_message_recent_for_id_conversation 2')
        # sys.stdout.flush()
        return self.get_list_message_recent(id_user_write, id_user_read)


# <div class="_1ZMSM" style="transform: scaleX(1) scaleY(1); opacity: 1;"><span class="P6z4j">1</span></div>
    #
    # message stuff
    #

    def get_list_message_recent(self, id_user_write, id_user_read):
        # print('get_list_message_recent 0')
        sys.stdout.flush()
        list_element_message = dl.get_selected_list_message(self.driver)   
        # print('get_list_message_recent 1')
        sys.stdout.flush()  
        list_message = []
        for element_message in list_element_message:
            list_message.append(self.parse_element_message(element_message, id_user_write, id_user_read))
        # print('get_list_message_recent 2')
        sys.stdout.flush()  
        return list_message


    def has_message_header(self, bs_obj):
        return not bs_obj.find('div', attrs={'class' : 'copyable-text'}) == None

    def has_message_download(self, bs_obj):
        return not bs_obj.find('span', attrs={'data-icon' : 'audio-download'}) == None

    def has_message_play(self, bs_obj):
        return not bs_obj.find('span', attrs={'data-icon' : 'audio-play'}) == None

    def has_message_text(self, bs_obj):
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

    def has_message_image(self, bs_obj):
        return not bs_obj.find('img') == None

    def has_message_video(self, bs_obj):
        return not bs_obj.find('video') == None
  

    def get_message_type(self, bs_obj):
        if self.has_message_download(bs_obj):
            return 'message_file'
        if self.has_message_play(bs_obj):
            return 'message_audio'
        if self.has_message_text(bs_obj):
            return 'message_text'
        if self.has_message_image(bs_obj):
            return 'message_image'
        if self.has_message_video(bs_obj):
            return 'message_video'
        return 'message_unknown'




    def parse_message_header(self, bs_obj):
        element_header = bs_obj.find('div', attrs={'class' : 'copyable-text'})
        header_text = element_header.get('data-pre-plain-text')
        id_user = header_text.split(']')[1][1:-2]
        str_datetime = header_text.split(']')[0][1:]
        datetime_message = datetime.datetime.strptime(str_datetime, '%H:%M, %m/%d/%Y')
        timestamp_message = int(datetime.datetime.timestamp(datetime_message))
        return id_user, timestamp_message

    def parse_message_text(self, bs_obj):
        message = {}
        message['type'] = 'message_text'
        if self.has_message_header(bs_obj):
            id_user, timestamp_message = self.parse_message_header(bs_obj)
            message['id_user'] = id_user
            message['timestamp'] = timestamp_message

        element_text =  bs_obj.find('span', attrs={'class' : 'copyable-text'})
        if not(element_text):
            print('no text')
            message['text'] = ''
        else:
            message['text'] = element_text.find('span').text
        return message

    def parse_message_file(self, bs_obj): 
        element_text =  bs_obj.find('span', attrs={'data-icon' : 'audio-download'})
        if not element_text:
            print('no download')
            return None
        message = {}
        message['type'] = 'message_file'
        message['id_user'] = ''
        message['timestamp'] = ''
        message['content'] = ''
        return message

    def parse_message_image(self, bs_obj): 
        uri =  bs_obj.find('img').get('src')
        print(uri)
        content = self.get_blob_as_stringbase64(uri)
        message = {}
        message['type'] = 'message_image'
        message['id_user'] = ''
        message['timestamp'] = ''
        message['content'] = 'content'
        return message

    def parse_message_audio(self, bs_obj):   
        uri =  bs_obj.find('audio').get('src')
        print(uri)
        content = self.get_blob_as_stringbase64(uri)
        message = {}
        message['type'] = 'message_audio'
        message['id_user'] = ''
        message['timestamp'] = ''
        message['content'] = 'content'
        return message

    def parse_message_video(self, bs_obj):   
        uri =  bs_obj.find('video').get('src')
        print(uri)
        content = self.get_blob_as_stringbase64(uri)
        message = {}
        message['type'] = 'message_audio'
        message['id_user'] = ''
        message['timestamp'] = ''
        message['content'] = 'content'
        return message



    def parse_element_message(self, element_message, id_user_write, id_user_read):
        html = element_message.get_attribute('outerHTML')   
        bs_obj = BeautifulSoup(html, 'html.parser')

        message_type = self.get_message_type(bs_obj)
        print(message_type)
        # message_source = 
        # class, 'message-out'
    
        if message_type == 'message_text':
            message = self.parse_message_text(bs_obj)
        elif message_type == 'message_file':
            message = self.parse_message_file(bs_obj)
        elif message_type == 'message_audio':
            message = self.parse_message_audio(bs_obj)
        elif message_type == 'message_image':
            message = self.parse_message_image(bs_obj)
        elif message_type == 'message_video':
            message = self.parse_message_video(bs_obj)
        else:
            raise RuntimeError('unknown message type')

        # filling in the blanks
        if not 'id_user' in message:
            print('add id_user')
            if 'message-out' in bs_obj.get('class'):
                message['id_user'] = id_user_write
            else:
                message['id_user'] = id_user_read

        return message

    def get_blob_as_stringbase64(self, uri):
        result = self.driver.execute_async_script("""
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


#
# end message read
# 
    def get_id_conversation_selected(self):
        list_div_main = self.driver.find_elements_by_id('main')
        if len(list_div_main) == 0:
            print('main not found')
            return ''            
        list_element = list_div_main[0].find_elements(By.TAG_NAME, "span")
        for element in list_element:
            if element.get_attribute('title'):
                if element.get_attribute('title') == element.get_attribute("innerHTML"):
                    attribute = element.get_attribute('title')
                    # print('selected_conversation:')
                    # print(attribute)                
                    return attribute

        print('title not found')
        return '' 

    def select_searched_conversation(self, name_conversation):
        search_box = self.get_element_search_box()
        search_box.clear()
        search_box.send_keys(name_conversation)
        time.sleep(0.5)
        self.select_present_conversation(name_conversation)

    def select_present_conversation(self, name_conversation):
        list_element = self.find_elements_by_title(name_conversation)
        if not len(list_element) == 1:
            raise RuntimeError()
        element = list_element[0]
        element.click()
        time.sleep(1) #TODO await selection
        self.name_conversation = name_conversation    

    def get_element_send_box(self):
        list_element = self.driver.find_elements(By.XPATH,  "//div[@contenteditable='true']")
        for element in list_element:
            if element.get_attribute('data-tab') == '1':
                return element
        raise RuntimeError()

    def get_element_search_box(self):
        list_element = self.driver.find_elements(By.XPATH,  "//div[@contenteditable='true']")
        for element in list_element:
            if element.get_attribute('data-tab') == '3':
                return element
        raise RuntimeError()

    def send_list_message(self, id_conversation, list_text):
        if not self.get_id_conversation_selected() == id_conversation:
            self.select_searched_conversation(id_conversation)
        for text in list_text:
            self.send_selected_user(text)
        
    def send_selected_user(self, text):
        input_box = self.get_element_send_box()
        input_box.clear()
        input_box.send_keys(text) # + Keys.ENTER (Uncomment it if your msg doesnt contain '\n')
        
        while not input_box.get_attribute('innerHTML') == text:
            sys.stdout.flush()
            time.sleep(0.1)

        input_box.send_keys(Keys.ENTER)
        #TODO for more speedup webdriver.executeScript("document.getElementById('elementID').setAttribute('value', 'new value for element')");


    def find_elements_by_title(self, title):
        # driver.find_element_by_xpath(
        return self.driver.find_elements(By.XPATH, '//*[@title="' + title + '"]')
