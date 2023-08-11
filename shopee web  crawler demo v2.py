import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import random
from tqdm import tqdm
import os

keyword= "電腦"
page= 17
ecode = "utf-8-sig"
my_headers = {'if-none-match-': '55b03-634508b9798ba9f4e118b697a946c895',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
    }    
#自動裝chromedriver
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
tStart = time.time()#計時開始
#開啟視窗
options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome()
time.sleep(random.randint(5,10))
#開啟網頁
driver.get("https://shopee.tw/buyer/login")
time.sleep(random.randint(5,10))

def login(Email,password):
    Email = driver.find_element("name","loginKey")
    Email.send_keys("your shopee email")   #@@@@
    password = driver.find_element("name","password")
    password.send_keys("your shopee name") #@@@@
    password.send_keys(Keys.RETURN)
    
def find_index(lst):
    for index, item in enumerate(lst):
        if '$' in item and '折' not in item :
            return index
    return '無資料'

def find_place_name(y):
    for edf, place_name in enumerate(y):
        if '市' in place_name or '縣' in place_name or place_name == '中國大陸':
            return edf
    return '無資料'

def find_Sales_volume(z):
    for ghi,Sales_volume_name in enumerate(z):
        if '已售出' in Sales_volume_name:
            return ghi
    return '無資料'

print('~~~~~~~~~~~開始爬蟲~~~~~~~~~~~')
container_product = pd.DataFrame()
tStart = time.time()#計時開始
for i in tqdm(range(int(page))): #tqdm=進度條 for迴圈跑page次
    itemid = []
    shopid =[]
    name = []
    link = []
    price = []
    place_of_goods = []
    Sales_volume = []
    driver.get('https://shopee.tw/search?keyword=' + keyword + '&page=' + str(i))
    time.sleep(random.randint(5,10))
    try:
        login(1,2)
    except:
        pass
    # 滾動頁面
    for scroll in range(6):
        driver.execute_script('window.scrollBy(0,1000)')
        time.sleep(random.randint(3,10))
    #取得商品內容
    for item, thename in zip(driver.find_elements(by=By.XPATH, value='//*[@data-sqe="link"]'), driver.find_elements(by=By.XPATH, value='//*[@data-sqe="name"]')):
        try:
            login(1,2)
        except:
            pass
        #商品名稱
        getname = thename.text.split('\n')[0]
        name.append(getname)
        try:
            login(1,2)
        except:
            pass
        #商品ID、商家ID
        getID = item.get_attribute('href')
        theitemid = (getID[getID.rfind('.')+1:])
        theshopid = (getID[ getID[:getID.rfind('.')].rfind('.')+1 :getID.rfind('.')])
        if 'sp_atk' in theitemid:
            itemid.append(theitemid)
            shopid.append(theshopid)
            link.append(getID)
        else:
            continue
        thecut = []
        thecontent = item.text
        try:
            login(1,2)
        except:
            pass  
        thecontent = thecontent[(thecontent.find(getname)) + len(getname):]
        thecontent = thecontent.replace('萬','000')
        thecut = thecontent.split('\n')
        print(thecut)
        result = None
        result = find_index(thecut)
        if result != '無資料' :
            theprice = thecut[result]
        else:
            theprice = '暫無資料'

        something = None
        something = find_place_name(thecut)
        if something != '無資料':
            theplaceofgoods = thecut[something]
            if '000' in theplaceofgoods:
                theplaceofgoods = theplaceofgoods.replace('000','萬')
        else:
            theplaceofgoods = '暫無資料'

        something2 = None
        something2 = find_Sales_volume(thecut)
        if something2 != '無資料' :
            thesalesvolume = thecut[something2]
        else:
            thesalesvolume = '暫無資料'

        place_of_goods.append(theplaceofgoods)
        price.append(theprice)
        Sales_volume.append(thesalesvolume)
        
    dic = {
    '商品ID':itemid,
    '賣家ID':shopid,
    '商品名稱':name,
    '商品連結':link,
    '價格':price,
    '出貨地':place_of_goods,
    '銷售量':Sales_volume
    }
    #資料整合
    container_product = pd.concat([container_product,pd.DataFrame.from_dict(dic,orient='index')], axis=0)
    #存檔
    container_product.drop(container_product.columns[[-4,-3,-2,-1]], axis=1, inplace=True)
    container_product.to_csv('C:/example/'+keyword +str(i+1)+'_商品資料.csv', encoding = ecode) #@@@@
    getData = pd.read_csv('C:/example/'+keyword +str(i+1)+'_商品資料.csv') #@@@@
    getData = getData.transpose()
    getData.columns = getData.iloc[0]
    getData = getData[1:]
    getData.to_csv('C:/example/'+keyword +str(i+1)+'_商品資料.csv', index=False) #@@@@

os.rename('C:/example/'+keyword +str(page)+'_商品資料.csv','C:/example/'+keyword+'_完整商品資料.xlsx') #@@@@
tEnd = time.time()#計時結束
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('商品資料儲存完成，花費時間（約）： ' + str(minute) + ' 分 ' + str(second) + '秒')