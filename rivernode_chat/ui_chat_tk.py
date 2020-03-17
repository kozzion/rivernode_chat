#Creating GUI with tkinter
import sys
import os
import time

import tkinter
from tkinter import *

from rivernode_chat.system_base_theaded_single import SystemBaseThreadedSingle
class UIChatTK(SystemBaseThreadedSingle):

    def __init__(self, system_chat_server, id_user, id_conversation):
        super(UIChatTK, self).__init__()
        self.system_chat_server = system_chat_server
        self.id_user = id_user
        self.id_conversation = id_conversation
        self.create_gui()

        self.index_message = -1


    def send(self):
        text = self.EntryBox.get("1.0",'end-1c').strip()
        self.EntryBox.delete("0.0",END)

        if text != '':
            message = {}
            message['id_conversation'] = self.id_conversation
            message['id_user'] = self.id_user
            message['text'] = text
            self.system_chat_server.save_list_message([message])

    def create_gui(self):
        self.base = Tk()
        self.base.title("Hello")
        self.base.geometry("400x500")
        self.base.resizable(width=FALSE, height=FALSE)

        #Create Chat window
        self.ChatLog = Text(self.base, bd=0, bg="white", height="8", width="50", font="Arial",)

        self.ChatLog.config(state=DISABLED)

        #Bind scrollbar to Chat window
        scrollbar = Scrollbar(self.base, command=self.ChatLog.yview, cursor="heart")
        self.ChatLog['yscrollcommand'] = scrollbar.set

        #Create Button to send message
        self.SendButton = Button(self.base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                            bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                            command= self.send)

        #Create the box to enter message
        self.EntryBox = Text(self.base, bd=0, bg="white",width="29", height="5", font="Arial")


        #Place all components on the screen
        scrollbar.place(x=376,y=6, height=386)
        self.ChatLog.place(x=6,y=6, height=386, width=370)
        self.EntryBox.place(x=128, y=401, height=90, width=265)
        self.SendButton.place(x=6, y=401, height=90)

        # self.base.mainloop()

    def work(self):
        list_conversation = self.system_chat_server.load_list_conversation_for_id_user(self.id_user)
        for conversation in list_conversation:
            if conversation['id_conversation'] == self.id_conversation:
                for index, message in enumerate(conversation['list_message']):
                    if self.index_message < index:
                        sys.stdout.flush()
                        self.ChatLog.config(state=NORMAL)
                        self.ChatLog.config(foreground="#442265", font=("Verdana", 12 ))
                        self.ChatLog.insert(END, message['id_user'] + ': ' + message['text'] + '\n\n')
                        self.ChatLog.config(state=DISABLED)
                        self.ChatLog.yview(END)

                        self.index_message = index

        time.sleep(0.2)

    def show(self):
        self.base.mainloop()


    def chatbot_response(self, msg):
        return 'boem'
