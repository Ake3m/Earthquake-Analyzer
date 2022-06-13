#Name: Akeem Peters
#Student ID: 410821332
#Data Science Final Project
from threading import local
from cv2 import sort
import pandas as pd
import numpy as np
from selenium import webdriver
import matplotlib.pyplot as plt
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import tkinter as tk
from tkinter import PhotoImage, ttk
from ctypes import windll
from datetime import datetime
from tkinter.font import BOLD, Font
from PIL import Image, ImageTk
windll.shcore.SetProcessDpiAwareness(1)
#GLOBAL VARIABLES
DRIVER_PATH = './/chromedriver.exe' #Please change this to the path of your chrome driver
URL="https://www.cwb.gov.tw/V8/E/E/index.html"
QUERY_URL="https://scweb.cwb.gov.tw/en-us/earthquake/data/"
page_source=""
#TEMPORARY COMMAND-LINE-INPUT. TKINTER WILL BE ADDED LATER
recent_table=""
parsed_df=""
local_copy=""
title_text=""
tag=""

def main():
    global recent_table
    global parsed_df
    global local_copy
    global title_text
    global tag
    title_text='Recent'
    df=fetchInformation() #function call to fetch the information from the website
    details=df['Details'].to_list() #gets the details column as a list to be split
    parsed_df=parseDetails(details) #function call to parse the details
    local_copy=parsed_df.copy()

    #GUI Section
    mainWindow = tk.Tk()
    mainWindow.title('Taiwan Earthquake Analysis system')
    window_width = 1280
    window_height = 950
    screen_width = mainWindow.winfo_screenwidth()
    screen_height = mainWindow.winfo_screenheight()

    center_x = int(screen_width/2 - window_width /2)
    center_y = int(screen_height/2 - window_height /2)
    
    title=ttk.Label(mainWindow,text='Taiwan Earthquake Analysis System',font=Font(mainWindow,size=25,weight=BOLD))
    title.pack(pady=25)
    img=ImageTk.PhotoImage(Image.open('./assets/taiwan.png').resize((100,150)))
    img_label=ttk.Label(mainWindow,image=img).pack()
    tag=ttk.Label(mainWindow, text='{} earthquakes in Taiwan (Updated on: {})'.format(title_text,datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
    tag.pack()
    table_columns = list(parsed_df.columns)
    recent_table=ttk.Treeview(mainWindow, columns=table_columns)
    recent_table.pack()

    for col in table_columns:
        recent_table.column(col, anchor="w")
        recent_table.heading(col, text=col, anchor='w')
    
    for index, row in parsed_df.iterrows():
        recent_table.insert("",0, text=index, values=list(row))

    view_recent_info = ttk.Button(mainWindow, text='Earthquake Analysis', command=lambda: viewInfo(parsed_df))
    view_recent_info.pack(pady=10,ipadx=50, ipady=25)
    note=ttk.Label(mainWindow, text='Please note: All Earthquake Analysis plots are automaticallt saved in the Analysis folder.')
    note.pack()
    sep=ttk.Separator(mainWindow,orient='horizontal')
    sep.pack(fill='x')
    search_text=ttk.Label(mainWindow,text='Search',font=Font(mainWindow, size=15, weight=BOLD))
    search_text.pack()
    explanation=ttk.Label(mainWindow, text='Example: Month: 3, Year: 2021 will give results for 3/2021')
    explanation.pack()
    month_label=ttk.Label(mainWindow,text='Enter month')
    month_label.pack()
    month=tk.StringVar()
    month_entry=ttk.Entry(mainWindow, textvariable=month)
    month_entry.pack()
    year_label=ttk.Label(mainWindow,text='Enter Year')
    year_label.pack()
    year=tk.StringVar()
    year_entry= ttk.Entry(mainWindow,textvariable=year)
    year_entry.pack()
    query_button = ttk.Button(mainWindow,text='Query',command=lambda:queryMonth(year.get(),month.get()))
    query_button.pack(pady=5,ipadx=25, ipady=5)
    reset_button = ttk.Button(mainWindow,text='Reset table', command=resetView)
    reset_button.pack(pady=20,ipadx=25, ipady=5)


    mainWindow.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    mainWindow.mainloop()


def resetView():
    global parsed_df
    global local_copy
    global recent_table
    global title_text
    global tag

    

    title_text='Recent'

    for i in recent_table.get_children():
        recent_table.delete(i)
    
    for index, row in local_copy.iterrows():
        recent_table.insert("",0, text=index, values=list(row))
    
    parsed_df=local_copy.copy()
    tag.config(text='{} earthquakes in Taiwan (Updated on: {})'.format(title_text,datetime.today().strftime('%Y-%m-%d %H:%M:%S')))

#function that is used to plot the information that it is given
def viewInfo(parsed_df):
    global title_text
    title=title_text
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
    plt.title("{} Earthquake count in Taiwan by County".format(title))
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
    plt.title("{} Earthquake count in Taiwan by magnitude".format(title))
    fig.tight_layout()
    save_title=title
    if '/' in save_title:
        save_title=save_title.replace('/','-')

    plt.savefig('./Analysis/earthquake_{}.jpg'.format(save_title), dpi=100)


    # plt.close()
    plt.show()

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
def getInput():
    qmwindow=tk.Tk()
    qmwindow.title("Query Window")
    window_width = 200
    window_height = 200
    screen_width = qmwindow.winfo_screenwidth()
    screen_height = qmwindow.winfo_screenheight()

    center_x = int(screen_width/2 - window_width /2)
    center_y = int(screen_height/2 - window_height /2)
    qmwindow.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    year=tk.StringVar()
    month = tk.StringVar()
    month_label=ttk.Label(qmwindow, text='Enter Month')
    month_label.pack()
    month_entry=ttk.Entry(qmwindow, textvariable=month)
    month_entry.pack()
    year_label=ttk.Label(qmwindow, text='Enter Year')
    year_label.pack()
    year_entry=ttk.Entry(qmwindow, textvariable=year)
    year_entry.pack()
    query_button = ttk.Button(qmwindow, text='Query',command=lambda:queryMonth(year.get(),month.get()))
    query_button.pack()

    qmwindow.mainloop()


def queryMonth(year, month):
    global recent_table
    global parsed_df
    global title_text
    global tag
    # year = input('Please enter a year: ')
    # month=input('Please enter the month: ')
    search_query = month+'-'+year
    title_text=search_query.replace('-','/')
    # print(search_query)
    data = getQueryInformation(search_query)
    parsed_data=parseQueryDetails(data)
    # print(parsed_data)
    for i in recent_table.get_children():
        recent_table.delete(i)
    for index, row in parsed_data.iterrows():
        recent_table.insert("",0, text=index, values=list(row))
    
    parsed_df=parsed_data.copy()
    tag.config(text='{} earthquakes in Taiwan (Updated on: {})'.format(title_text,datetime.today().strftime('%Y-%m-%d %H:%M:%S')))
    # viewInfo(parsed_data,search_query)

    #GUI for month query
    # query_window = tk.Tk()

    
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