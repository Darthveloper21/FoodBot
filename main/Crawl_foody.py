import json
import re
import os
from time import sleep

from requests_html import HTMLSession
from selenium import webdriver as wb

session = HTMLSession()
text_re = r"jsonData = (.*);"
regex = r"initData = (.*);"

options = wb.ChromeOptions()


def crawl_cmt(link, driver_path):
    driver = wb.Chrome(executable_path=driver_path, options=options)
    driver.get(link)
    while True:
        try:
            clickObj = driver.find_elements_by_xpath(
                '/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/a')
            clickObj[0].click()
        except IndexError:
            print("Load full cmt")
            break
    full_cmt = driver.find_elements_by_xpath(
        '/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[1]/div/ul')

    full_cmt_by_text = ''
    for k in full_cmt:
        full_cmt_by_text = full_cmt_by_text + k.text
    driver.close()
    return full_cmt_by_text


def get_full_menu(store_link, driver_path):
    driver1 = wb.Chrome(executable_path=driver_path, options=options)

    driver1.get('chrome://settings/')
    driver1.execute_script('chrome.settingsPrivate.setDefaultZoom(0.1);')
    sleep(1)
    driver1.get(store_link)
    sleep(1)

    # change zoom for web driver
    sleep(1)
    driver1.execute_script("document.body.style.zoom='50%'")
    driver1.get(store_link)
    sleep(1)

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


def get_full_information(store_link, driver_path):
    link_foody_store = 'https://www.foody.vn{}'.format(store_link)
    link_menu = 'https://www.now.vn{}'.format(store_link)
    # cmt = crawl_cmt(link_foody_store, driver_path)
    menu = get_full_menu(link_menu, driver_path)
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
            # 'cmt': get_cmt(cmt),
            'website': link_foody_store,
        }
    except IOError:
        print("Error")
        information = None
    return information


def crawl_data_from(data_link: str, dest_link: str, driver_path: str, limit: int = 500, path_id: int = 0):
    print("Crawl Data from {}, save to {}, limit by {}".format(data_link, dest_link, limit))
    with open(data_link, 'r', encoding='utf-8') as f:
        cnt = 0
        t = f.read()
        s = t.count('\n')
        start = int(s / 100) * path_id

        t = t.split("\n")

        for i, line in enumerate(t):
            if i < start:
                continue
            elif i >= int(s / 100) * (path_id + 1):
                break
            elif cnt >= limit:
                break

            line = line.strip('\n')
            diner_name = line.split("/")[-1]

            try:
                file = open(dest_link + "/" + diner_name + ".json", "w", encoding="utf-8")
                value = get_full_information(line, driver_path)
                try:
                    json.dump(value, file, ensure_ascii=False, indent=4)
                    cnt += 1
                    if cnt >= limit:
                        break
                except IOError:
                    print("Some error occur at " + diner_name)
            except Exception as e:
                print(str(e))
            finally:
                file.close()


def crawl(load_data_path: str, save_data_path: str, driver_path: str, limit: int, path_id: int = 0):
    if not os.path.exists(load_data_path):
        raise Exception("Data path not found")
    if not os.path.exists(save_data_path):
        os.mkdir(save_data_path)

    slist = os.listdir(load_data_path)

    for name in slist:
        filename, ext = os.path.splitext(name)
        if not os.path.exists(save_data_path + "/" + filename + "_{}".format(str(path_id))):
            os.mkdir(save_data_path + "/" + filename + "_{}".format(str(path_id)))
        current_save_data_path = save_data_path + "/" + filename + "_{}".format(str(path_id))
        crawl_data_from(load_data_path + "/" + name, current_save_data_path, driver_path, limit=limit, path_id=path_id)


def craw_in_range(load_data_path: str, save_data_path: str, driver_path: str,
                  limit: int, left: int = 0, right: int = 100):
    for i in range(left, right + 1):
        print("Start crawl at epoch {}".format(str(i)))
        crawl(load_data_path, save_data_path, driver_path, limit, i)
        print("Complete crawl at epoch {}".format(str(i)))
