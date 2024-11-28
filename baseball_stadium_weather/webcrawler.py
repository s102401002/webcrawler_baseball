import time
# from DrissionPage import ChromiumPage, ChromiumOptions
import csv
import os
import io
from bs4 import BeautifulSoup
import requests
import pandas
# from PIL import Image
import base64
# import pytesseract
from itertools import chain
import codecs
import sys
from bs4 import BeautifulSoup
from datetime import datetime
import re

def parse_weather_forecast(soup):
    # This is a simplified parsing approach
    weather_data = {}
    
    date_elements = soup.find_all('th',headers="PC3_D")
    dates = {}
    for date_raw in date_elements:
        col = date_raw.get('colspan', 1) # the second parameter 1 means if no colspan attribute, it will return 1
        col = int(col)
        date = date_raw.get_text(strip=True)
        dates[date] = col
    print(dates)

    crawled_element = {"時間": 'PC3_Ti',"天氣狀況": 'PC3_Wx', "溫度": "PC3_T", "體感溫度": "PC3_AT", "降雨機率": "PC3_Po", "舒適度": "PC3_CI"}
    
    
    time_elements = soup.find_all('th', {'headers': lambda x: x and 'PC3_Ti' in x.split()})
    # print(time_elements)
    times = []
    for time in time_elements:
        time = time.get_text()
        times.append(time)
    
    # PC3_Wx

    
    time_index = 0
    for date, col in dates.items():
        weather_data[date] = []
        for i in range(col):
            weather_data[date].append({'time':times[time_index]})
            time_index += 1
    return weather_data

currentDateAndTime = datetime.now()
T = str(currentDateAndTime.year) + str(currentDateAndTime.month) + str(currentDateAndTime.day) + str(currentDateAndTime.hour) + "-" + str(currentDateAndTime.minute//10)
print(T)
url = "https://www.cwa.gov.tw/V8/C/L/Ballpark/MOD/3hr/K001_3hr_PC.html?T=" + T
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'}
# url = "https://www.cwa.gov.tw/Data/js/GT/TableData_GT_R_Ballpark.js?T=" + T
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")
data = parse_weather_forecast(soup)
# span = soup.find_all("span")
print(data)