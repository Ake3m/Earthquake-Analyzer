#Name: Akeem Peters
#Student ID: 410821332
#Data Science Final Project
from cv2 import sort
import pandas as pd
import numpy as np
from parso import parse
import requests
from selenium import webdriver
import matplotlib.pyplot as plt
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

#GLOBAL VARIABLES
DRIVER_PATH = './/chromedriver.exe' #Please change this to the path of your chrome driver
URL="https://www.cwb.gov.tw/V8/E/E/index.html"
QUERY_URL="https://scweb.cwb.gov.tw/en-us/earthquake/data/"
page_source=""
#TEMPORARY COMMAND-LINE-INPUT. TKINTER WILL BE ADDED LATER

def main():
    options=['View recent Data','Query a specific month', 'Exit']
    df=fetchInformation() #function call to fetch the information from the website
    # print(df)
    details=df['Details'].to_list() #gets the details column as a list to be split
    parsed_df=parseDetails(details) #function call to parse the details
    # print(parsed_df)
    print("Welcome to the Taiwan Earthquake Analysis system.")
    while True:
        print("What would you like to do?")
        for i, option in enumerate(options):
            print(i+1,option)
        choice=int(input())-1
        if choice>len(options)-1:
            print("Out of bounds.")
        else:
            if choice==0:
                viewInfo(parsed_df,'Recent')
            elif choice==1:
                queryMonth()
            elif choice==2:
                break

#function that is used to plot the information that it is given
def viewInfo(parsed_df, title):
    print(parsed_df)
    labels=parsed_df['Date'].to_list()
    magnitudes=parsed_df['Magnitude'].to_list()
    depth=parsed_df['Depth'].to_list()
    x=np.arange(len(labels))
    by_county=parsed_df['Location'].value_counts()
    print(by_county)
    by_county=by_county.to_dict()
    names=list(by_county.keys())
    values=list(by_county.values())
    #magnitudes
    by_magnitude = parsed_df['Magnitude'].astype('int32').value_counts()
    by_magnitude = by_magnitude.to_dict()
    by_magnitude=dict(sorted(by_magnitude.items()))
    print(by_magnitude)
    magnitude_category = list(by_magnitude.keys())
    magnitude_count=list(by_magnitude.values())

    #plt section
    fig=plt.figure(num=1, figsize=(10,8))
    fig.suptitle('Taiwan {} Earthquake Summary'.format(title))
    plt.subplot(221)
    plt.bar(np.arange(len(names)),values, tick_label=names)
    plt.xlabel('County')
    plt.ylabel("Number of Earthquakes")
    plt.xticks(rotation=300)
    plt.title("{} earthquake Count in Taiwan by County".format(title))
    plt.subplot(222)
    plt.plot(x,magnitudes)
    plt.xlabel('Date')
    plt.ylabel("Magnitude")
    plt.xticks(x,labels,rotation=90)
    plt.title("Magnitudes of {} earthquakes in Taiwan".format(title))
    plt.subplot(223)
    plt.plot(x,depth)
    plt.xlabel('Date')
    plt.ylabel("Depth (KM)")
    plt.xticks(x,labels,rotation=90)
    plt.title("Depth of {} earthquakes in Taiwan".format(title))
    plt.subplot(224)
    plt.bar(np.arange(len(magnitude_category)),magnitude_count, tick_label=magnitude_category)
    plt.xlabel('Magnitudes')
    plt.ylabel("Number of Earthquakes")
    plt.title("{} earthquake Count in Taiwan by magnitude".format(title))
    fig.tight_layout()
    plt.savefig('410821332_test.jpg', dpi=100)
    plt.close()

def fetchInformation():
    headless_option=webdriver.ChromeOptions()
    headless_option.add_argument('headless')
    browser=webdriver.Chrome(executable_path=DRIVER_PATH, options=headless_option)
    browser.get(URL)
    pagedata=browser.page_source
    df=pd.read_html(pagedata)[0]
    # browser.quit()
    return df

def parseDetails(details):
    dates=[]
    times=[]
    magnitudes=[]
    locations=[]
    depth_list=[]
    for detail in details:
        parts=detail.split()
        dates.append(parts[0])
        times.append(parts[1])
        locations.append(parts[6]+' '+parts[7]+' '+parts[8])
        magnitudes.append(float(parts[10][2:]))
        depth_list.append(float(parts[9][5:len(parts[9])-2]))
    dates.reverse()
    times.reverse()
    locations.reverse()
    magnitudes.reverse()
    depth_list.reverse()

    reconstructed_details={
        "Location":locations,
        "Date":dates,
        "Time":times,
        "Depth":depth_list,
        "Magnitude":magnitudes
    }
    new_df=pd.DataFrame(reconstructed_details)
    return new_df

def separateLocation(location_list):
    returned_locations = []
    for location in location_list: 
        parts=location.split()
        returned_locations.append(parts[7]+' '+parts[8])
    
    return returned_locations

def separateDateAndTime(date_time_info):
    times=[]
    dates=[]
    for date_time in date_time_info:
        parts=date_time.split()
        dates.append(parts[0].replace('-','/'))
        times.append(parts[1])
    print(dates)
    print(times)

    return dates, times

def parseQueryDetails(details):
    magnitudes=details['ML'].to_list()
    depth_list = details['Depth'].to_list()
    location_information = details['Location']
    date_time_info= details['GMT+8(Taiwan)']
    locations=separateLocation(location_information)
    dates,times=separateDateAndTime(date_time_info)
    dates.reverse()
    times.reverse()
    locations.reverse()
    magnitudes.reverse()
    depth_list.reverse()
    reconstructed_details={
        "Location":locations,
        "Date":dates,
        "Time":times,
        "Depth":depth_list,
        "Magnitude":magnitudes
    }
    new_df=pd.DataFrame(reconstructed_details)
    return new_df

def getQueryInformation(search_query):
    
    headless_option=webdriver.ChromeOptions()
    headless_option.add_argument('headless')
    browser=webdriver.Chrome(executable_path=DRIVER_PATH, options=headless_option)
    browser.get(QUERY_URL)
    search_field = browser.find_element_by_id('Search')
    search_field.clear()
    time.sleep(1)
    search_field.send_keys(search_query)
    time.sleep(1)
    search_field.send_keys(Keys.RETURN)
    time.sleep(1)
    data=pd.read_html(browser.page_source)[1]

    return data

def queryMonth():
    year = input('Please enter a year: ')
    month=input('Please enter the month: ')
    search_query = month+'-'+year
    data = getQueryInformation(search_query)
    parsed_data=parseQueryDetails(data)
    print(parsed_data)
    viewInfo(parsed_data,search_query.replace('-','/'))
    
if __name__=='__main__':
    main()


# 0 - 06/03
# 1 - 05:09
# 2 - Location62.7
# 3 - km
# 4 - SSW
# 5 - of
# 6 - Hualien
# 7 - County
# 8 - Hall
# 9 - Depth27.9km
# 10 - ML4.5
# 11 - Check
# 12 - more