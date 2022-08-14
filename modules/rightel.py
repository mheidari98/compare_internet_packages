import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
import time
import math

def fa2EnNum(number_string):
    number_string = number_string.replace(',', '')
    dic = {
        '۰' : 0,
        '۱' : 1,
        '٢' : 2,
        '۲' : 2,
        '۳' : 3,
        '٤' : 4,
        '۴' : 4,
        '۵' : 5,
        '٦' : 6,
        '۶' : 6,
        '۷' : 7,
        '۸' : 8,
        '۹' : 9,
    }
    num = 0
    for ch in number_string :
        num = num*10 + dic[ch]

    return num


def CreateDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True

    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
    driver.implicitly_wait(3)

    return driver


def rightel(allow_limited_packs=False):

    URL = "https://package.rightel.ir/ExtraPackageSales/ProductListToSales/ShowProduct"
    
    driver = CreateDriver()

    driver.get(URL) 

    # this is just to ensure that the page is loaded
    time.sleep(5) 

    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc, 'html5lib')

    df = pd.DataFrame(columns = ['type', 'package_volume_info', 'package_price', 'ussd_code_block'])

    packageTypes = ['pack-grid-item prepaid', 'pack-grid-item postpaid', 'pack-grid-item data']

    for pType in packageTypes :
        packages = soup.find_all('div',attrs={"class":pType})
        for package in packages :
            package_type = package.find('span').text
            package_volume_info = package.find('h2').text
            package_price_rial = package.find('span', class_='fix').text 
            try :
                ussd_code_block = package.find('span', class_='code').text 
            except :
                ussd_code_block = ''
            df.loc[0 if pd.isnull(df.index.max()) else df.index.max() + 1] = \
                        [package_type, package_volume_info, package_price_rial, ussd_code_block]

    df['package_price'] = df['package_price'].apply(lambda x: fa2EnNum(x)* 1.09) # 9% tax

    df = df.drop_duplicates(keep='first').reset_index(drop=True)

    df.to_csv("DB/rightel.csv", sep=',' , encoding='utf-8-sig', index=False)

    return df