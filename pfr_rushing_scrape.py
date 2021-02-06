# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31   1 18:15:20 2021

@author: Justin Smith
"""
# Import scraping modules
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Import data manipulation modules
import pandas as pd

#import time module
import time

# years to collect stats from
years = [2016, 2017, 2018, 2019, 2020]

#iterate through years and save file for each years rushing stats
for year in years:    
    # URL of page
    url = 'https://www.pro-football-reference.com/years/' + str(year) + \
        '/rushing.htm'
    
    # Open URL and pass to BeautifulSoup
    html = urlopen(url)
    stats_page = BeautifulSoup(html, features='lxml')
    
    # Collect table headers
    column_headers = stats_page.findAll('tr')[1]
    column_headers = [i.getText() for i in column_headers.findAll('th')]
    
    #examine column headers
    #print(column_headers)

    # Collect table rows
    rows = stats_page.findAll('tr')[2:]
    
    # Get stats from each row
    rushing_stats = []
    for i in range(len(rows)):
      rushing_stats.append([col.getText() for col in rows[i].findAll('td')])
      
    #examine first row of data  
    #print(rushing_stats[0])
    
    # Create DataFrame from our scraped data
    data = pd.DataFrame(rushing_stats, columns=column_headers[1:])
    
    # Examine first/last five rows of data
    #print(data.head())
    #print(data.tail())
    
    export_file =  r'C:\Users\jds05\Desktop\qb_project\\' + str(year) + \
        '_rushing_stats.csv'
    
    #export file to csv
    data.to_csv(export_file, index=False)
    time.sleep(2)
