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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('proxy_list.txt', 'r') as file:
    proxy_ips = file.read().splitlines()

keyword= "hololive"
page= 17
ecode = "utf-8-sig"
my_headers = {'if-none-match-': '55b03-6d83b58414a54cb5ffbe81099940f836',
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
    'X-Sap-Access-F': "3.0.0.6.0|13|2.4.12_5.1.0_0_187|d7fdb0e639214ead93fc55232d583a5672d3fc79a4974e|10900|1100",   
    'X-Sap-Access-S': "MUZALjKcrgAuyFpkJuSsYBpwPHzjuPHbPVu1IfSJeJA=",  
    'X-Sap-Access-T': "1667569629",   
    'af-ac-enc-dat': "null"
    }    
#自動裝chromedriver
service = ChromeService(executable_path=ChromeDriverManager().install())
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs",prefs)
#開啟視窗
options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome()
time.sleep(random.randint(5,10))

def wrong_url(url):
    time.sleep(1)
    if driver.current_url != url:
        return 1

def has_digit(input_string):
    for char in input_string:
        if char.isdigit():
            return True
    return False

def login(Email,password):
    Email = driver.find_element("name","loginKey")
    Email.send_keys("your mail")
    password = driver.find_element("name","password")
    password.send_keys("your password")
    password.send_keys(Keys.RETURN)
    
def find_index(x):
    for abc, item in enumerate(x):
        if '$' in item and '折' not in item :
            return abc
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

def find_data1(url):
    driver.get(url)
    time.sleep(random.randint(5,10))
    try:
        login(1,2)
    except:
        pass
    if wrong_url(url=url) == 1:
        a = "找不到商品"
        return a
    try:
        r = driver.find_element(by=By.CLASS_NAME,value="pqTWkA")
    except:
        r = None
    if r != None:
        wait = WebDriverWait(driver, 10) 
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pqTWkA")))
        a = element.text
        return a
    else:
        a = "找不到商品"
        return a

def find_data2(url):
    current_url = driver.current_url
    if url != current_url:
        driver.get(url)
        time.sleep(random.randint(5,10))
    try:
        login(1,2)
    except:
        pass
    if wrong_url(url=url) == 1:
        b = "找不到商品"
        return b
    try:
        r = driver.find_element(by=By.CLASS_NAME,value="MCCLkq")
    except:
        r = None
    if r != None:
        wait = WebDriverWait(driver, 10) 
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "MCCLkq")))
        a = element.text.split()
        for b in a:
            if '市' in b or '縣' in b or b == '中國大陸':
                return b
        return '無資料'
    else:
        b = "找不到商品"
        return b

def find_data3(url):
    current_url = driver.current_url
    if url != current_url:
        driver.get(url)
        time.sleep(random.randint(5,10))
    try:
        login(1,2)
    except:
        pass
    if wrong_url(url=url) == 1:
        b = "找不到商品"
        return b
    try:
        r = driver.find_element(by=By.CLASS_NAME,value="flex.eaFIAE")
    except:
        r = None
    if r != None:
        wait = WebDriverWait(driver, 10) 
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "flex.eaFIAE")))
        zun = element.text
        parts = zun.split("已售出")
        c = "已售出 " + parts[0]  
        return c
    else:
        c = "找不到商品"
        return c
def find_data4(url):
    current_url = driver.current_url
    if url != current_url:
        driver.get(url)
        time.sleep(random.randint(5,10))
    try:
        login(1,2)
    except:
        pass
    try:
        r = driver.find_element(by=By.CLASS_NAME,value="flex.items-center._6lioXX")
    except:
        r = None
    if r != None:
        wait = WebDriverWait(driver, 10) 
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "flex.items-center._6lioXX")))
        a = element.text.split()
        print(a)
        for df in a:
            if '還剩' in df:
                return df
        return '無資料'
    else:
        d = '無資料'
        return d
    
