# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 15:58:19 2021

@author: Justin Smith

This file scrapes Pro-Football Reference for passing stats from the years 
2011-2020. This data is then exported to 5 csv files
"""
# Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Import data manipulation modules
import pandas as pd

#import time module
import time

# years to collect stats from
years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

#iterate through years and save file for each years QB stats
for year in years:    
    # URL of page
    url = 'https://www.pro-football-reference.com/years/' + str(year) + \
        '/passing.htm'
    
    # Open URL and pass to BeautifulSoup
    html = urlopen(url)
    stats_page = BeautifulSoup(html, features='lxml')
    
    # Collect table headers
    column_headers = stats_page.findAll('tr')[0]
    column_headers = [i.getText() for i in column_headers.findAll('th')]

    #examine column headers
    #print(column_headers)

    # Collect table rows
    rows = stats_page.findAll('tr')[1:]
    
    # Get stats from each row
    qb_stats = []
    for i in range(len(rows)):
      qb_stats.append([col.getText() for col in rows[i].findAll('td')])
      
    #examine first row of data 
    #print(qb_stats[0])
    
    # Create DataFrame from our scraped data
    data = pd.DataFrame(qb_stats, columns=column_headers[1:])
    
    # Examine first/last five rows of data
    #print(data.head())
    #print(data.tail())
    
    export_file =  r'C:\Users\jds05\Desktop\qb_project\\' + str(year) + \
        '_passing_stats.csv'
    
    #export file to csv
    data.to_csv(export_file, index=False)
    time.sleep(2)
