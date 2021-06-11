import json
import re
import os
from time import sleep

from requests_html import HTMLSession
from selenium import webdriver as wb
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

session = HTMLSession()
text_re = r"jsonData = (.*);"
regex = r"initData = (.*);"

options = wb.ChromeOptions()


def get_full_menu(store_link):
    print("Vẫn Chạy trong im lặng...")
    driver1 = wb.Chrome(executable_path='D:/Web/FoodBot/chromedriver.exe', options=options)

    print("Chạy xong, đang setting...")
    driver1.get('chrome://settings/')
    driver1.execute_script('chrome.settingsPrivate.setDefaultZoom(0.1);')
    sleep(1)
    print("Lấy data...")
    driver1.get(store_link)
    sleep(1)
    driver1.save_screenshot('normal.png')

    print("Lấy data xong, đang zoom...")

    print("Zoom xong, đang chạy script thu nhỏ 1%...")
    # change zoom for web driver
    sleep(1)
    driver1.save_screenshot('zoomed.png')
    driver1.execute_script("document.body.style.zoom='50%'")
    driver1.get(store_link)
    print("Chạy script thu nhỏ xong rồi.")
    sleep(1)
    driver1.save_screenshot('zoomed2.png')

    menu_data = driver1.find_elements_by_class_name('item-restaurant-row')
    menu: str = ''
    for k in menu_data:
        menu = menu + k.text
    driver1.close()
    return menu


"""
    Function name: Get_menu
    :param val: Str
    :return:  res: dict
    Format: {"data": [<sub_format>]}
    Sub_format:
        name: Str: dish's name
        price: Str: dish's price
        details: Str: additional information about dishes
    """

def get_menu(val):
    menu_list = str.split(val, '\n')
    res = {'data': []}
    cur = {'details': None}
    count_param = 0

    print(menu_list)

    for cmt in menu_list:
        if count_param == 0:
            if cmt.startswith("+"):
                cur['name'] = cmt[1:]
                count_param += 1
            elif cmt.startswith("Hết hàng"):
                cur['name'] = cmt[8:]
                count_param += 1
            elif count_param == 0:
                cur['name'] = cmt
                count_param += 1
        elif count_param > 0:
            if '0' <= cmt[0] <= '9' and cmt[-1] == 'đ':
                cmt = cmt.replace(',', '')
                cur['price'] = cmt
                res['data'].append(cur)
                cur = {'details': None}
                count_param = 0
            else:
                cur['details'] = cmt

    return res



#print(get_menu(get_full_menu('https://www.now.vn/ha-noi/o-ga-com-ga-de-nhat')))
