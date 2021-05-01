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

def write_to_csv(formatted_list):
  fields_name = ["Date"]
  file_name = "SG_2021.csv"

  if os.path.isfile(file_name) is True:
    os.remove(file_name)
    print(f'existing {file_name} deleted.')

  try:
    df = pd.DataFrame(formatted_list, columns=["Date"])
    df.to_csv(file_name, index=False)
    print(f'{file_name} created.')
  except Exception as e:
    raise e

def format_date(holidays_list):
  new_list = []
  for idx in range(len(holidays_list)):
    new_list.append(datetime.strptime(holidays_list[idx], "%d %B %Y").strftime('%Y-%m-%d'))
  return new_list

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

  # close the overlay layer
  skip_btn = driver.find_element_by_xpath('/html/body/div[1]/div[3]/a[1]')
  skip_btn.click()

  # switch to 2022
  # trigger_btn = driver.find_element_by_xpath('//*[@id="pagecontent_0_documentcontent_0_RptHolidayTab_HlYear_2"]')
  # trigger_btn.click()

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
  else:
    # format date
    formatted_list = format_date(holidays_list)
    write_to_csv(formatted_list)
  
  driver.quit()

  # print(formatted_list)


main()
