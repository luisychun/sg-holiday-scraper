import pandas as pd
import time
import csv
import os
from selenium import webdriver
from selenium.webdriver import Chrome
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from csv import DictWriter
from datetime import datetime, timedelta

# def write_to_csv(ticket_price_dict):
#     departure_time_key = []
#     price_values = []
#     num_of_slots = 10
#     fields_name = ["Request On", "Departure - Destination", "Departure Date"]
#     file_name = "Tickets.csv"

#     for i in range(num_of_slots):
#         fields_name.append("Slot "+str(i+1))

#     try:
#         if os.path.isfile(file_name) is False:
#             init_set = {
#                 fields_name[0]: "",
#                 fields_name[1]: "",
#                 fields_name[2]: ""
#             }

#             for i in range(num_of_slots):
#                 init_set.update({ "Slot "+str(i+1) : [] })

#             map_to_csv = pd.DataFrame.from_dict(
#                 init_set)
#             map_to_csv.to_csv(file_name, index=False)

#             for keys, values in ticket_price_dict.items():
#                 departure_time_key.append(keys)
#                 price_values.append(values[0])
#             with open(file_name, 'a+', newline='') as write_obj:
#                 dict_writer = DictWriter(write_obj, fieldnames=fields_name)
#                 dict_writer.writerow(ticket_price_dict)
#                 print('CSV file created.')
#         else:
#             for keys, values in ticket_price_dict.items():
#                 departure_time_key.append(keys)
#                 price_values.append(values[0])
#             with open(file_name, 'a+', newline='') as write_obj:
#                 dict_writer = DictWriter(write_obj, fieldnames=fields_name)
#                 dict_writer.writerow(ticket_price_dict)
#                 print('CSV file updated.')
#     except Exception as e:
#         raise e

# program start here
def main():

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)

    URL = 'https://www.mom.gov.sg/employment-practices/public-holidays'

    driver.get(URL)

    # execute script to scroll down the page
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    # sleep for 30s
    time.sleep(10)


    # holidays list
    holidays_list = []

    # holidays row XPath
    # 2020 //*[@id="pagecontent_0_documentcontent_0_RptHolidayTabContent_RptHoliday_0_Row_0"]/td[1]/text()
    # 2021 //*[@id="pagecontent_0_documentcontent_0_RptHolidayTabContent_RptHoliday_1_Row_0"]/td[1]/text()
    # 2022 //*[@id="pagecontent_0_documentcontent_0_RptHolidayTabContent_RptHoliday_2_Row_0"]/td[1]/text()

    content_wrapper = driver.find_elements_by_xpath("//tr[contains(@id, '_RptHoliday_1_')]")
    for content in content_wrapper:
        actual_date = content.find_element_by_class_name('footable-first-column')
        if("\n" in actual_date.text):
          split_date = actual_date.text.split("\n")
          for split in split_date:
            holidays_list.append(split)
        else:
          holidays_list.append(actual_date.text)

    if not content_wrapper:
        print("Requested URL is invalid. Please check.")
    
    driver.quit()

    print(holidays_list)


main()
