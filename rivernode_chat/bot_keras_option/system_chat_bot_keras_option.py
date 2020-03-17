
import nltk
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np

from keras.models import load_model

import json
import random
import time


from rivernode_chat.system_base_theaded_single import SystemBaseThreadedSingle
class SystemChatBotKerasOption(SystemBaseThreadedSingle):

    def __init__(self, system_chat_server, id_user, path_file_model, path_file_context):
        super(SystemChatBotKerasOption, self).__init__()
        self.system_chat_server = system_chat_server
        self.id_user = id_user
        self.path_file_model = path_file_model
        self.path_file_context = path_file_context

        self.lemmatizer = WordNetLemmatizer()
        self.model = None
        self.context = None

    def prepare(self):
        self.model = load_model(self.path_file_model)
        with open(self.path_file_context, 'r') as file:
            self.context = json.load(file)
       
    def work(self):
        list_conversation = self.system_chat_server.load_list_conversation_for_id_user(self.id_user)
        # print(len(list_conversation))
        list_message_send = []
        for conversation in list_conversation:
            # print(conversation)
            if 0 < len(conversation['list_message']):
                if not conversation['list_message'][-1]['id_user'] == self.id_user:
                    message = {}
                    message['id_user'] = self.id_user
                    message['id_conversation'] = conversation['id_conversation']
                    message['text'] = self.response(conversation['list_message'][-1]['text'])
                    list_message_send.append(message)

        self.system_chat_server.save_list_message(list_message_send)
        time.sleep(1.0)
            

    # specific    
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bow(self, sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = self.clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return(np.array(bag))

    def predict_class(self, sentence, model):
        # filter out predictions below a threshold
        p = self.bow(sentence, self.context['list_word'], show_details=False)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": self.context['list_class'][r[0]], "probability": str(r[1])})
        return return_list

    def get_response(self, ints, list_intent):
        tag = ints[0]['intent']
        for intent in list_intent:
            if(intent['tag']== tag):
                result = random.choice(intent['responses'])
                break
        return result

    def response(self, text):
        ints = self.predict_class(text, self.model)
        return self.get_response(ints, self.context['list_intent'])
