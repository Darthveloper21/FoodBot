from main.Crawl_foody import *
import os

# craw_in_range("linkstore", "save", "chromedriver.exe", 100, 22, 30)

line = '/ha-noi/the-church'
save = 'test'

try:
    file = open(save + "/" + "testing" + ".json", "w", encoding="utf-8")
    value = get_full_information(line, "chromedriver.exe")
    try:
        json.dump(value, file, ensure_ascii=False, indent=4)
    except IOError:
        print("Some error occur at ")
except Exception as e:
    print(str(e))