print('~~~~~~~~~開始進行爬蟲~~~~~~~~~')
#第一階段:先抓不需要進商品頁面就抓的到的東西
container_product = pd.DataFrame()
tStart = time.time()#計時開始
for i in tqdm(range(int(page))): #tqdm=進度條 for迴圈跑page次   
    # 準備用來存放資料的陣列
    itemid = []
    shopid =[]
    name = []
    link = []
    price = []
    place_of_goods = []
    Sales_volume = []
    Number_of_Products = []
    Total_Rating = []
    Chat_Response_Rate = []
    Join_Time = []
    Chat_Response_Speed = []
    fans = []
    driver.get('https://shopee.tw/search?keyword=' + keyword + '&page=' + str(i))
    time.sleep(random.randint(5,10))
    try:
        login(1,2)
    except:
        pass
    # 滾動頁面
    for scroll in range(6):
        driver.execute_script('window.scrollBy(0,1000)')
        time.sleep(random.randint(5,10))
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
        Number_of_Products.append('NaN')
        Total_Rating.append('NaN')
        Chat_Response_Rate.append('NaN')
        Join_Time.append('NaN')
        Chat_Response_Speed.append('NaN')
        fans.append('NaN')
        
    dic = {
    '商品ID':itemid,
    '賣家ID':shopid,
    '商品名稱':name,
    '商品連結':link,
    '價格':price,
    '出貨地':place_of_goods,
    '銷售量':Sales_volume,
    '商品數量':Number_of_Products,
    '商品總評價':Total_Rating,
    '聊聊回應率':Chat_Response_Rate,
    '商家加入時間':Join_Time,
    '聊聊回應速度':Chat_Response_Speed,
    '粉絲':fans,
    }
    #資料整合
    container_product = pd.concat([container_product,pd.DataFrame.from_dict(dic,orient='index')], axis=1)
    #存檔
    container_product.drop(container_product.columns[[-4,-3,-2,-1]], axis=1, inplace=True)
    container_product.to_csv('E:/新增資料夾/python/真正的實作/'+keyword +str(i+1)+'_商品資料.csv', encoding = ecode)
    getData = pd.read_csv('E:/新增資料夾/python/真正的實作/'+keyword +str(i+1)+'_商品資料.csv')
    getData = getData.transpose()
    getData.columns = getData.iloc[0]
    getData = getData[1:]
    getData.to_csv('E:/新增資料夾/python/真正的實作/'+keyword +str(i+1)+'_商品資料.csv', index=False)
os.rename('E:/新增資料夾/python/真正的實作/'+keyword +str(page)+'_商品資料.csv','E:/新增資料夾/python/真正的實作/'+keyword+'_第一階段商品資料.csv')

tEnd = time.time()#計時結束
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('第一階段商品資料儲存完成，花費時間： ' + str(minute) + ' 分 ' + str(second) + '秒')
print("正在準備進行第二階段...")
time.sleep(2)

