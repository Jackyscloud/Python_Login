from flask import Flask
app = Flask(__name__)

from flask import Flask, request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from linebot.models import *
import re

from selenium import webdriver
import time

def bug(a):

    options = webdriver.ChromeOptions()

    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36")
    options.add_argument("--incognito")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('disable-dev-shm-usage')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--single-process')
    options.add_argument('--windows-size=1920,1080')
    #options.add_argument('blink-settings=imagesEnabled=false')
    # no screen
    options.add_argument('--headless') 
    # no pop up
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs",prefs)
    print("Initializing....")

    driver = webdriver.Chrome(options = options, executable_path=ChromeDriverManager().install())
    driver.get("http://www.google.com")
    #driver.close()
    #school = input()
    #driver.find_element_by_class_name("gLFyf.gsfi").send_keys( a + "附近美食")
    #driver.find_element(By.CLASS_NAME, 'gLFyf.gsfi').send_keys(a + "附近美食")
    #time.sleep(5)
    #button = driver.find_element_by_class_name("gNO89b")
    #button = Wait(driver, 10).until(EC.element_to_be_clickable(driver.find_element(By.NAME, 'btnK')))
    #button.click()
    elm = driver.find_element_by_css_selector('input[name="q"]')
    elm.send_keys(a + "附近美食")
    elm.send_keys(Keys.RETURN)

    #點更多資訊
    Wait(driver, 10).until(EC.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, '.tiS4rf.Q2MMlc'))).click()


    names = []
    allname = driver.find_elements_by_css_selector('.dbg0pd.eDIkBe span.OSrXXb')
    step = 0
    for name in allname: 
        if len(names) < 5 and step > 2:
            names.append(name.text)
        step = step + 1


    starstemp = []
    stars = []
    allstar = driver.find_elements_by_css_selector('span.YDIN4c.YrbPuc')
    #去除nan
    for i in range(0, len(allstar)):
        if (allstar[i].text != ""):
            stars.append(allstar[i].text)
        if (len(stars) == 5): break

    #print(stars)
    #print(names)
    #收集網址
    restaurantdata = []
    foodimages = []
    indata = driver.find_elements_by_css_selector('.C8TUKc.rllt__link.a-no-hover-decoration')
    step = 0
    for link in indata:
        if step < 5:
            Wait(driver, 10).until(EC.element_to_be_clickable(link)).click()
            time.sleep(3)
            allimage = driver.find_elements_by_css_selector('div.vwrQge')
            temp = allimage[0].get_attribute('outerHTML')
            #temp = re.search('(([^)]+)', temp).group(1)
            foodimages.append(temp[48:145]) 
            restaurantdata.append(driver.current_url)
            step += 1
        else:
            break
    rankname = []
    rankimg = []
    rankdata = []
    rankstar = sorted(stars)
    q = 0
    for i in range(5):#0~9
        if(i == 0):
            q = 0
        elif rankstar[i]==rankstar[i-1] :
            q = q + 1
        else:
            q = 0
        while q < 5:
            if(rankstar[i]==stars[q]):
                rankname.append(names[q])
                rankimg.append(foodimages[q])
                rankdata.append(restaurantdata[q])
                break
            q += 1
    print(rankname)
    driver.quit()
    return Carousel_Template(rankname, rankimg, rankstar, rankdata)

def Carousel_Template(name, image, grade, url):
    message = TemplateSendMessage(
        alt_text='一則旋轉木馬按鈕訊息',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url = image[4],
                    title=name[4],
                    text='餐廳評分為:' + grade[4],
                    actions=[
                        URITemplateAction(
                            label='餐廳連結',
                            uri=url[4]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = image[3],
                    title=name[3],
                    text='餐廳評分為:' + grade[3],
                    actions=[
                        URITemplateAction(
                            label='餐廳連結',
                            uri=url[3]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = image[2],
                    title=name[2],
                    text='餐廳評分為:' + grade[2],
                    actions=[
                        URITemplateAction(
                            label='餐廳連結',
                            uri=url[2]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = image[1],
                    title=name[1],
                    text='餐廳評分為:' + grade[1],
                    actions=[
                        URITemplateAction(
                            label='餐廳連結',
                            uri=url[1]
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url = image[0],
                    title=name[0],
                    text='餐廳評分為:' + grade[0],
                    actions=[
                        URITemplateAction(
                            label='餐廳連結',
                            uri=url[0]
                        )
                    ]
                )
            ]
        )
    )
    return message

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

line_bot_api = LineBotApi('AeXTgftCbK2BDogofsoXbMObgU3TaL1fCMtuxtU94u7MlFkIeEXoNNR4RGIi9CdYC4vaq3lp4/SnBjWGcHLhMfUKS3qvahcB25af0td3K8xEckO48OC+UXuJMkXW75yfaVXE84tyZ5JaprzbglFsEQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2d77a86e124cc8b38d427613455d11ab')

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    messagereply = bug(event.message.text)
    line_bot_api.reply_message(event.reply_token,messagereply)

if __name__ == '__main__':
    app.run()

