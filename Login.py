#Login
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
#Line
from flask import Flask
from flask import Flask, request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from RSA_File import Write_and_Export

app = Flask(__name__)

#token
line_bot_api = LineBotApi('AeXTgftCbK2BDogofsoXbMObgU3TaL1fCMtuxtU94u7MlFkIeEXoNNR4RGIi9CdYC4vaq3lp4/SnBjWGcHLhMfUKS3qvahcB25af0td3K8xEckO48OC+UXuJMkXW75yfaVXE84tyZ5JaprzbglFsEQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2d77a86e124cc8b38d427613455d11ab') #Channel secret

#url_test = "https://itouch.cycu.edu.tw/active_system/query_course/learning_activity_stusign.jsp?act_no=4af01134-1881-42cb-b550-6626dd59b918&afterLogin=true"

emoji1 = [
    {
        "index": 0,
        "productId": "5ac21c46040ab15980c9b442",
        "emojiId": "008"
    }
]
emoji2 = [
    {
        "index": 33,
        "productId": "5ac21e6c040ab15980c9b444",
        "emojiId": "020"
    }
]

class Student:

    def __init__(self, user = None, passwd = None):
        self.user = user
        self.passwd = passwd

class chrome:

    def option():

        global driver

        options = webdriver.ChromeOptions()

        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36")
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('disable-dev-shm-usage')
        options.add_argument('blink-settings=imagesEnabled=false')
        # no screen
        options.add_argument('--headless') 
        # no pop up
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        print("Initializing....")

        driver = webdriver.Chrome(options = options, executable_path=ChromeDriverManager().install())
    
    def Open_Page(url):

        try:
            driver.get(url)
            #print("I successfully parser to Login page...")
            return True

        except:
            print("Open page failed")
            return False

    def Login(person):

        driver.find_element(By.ID, 'UserNm').clear()
        driver.find_element(By.ID, 'UserPasswd').clear()
        driver.find_element(By.ID, 'UserNm').send_keys(person.user)
        driver.find_element(By.ID, 'UserPasswd').send_keys(person.passwd)
        #print("enter" + person.user + "information successfully")

        print("Logging " + person.user)
        driver.find_element(By.NAME, 'Submit').click()
        return chrome.Login_check(person.user)

    def Login_check(user):

        global Login_information
        
        try:
            Wait(driver, 1)

            error = driver.switch_to.alert
            msg = error.text
            print(msg)
            error.accept()
            print("press error accept botton")
            Login_information.append(user + " " + msg) 

            return False

        except:
            print("successful")
            return True

def start_Login(url):

    global Login_information
    Login_information = []
    Login_information.clear()
    students = []
    students.clear()
    #students = Build.data("getall")
    students = Write_and_Export().export()
    if (students == None): return "no student here, please signup first!"
    chrome.option()
    type = chrome.Open_Page(url)

    for i in range (0, len(students)):

        if (type): 

            mode = chrome.Login(students[i])
            

            if (mode == True):
                
                Wait(driver, 3).until(EC.new_window_is_opened)
                status = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div').text
                print(status)
                if (status[0:4] == "簽到完成"): 
                    Login_information.append(students[i].user + " " + status[0:4])
                elif (status[0:6] == "非本課程學生"):
                    Login_information.append(students[i].user + " " + status[0:6])
                else:
                    Login_information.append(students[i].user + " " + status)

                driver.back()
                #print("Backing...")

                try: 
                    error = driver.switch_to.alert.accept()
                
                except:
                    Wait(driver, 3).until(EC.new_window_is_opened)
                    driver.refresh()
                    #print("refreshing...")


        else: break

        
    print("Driver closing...")
    driver.quit()

    return Login_information

def store_information(list):

    All = "Login Result\n"

    for i in range (0, len(list)):

        All += list[i] + '\n'

    All += "你各位可以去睡了"

    return All

@app.route("/callback", methods=['POST'])
def callback():

    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:

        handler.handle(body, signature)

    except InvalidSignatureError:

        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    
    if isinstance(event.message, TextMessage):

        mtext = event.message.text
        userid = event.source.user_id
        #groupid = event.source.group_id

        global person
        global status

        if mtext[0:26] == "https://itouch.cycu.edu.tw":

            status = 0

            line_bot_api.reply_message(event.reply_token, TextSendMessage("$Your URL is Vaild, Logining...", emojis = emoji1))

            information = start_Login(mtext)

            if (type(information) == type("string")):

                line_bot_api.push_message(userid, TextSendMessage(information))

            else:

                msg = store_information(information)

                line_bot_api.push_message(userid, TextSendMessage(msg))

                information.clear()

        elif mtext == 'help' or mtext == 'Help':

            line_bot_api.reply_message(event.reply_token, TextSendMessage("$You don't need help\nTo Sign Up, Press Sign Up botton\nYour password will use RSA1024bits to Encrypt!", emojis = emoji1))
            status = 0

        elif mtext == 'list' or mtext == 'List':
            
            lists = Write_and_Export().export()
            if (lists == None):
                line_bot_api.reply_message(event.reply_token, TextSendMessage("To Sign Up, Press Sign Up botton $", emojis = emoji2))
            else:

                lists_user_msg = "*****Account*****\n"

                for i in range (0, len(lists)):

                    lists_user_msg += "\U0001F449 " + lists[i].user + " \U0001F448" +'\n'

                lists_user_msg += "****End of List****"

                line_bot_api.reply_message(event.reply_token, TextSendMessage(lists_user_msg))

            status = 0
            line_bot_api.push_message(userid, TextSendMessage("To Sign Up, Press Sign Up botton $", emojis = emoji2))

        elif mtext == 'SignUp' or mtext == 'S':

            line_bot_api.reply_message(event.reply_token, TextSendMessage("$Please input Your\nStudentID%Password%\nEx:10828152%password%", emojis = emoji1))
            

        elif len(mtext) >= 12 and mtext[len(mtext)-1] == '%':
            
            size = len(mtext)
            person = (Student(mtext[0 : 8], mtext[9 : size - 1]))
            print(person)
            Write_and_Export().store(person)
            line_bot_api.reply_message(event.reply_token, TextSendMessage("$Sign Up Successfully", emojis = emoji1))
        
        else:

            line_bot_api.reply_message(event.reply_token, TextSendMessage("$Shut Up!", emojis = emoji1))
            status = 0

if __name__ == '__main__':

    app.run()
