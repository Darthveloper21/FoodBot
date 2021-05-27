import json
import re

from requests_html import HTMLSession

session = HTMLSession()
text_re = r"jsonData = (.*);"
regex = r"initData = (.*);"


def get_list_store(topic, page):
    for stt in range(1, page):
        store_full_html = session.get(
            f'https://www.foody.vn/ha-noi/dia-diem?ds=Restaurant&vt=row&st=1&q={topic}&page={stt}&'
            f'provinceId=218&categoryId'
            '=&append=true')
        list_store_html: str = store_full_html.text
        # print(text_re.match(text_str))
        matches = re.finditer(text_re, list_store_html, re.MULTILINE)
        need_data = ''
        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                groupNum = groupNum + 1
                need_data = match.group(groupNum)
        # print(r.text)
        data = json.loads(need_data)
        f = open('link_store_{}.txt'.format(topic), mode='a+', encoding='utf-8')
        for k in data['searchItems']:
            if 'DetailUrl' in k and k['AvgRating'] != '_._':
                f.write(k['DetailUrl'] + '\n')
                print(k['AvgRating'])
            if k['SubItems'] and k['AvgRating'] != '_._':
                for d in k['SubItems']:
                    f.write(d['DetailUrl'] + '\n')
                    print(k['AvgRating'])


def get_full_information(store_link):
    link_store = 'https://www.foody.vn{}'.format(store_link)
    rb = session.get(link_store)
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
    information = {
        'name': data['Name'],
        'address': data['Address'],
        'city': data['City'],
        'district': data['District'],
        'priceMin': data['PriceMin'],
        'priceMax': data['PriceMax'],
        'Time': time_do,
        'review_point': review_point

    }
    return information


if __name__ == '__main__':
    print(get_full_information('/ha-noi/com-tam-hang'))