#第二階段:把第一階段沒抓到的東西補抓下來
print('~~~~~~~~~開始進行爬蟲~~~~~~~~~')
tStart = time.time()#計時開始
itemDetail = ''
getlostData = pd.read_csv('E:/新增資料夾/python/真正的實作/'+keyword+'_第一階段商品資料.csv')
driver.get('https://shopee.tw/INTEL%E5%85%A8%E6%96%B012%E4%BB%A3I5%E9%9B%BB%E8%85%A6%E4%B8%BB%E6%A9%9F16G-500G%E6%A5%B5%E9%80%9FSSD-WIN11%E5%AE%89%E5%8D%93%E9%9B%99%E7%B3%BB%E7%B5%B1-%E5%8F%AF%E5%8D%87%E7%8D%A8%E7%AB%8B%E9%A1%AF%E5%8D%A1I7-I9-%E5%88%B0%E5%BA%9C%E6%94%B6%E9%80%81%E4%BF%9D%E5%9B%BA-i.17001426.12784378460')
for r in tqdm(range(688,len(getlostData))):
    data = []
    data.append(getlostData.iloc[r]['商品連結'])
    if getlostData.iloc[r]['價格'] != '暫無資料':
        if getlostData.iloc[r]['出貨地'] != '暫無資料':
            if getlostData.iloc[r]['銷售量'] != '暫無資料':
                pass #三樣都有
            else: 
                itemDetail = find_data3(url=data[0])
                getlostData.at[r,'銷售量'] = itemDetail
        else:
            if getlostData.iloc[r]['銷售量'] != '暫無資料': 
                itemDetail = find_data2(url=data[0])
                getlostData.at[r,'出貨地'] = itemDetail

            else: 
                itemDetail = find_data2(url=data[0])
                getlostData.at[r,'出貨地'] = itemDetail
                itemDetail = find_data3(url=data[0])
                getlostData.at[r,'銷售量'] = itemDetail
    else:
        if getlostData.iloc[r]['出貨地'] != '暫無資料':
            if getlostData.iloc[r]['銷售量'] != '暫無資料': 
                itemDetail = find_data1(url=data[0])
                getlostData.at[r,'價格'] = itemDetail
            else:
                itemDetail = find_data1(url=data[0])
                getlostData.at[r,'價格'] = itemDetail
                itemDetail = find_data3(url=data[0])
                getlostData.at[r,'銷售量'] = itemDetail
        else:
            if getlostData.iloc[r]['銷售量'] != '暫無資料': 
                itemDetail = find_data1(url=data[0])
                getlostData.at[r,'價格'] = itemDetail
                itemDetail = find_data2(url=data[0])
                getlostData.at[r,'出貨地'] = itemDetail
            else: 
                itemDetail = find_data1(url=data[0])
                getlostData.at[r,'價格'] = itemDetail
                itemDetail = find_data2(url=data[0])
                getlostData.at[r,'出貨地'] = itemDetail
                itemDetail = find_data3(url=data[0])
                getlostData.at[r,'銷售量'] = itemDetail
    itemDetail = find_data4(url=data[0])
    getlostData.at[r,'商品數量'] = itemDetail
    current_url = driver.current_url
    url = data[0]
    if url != current_url:  
        driver.get(url)
        time.sleep(random.randint(5,10))
    try:
        login(1,2)
    except:
        pass
    try:
        v = driver.find_element(by=By.CLASS_NAME,value="Po6c6I")
    except:
        v = None
    if v != None:
        wait = WebDriverWait(driver, 10) 
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Po6c6I")))
        a = element.text.split()
        print(a)
        if a != '':
            w = a.index('商品評價')
            if has_digit(a[w+1]):
                a[w+1] = a[w+1].replace('萬','000')
                getlostData.at[r,'商品總評價']=a[w+1]
            else:
                getlostData.at[r,'商品總評價']='無資料'

            w = a.index('聊聊回應率')
            if has_digit(a[w+1]):
                getlostData.at[r,'聊聊回應率']=a[w+1]
            else:
                getlostData.at[r,'聊聊回應率']='無資料'

            w = a.index('加入時間')
            if has_digit(a[w+1]):
                getlostData.at[r,'商家加入時間']=a[w+1]
            else:
                getlostData.at[r,'商家加入時間']='無資料'

            w = a.index('回應速度')
            if a[w+1] != '粉絲':
                getlostData.at[r,'聊聊回應速度']=a[w+1]
            else:
                getlostData.at[r,'聊聊回應速度']='無資料'

            w = a.index('粉絲')
            if w+1 <= len(a):
                a[w+1] = a[w+1].replace('萬','000')
                getlostData.at[r,'粉絲']=a[w+1]
            else:
                getlostData.at[r,'粉絲']='無資料'
        else:
            for f in ['商品評價','聊聊回應率','商家加入時間','聊聊回應速度','粉絲']:
               getlostData.at[r,f]='無資料'     
        getlostData.to_csv('E:/新增資料夾/python/真正的實作/'+keyword+'_第二階段商品資料.csv', index=False)
        print(str(getlostData.loc[r]))
l = -1
for g in range(len(getlostData)):
    l = l+1
    if getlostData.iloc[g]['銷售量'] == '暫無資料':
        getlostData.loc[g, '銷售量'] = '已售出 0'

    if getlostData.iloc[g]['銷售量'] == "找不到商品" or getlostData.iloc[g]['價格'] == "找不到商品" or getlostData.iloc[g]['出貨地'] == "找不到商品":
        print(getlostData.iloc[g]['銷售量'])
        print(getlostData.iloc[g]['價格'])
        print(getlostData.iloc[g]['出貨地'])
        getlostData = getlostData.drop(l)

frame = pd.read_csv('E:/新增資料夾/python/真正的實作/'+keyword+'_第二階段商品資料.csv')
subset_columns = ['賣家ID', '商品名稱', '價格', '出貨地', '銷售量']
data = frame.drop_duplicates(subset=subset_columns, keep='first', inplace=False)
data.to_csv('E:/新增資料夾/python/真正的實作/'+keyword+'_第二階段商品資料.csv', index=False)
tEnd = time.time()#計時結束
totalTime = int(tEnd - tStart)
minute = totalTime // 60
second = totalTime % 60
print('第二階段商品資料儲存完成，花費時間： ' + str(minute) + ' 分 ' + str(second) + '秒')
for p in range(page-1):
    os.remove('E:/新增資料夾/python/真正的實作/'+keyword +str(p+1)+'_商品資料.csv')
os.remove('E:/新增資料夾/python/真正的實作/'+keyword+'_第一階段商品資料.csv')
driver.close()
