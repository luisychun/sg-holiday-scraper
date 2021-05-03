import datetime
from datetime import date, timedelta
import pandas as pd
import os

def write_to_csv(weekends_list):
  file_name = "Weekends_Dt_2021.csv"

  if os.path.isfile(file_name) is True:
    os.remove(file_name)
    print(f'existing {file_name} deleted.')

  try:
    df = pd.DataFrame(weekends_list, columns=["Date"])
    df.to_csv(file_name, index=False)
    print(f'{file_name} created.')
  except Exception as e:
    raise e

def getAllWeekendsDate(startYear, endYear):
  sat_list = pd.date_range(start=str(startYear), end=str(endYear), freq='W-SAT').strftime('%Y-%m-%d').tolist()
  sun_list = pd.date_range(start=str(startYear), end=str(endYear), freq='W-SUN').strftime('%Y-%m-%d').tolist()
  return sorted(sat_list+sun_list, key=lambda x:datetime.datetime.strptime(x, '%Y-%m-%d'))

def main():
  write_to_csv(getAllWeekendsDate('2021-01-01', '2021-12-31'))

main()