import re
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import math

def CreateDriver():
    options = webdriver.ChromeOptions()
    options.add_argument("--enable-javascript")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.headless = True

    driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
    driver.implicitly_wait(3)

    return driver


def volumePerMeg(package_volume_info):
    if 'صبحانت' in package_volume_info or 'نامحدود'in package_volume_info :
        return 0
    tmp = package_volume_info.split('بایت')[0].strip()
    val = float( re.match( r'([-+]?\d*\.\d+|\d+) .+', tmp ).group(1) )
    if 'گیگا' in tmp :
        val *= 1024
    return val

def AddItem(df1, df2, MyID, li):
    content = li.find_all('div', class_='package-list-item-content-block')

    package_volume_info = content[0].find('div').text
    package_price = content[2].find('div').text
    ussd_code_block= content[3].find('div').text

    df1.loc[0 if pd.isnull(df1.index.max()) else df1.index.max() + 1] = [package_volume_info, package_price, ussd_code_block]
    MyID += 1

    vol = volumePerMeg(package_volume_info)
    if not vol :
        return MyID

    package_price = content[2].find('div').text
    price = int( ''.join( re.match( r'(.*) تومان ', package_price ).group(1).strip().split(',') ) )

    df2.loc[0 if pd.isnull(df2.index.max()) else df2.index.max() + 1] = [MyID, vol, price]
    return MyID


def MciScrap():
    url = "https://mci.ir/notrino-plans"
    driver = CreateDriver()

    driver.get(url) 

    # this is just to ensure that the page is loaded
    time.sleep(5) 

    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc, 'html5lib')

    page_list_info = soup.find('p', class_='page-list-info text-center').text
    pat = re.match( r'.* (\d+) .* (\d+) .* (\d+) .*', page_list_info )
    num = math.floor( int( pat.group(3) ) / int( pat.group(2) ) )

    df1 = pd.DataFrame(columns = ['package_volume_info', 'package_price', 'ussd_code_block'])
    df2 = pd.DataFrame(columns = ['id', 'package_volume_info', 'package_price'])
    MyID = -1

    lis = soup.find_all('li', class_='package-list-item')
    for li in lis :
        MyID = AddItem(df1, df2, MyID, li)

    for i in range(num):
        element = driver.find_element_by_id('nextPageList')
        driver.execute_script("arguments[0].click();", element)

        html_doc = driver.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        lis = soup.find_all('li', class_='package-list-item')

        for li in lis :
            MyID = AddItem(df1, df2, MyID, li)

    driver.close()

    df1.to_csv("mci.csv", index=False)

    return df1, df2 
