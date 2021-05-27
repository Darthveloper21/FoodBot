import json
import re
from time import sleep

from requests_html import HTMLSession
from selenium import webdriver as wb

session = HTMLSession()
text_re = r"jsonData = (.*);"
regex = r"initData = (.*);"


def crawl_cmt(link):
    driver = wb.Chrome(executable_path='chromedriver.exe')
    driver.get(link)
    while True:
        try:
            clickObj = driver.find_elements_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/a')
            clickObj[0].click()
        except:
            print("Load full cmt")
            break
    full_cmt = driver.find_elements_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[1]/div/ul')

    full_cmt_by_text = ''
    for k in full_cmt:
        full_cmt_by_text = full_cmt_by_text + k.text
    driver.close()
    return full_cmt_by_text


def get_full_menu(store_link):
    driver1 = wb.Chrome(executable_path='chromedriver.exe')
    driver1.get(store_link)
    sleep(10)
    menu_data = driver1.find_elements_by_xpath('/html/body/div[1]/div/div[5]/div[1]/div[2]/div/div[2]')
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

    for cmt in menu_list:
        if cmt == "MENU":
            continue
        elif cmt == "Giá đã bao gồm tiền hộp mang về":
            cur['details'] = cmt
        elif cmt.startswith("+"):
            continue
        else:
            if count_param == 0:
                cur['name'] = cmt
            elif count_param == 1:
                cur['price'] = cmt
            count_param += 1
            if count_param == 2:
                res['data'].append(cur)
                count_param = 0

    return res


"""
    Function name: Get_cmt
    parse comment
    :param val: Str
    :return: res: dict:
    Format: {"data": [<sub_format>]}
    Sub_format:
        name: Str: customer name
        rate: Float: customer rate for diner
        device: customer device use to comment
        cmt: content of the comment
    """


def get_cmt(val):
    cmt_list = str.split(val, '\n')
    res = {'data': []}
    cur = {'details': None}
    count_param = 0

    for cmt in cmt_list:
        if cmt == "Thích" or cmt == "Thảo luận" or cmt == "Báo lỗi":
            if count_param > 0:
                res['data'].append(cur)
                cur = {'details': None}
                count_param = 0
        elif cmt.startswith("- Đây"):
            cur['details'] = cmt
            res['data'].append(cur)
            cur = {'details': None}
            count_param = 0
        else:
            if count_param == 0:
                if len(cmt) != 3:
                    continue
                cur['rate'] = float(cmt)
            elif count_param == 1:
                cur['name'] = cmt
            elif count_param == 2:
                cur['device'] = cmt
            elif count_param == 3:
                cur['cmt'] = cmt
            elif count_param > 3:
                cur['cmt'] += cmt
            count_param += 1

    return res


def get_full_information(store_link):
    link_foody_store = 'https://www.foody.vn{}'.format(store_link)
    link_menu = 'https://www.now.vn{}'.format(store_link)
    cmt = crawl_cmt(link_foody_store)
    menu = get_full_menu(link_menu)
    rb = session.get(link_foody_store)
    store_inf_text_link: str = rb.text
    # print(text_re.match(text_str))
    matches = re.finditer(regex, store_inf_text_link, re.MULTILINE)
    need_data = ''
    for matchNum, match in enumerate(matches, start=1):
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            need_data = match.group(groupNum)
    # print(r.text)
    data = json.loads(need_data)
    time_do = []
    for k in data['OpeningTime']:
        time_do.append('{}'.format(k['TimeOpen']['Hours']) + ':' + '{}'.format(
            k['TimeOpen']['Minutes']) + '-' + '{}'.format(k['TimeClose']['Hours']) + ':' + '{}'.format(
            k['TimeClose']['Minutes']))

    review_point = []
    for point in data['AvgPointList']:
        review_point.append({point['Label']: point['Point']})
    try:
        information = {
            'name': data['Name'],
            'address': data['Address'],
            'city': data['City'],
            'district': data['District'],
            'priceMin': data['PriceMin'],
            'priceMax': data['PriceMax'],
            'Time': time_do,
            'review_point': review_point,
            'menu': get_menu(menu),
            'cmt': get_cmt(cmt),
            'website': link_foody_store,
        }
    except IOError:
        print("Error")
        information = None
    return information


link_store = [
    'link_store_bún',
    'link_store_cơm',
    'link_store_phở',
]
if __name__ == '__main__':
    with open('link_store_bun.txt', 'r', encoding='utf-8') as f:
        cnt = 0
        for line in f:
            line = line.strip('\n')
            diner_name = line.split("/")[-1]
            try:
                value = get_full_information(line)
                file = open(diner_name + ".json", "w", encoding="utf-8")
                try:
                    json.dump(value, file, ensure_ascii=False, indent=4)
                except IOError:
                    print("vkl")
            except:
                continue