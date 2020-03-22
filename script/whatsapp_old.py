import sys
import os
import json

# Can save contact with their phone Number

# Import required packages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import datetime
import time
import pickle

from rivernode_chat.whatsapp.system_webcontroller_whatsapp import SystemWebcontrollerWhatsapp

# def save(driver):
#     print('saving cookies')
#     pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))


# def load(driver):
#     print('loading cookies')
#     cookies = pickle.load(open("cookies.pkl", "rb"))
#     for cookie in cookies:
#         driver.add_cookie(cookie)



executable_path = 'C:\\tools\\chromedriver\\chromedriver_80_0_3987_106.exe'
#

# try:
#     print('connecting to runnning session')
#     sys.stdout.flush()
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")
#     driver = webdriver.Remote(command_executor='http://127.0.0.1:65256', desired_capabilities={}) # this opens a new windw
#     driver.session_id = 'f7baa8a0dc427b36df04e82e8aa3f2c4'
#     driver.close()
    
# except Exception as e:
    # print(e)
print('starting new session')
# start normally
chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium") 
driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
driver.get("https://web.whatsapp.com/") #TODO check and move to controller

session = {}
session['url'] = driver.command_executor._url
session['session_id'] = driver.session_id
with open('session.json', 'w') as file:
    json.dump(session, file)






controller = SystemWebcontrollerWhatsapp(driver)
controller.await_loaded()


# name_conversation = 'Deception island swimteam'
name_conversation = 'Myself'
controller.select_searched_conversation(name_conversation)
# controller.select_present_user(user)
list_message = controller.get_list_message_recent()
for message in list_message:
    print(message['author'])
    print(message['text'])

# controller.send_selected_user('Dit is een automatisch verzonden bericht')

# user = 'Ward van Hoof'

# controller.send_selected_user('ward dit is een automatisch verzonden bericht')

# time.sleep(30)
# driver.quit()
# def send_message(wait, target, message):
#     print("Target is: " + target)
#     try:
#         # Select the target
#         x_arg = '//span[contains(@title,' + target + ')]'
#         try:
#             wait.until(EC.presence_of_element_located((
#                 By.XPATH, x_arg
#             )))
#         except:
#             # If contact not found, then search for it
#             searBoxPath = '//*[@id="input-chatlist-search"]'
#             wait.until(EC.presence_of_element_located((
#                 By.ID, "input-chatlist-search"
#             )))
#             inputSearchBox = driver.find_element_by_id("input-chatlist-search")
#             time.sleep(0.5)
#             # click the search button
#             driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div/button').click()
#             time.sleep(1)
#             inputSearchBox.clear()
#             inputSearchBox.send_keys(target[1:len(target) - 1])
#             print('Target Searched')
#             # Increase the time if searching a contact is taking a long time
#             time.sleep(4)

#         # Select the target
#         driver.find_element_by_xpath(x_arg).click()
#         print("Target Successfully Selected")
#         time.sleep(2)

#         # Select the Input Box
#         inp_xpath = "//div[@contenteditable='true']"
#         input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
#         time.sleep(1)

#         # Send message
#         # taeget is your target Name and msgToSend is you message
#         input_box.send_keys("Hello, " + target + "."+ Keys.SHIFT + Keys.ENTER + msgToSend[count][3] + Keys.SPACE) # + Keys.ENTER (Uncomment it if your msg doesnt contain '\n')
#         # Link Preview Time, Reduce this time, if internet connection is Good
#         time.sleep(10)
#         input_box.send_keys(Keys.ENTER)
#         print("Successfully Send Message to : "+ target + '\n')
#         time.sleep(0.5)

#     except:
#         # If target Not found Add it to the failed List
#         print("Cannot find Target: " + target)
#         failList.append(target)
#         pass


# send_message(wait, 'Ward van Hoof', 'test 123')

# wait = WebDriverWait(driver, 5)
# driver.quit()
# exit()

# # Count variable to identify the number of messages to be sent
# count = 0
# while count<len(msgToSend):

#     # Identify time
#     curTime = datetime.datetime.now()
#     curHour = curTime.time().hour
#     curMin = curTime.time().minute
#     curSec = curTime.time().second

#     # if time matches then move further
#     if msgToSend[count][0]==curHour and msgToSend[count][1]==curMin and msgToSend[count][2]==curSec:
#         # utility variables to tract count of success and fails
#         success = 0
#         sNo = 1
#         failList = []

#         # Iterate over selected contacts
#         for target in list_target:
#             print(sNo, ". Target is: " + target)
#             sNo+=1
#             try:
#                 # Select the target
#                 x_arg = '//span[contains(@title,' + target + ')]'
#                 try:
#                     wait5.until(EC.presence_of_element_located((
#                         By.XPATH, x_arg
#                     )))
#                 except:
#                     # If contact not found, then search for it
#                     searBoxPath = '//*[@id="input-chatlist-search"]'
#                     wait5.until(EC.presence_of_element_located((
#                         By.ID, "input-chatlist-search"
#                     )))
#                     inputSearchBox = driver.find_element_by_id("input-chatlist-search")
#                     time.sleep(0.5)
#                     # click the search button
#                     driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div/div[2]/div/button').click()
#                     time.sleep(1)
#                     inputSearchBox.clear()
#                     inputSearchBox.send_keys(target[1:len(target) - 1])
#                     print('Target Searched')
#                     # Increase the time if searching a contact is taking a long time
#                     time.sleep(4)

#                 # Select the target
#                 driver.find_element_by_xpath(x_arg).click()
#                 print("Target Successfully Selected")
#                 time.sleep(2)

#                 # Select the Input Box
#                 inp_xpath = "//div[@contenteditable='true']"
#                 input_box = wait.until(EC.presence_of_element_located((
#                     By.XPATH, inp_xpath)))
#                 time.sleep(1)

#                 # Send message
#                 # taeget is your target Name and msgToSend is you message
#                 input_box.send_keys("Hello, " + target + "."+ Keys.SHIFT + Keys.ENTER + msgToSend[count][3] + Keys.SPACE) # + Keys.ENTER (Uncomment it if your msg doesnt contain '\n')
#                 # Link Preview Time, Reduce this time, if internet connection is Good
#                 time.sleep(10)
#                 input_box.send_keys(Keys.ENTER)
#                 print("Successfully Send Message to : "+ target + '\n')
#                 success+=1
#                 time.sleep(0.5)

#             except:
#                 # If target Not found Add it to the failed List
#                 print("Cannot find Target: " + target)
#                 failList.append(target)
#                 pass

#         print("\nSuccessfully Sent to: ", success)
#         print("Failed to Sent to: ", len(failList))
#         print(failList)
#         print('\n\n')
#         count+=1
