#Name: Akeem Peters
#Student ID: 410821332
#Data Science Final Project
import pandas as pd
import numpy as np
from parso import parse
import requests
from selenium import webdriver
import matplotlib.pyplot as plt
import time
from bs4 import BeautifulSoup

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
                viewRecent(parsed_df)
            elif choice==1:
                queryMonth()
            elif choice==2:
                break





def viewRecent(parsed_df):
    print(parsed_df)
    labels=parsed_df['Date'].to_list()
    magnitudes=parsed_df['Magnitude'].to_list()
    depth=parsed_df['Depth'].to_list()
    x=np.arange(len(labels))
    by_county=parsed_df['Location'].value_counts()
    by_county=by_county.to_dict()
    names=list(by_county.keys())
    values=list(by_county.values())

    #plt section
    fig=plt.figure(num=1, figsize=(10,8))
    fig.suptitle('Taiwan Recent Earthquake Summary')
    plt.subplot(221)
    plt.bar(np.arange(len(names)),values, tick_label=names)
    plt.xlabel('County')
    plt.ylabel("Number of Earthquakes")
    plt.xticks(rotation=300)
    plt.title("Earthquakes Count in Taiwan by County")
    plt.subplot(222)
    plt.plot(x,magnitudes)
    plt.xlabel('Date')
    plt.ylabel("Magnitude")
    plt.xticks(x,labels,rotation=90)
    plt.title("Magnitudes of recent earthquakes in Taiwan")
    plt.subplot(223)
    plt.plot(x,depth)
    plt.xlabel('Date')
    plt.ylabel("Depth (KM)")
    plt.xticks(x,labels,rotation=90)
    plt.title("Depth of recent earthquakes in Taiwan")
    fig.tight_layout()
    plt.savefig('410821332_test.jpg', dpi=100)

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

def queryMonth():
    year = input('Please enter a year: ')
    month=input('Please enter the month: ')
    headless_option=webdriver.ChromeOptions()
    headless_option.add_argument('headless')
    browser=webdriver.Chrome(executable_path=DRIVER_PATH, options=headless_option)
    browser.get(QUERY_URL)

    test=pd.read_html(browser.page_source)[1]
    print(test)
    
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