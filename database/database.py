import mysql.connector
import os
import json
from datetime import datetime

mydb = mysql.connector.connect(
    host="localhost",
    port=os.environ["DBPort"],
    user="root",
    password=os.environ["DBP"],
    database="FindFood"
)

cursor = mydb.cursor()

path_bun = "../save/link_store_bún_"
path_com = "../save/link_store_cơm_"
path_pho = "../save/link_store_phở_"


def add_diner(name, address, city, district, price_min, price_max, website,
              price_point, quality_point, destination_point, service_point, space_point):
    """
    Add diner information, id auto_increment
    :param name: str diner name
    :param address: str diner address
    :param city: str diner location
    :param district: str
    :param price_min: float minimum price range
    :param price_max: float maximum price range
    :param website: str foody site
    :param price_point: float %.2f price review
    :param quality_point: float %.2f food quality review
    :param destination_point: float %.2f destination review
    :param service_point: float %.2f service review
    :param space_point: float %.2f layout review
    :return: None
    """
    pass


def add_menu(name, price, diner_id, details=None):
    """

    :param name: str dish name
    :param price: float dish price
    :param diner_id:
    :param details:
    :return:
    """
    pass


def get_diner_id():
    """
    :return: the next diner id
    """
    pass


def prep_time(timetable: list, diner_id):
    """
    Time table preprocessing and add to database
    :param timetable: list of shifts of diners
    :param diner_id: int specify which diner
    :return: None
    """
    for shift in timetable:
        marks = shift.split('-')
        for mark in marks:
            print(datetime.strptime(mark, '%H:%M').time())


def prep_review(review_point: list):
    """
    preprocessing review_point
    :param review_point: list of points of each aspects
    :return: list of review_point in order: Chất lượng, Giá cả, Phục vụ, Vị trí, Không gian
    """
    for x in review_point:
        print(x)


def load_in_range(food_path, left, right):
    """
    get all the data from .json files to the database
    :param food_path: path of food type
    :param left: from epoch left
    :param right: to epoch right
    :return: None
    """
    for i in range(left, right + 1):
        path_tmp = food_path + str(i)
        file_list = os.listdir(path_tmp)
        for f in file_list:
            file = open(path_tmp + '/' + f, 'r', encoding='utf8')
            data = json.load(file)
            try:
                prep_time(data['Time'])
                # add_diner(data['name'],
                #           data['address'],
                #           data['city'],
                #           data['district'],
                #           data['priceMin'],
                #           data['priceMax'],
                #           data['review_point'])
                prep_review(data['review_point'])
            except IndexError:
                print('no menu')
            file.close()


load_in_range(path_bun, 31, 33)
