# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:16:20 2021

@author: Justin Smith

This file imports 10 csv files containing yearly football data. It then 
refines it into QB passing/rushing datframes from years 2011-2020 and includes
a summarized dataframe for the 10 combined years of data. These 11 dataframes 
are then exported back to CSV files in their final data format.
"""

# Import data manipulation modules
import pandas as pd
import os
from cleaning import cleanup, fix_names, combine_df, rename_passing, \
     rename_rushing, get_qbs

#specify working directory
os.getcwd()
os.chdir(r'C:\Users\jds05\Desktop\qb_project')

#this function cleans up the data and adds some calculated fields
def reformat_data(year, df = 'np.nan'):    
    
    #if year > 0, load in file and clean columns
    if year > 0:
        #define file names
        pass_file_name = str(year) + '_passing_stats.csv'
        rush_file_name = str(year) + '_rushing_stats.csv'
            
        #load in files
        pass_df = pd.read_csv(pass_file_name, index_col = 0)
        rush_df = pd.read_csv(rush_file_name, index_col = 0)
        
        #remove undesirable columns
        pass_df, qb_names = get_qbs(pass_df)
        pass_df = cleanup(pass_df, qb_names)
        rush_df = cleanup(rush_df, qb_names)
        
        #cleanup Player name column
        pass_df = fix_names(pass_df)    
        rush_df = fix_names(rush_df)
        
        #Rename columns to better identify attributes (i.e. Yds vs Pass_Yds)
        pass_df = rename_passing(pass_df)
        rush_df = rename_rushing(rush_df)
        
        #concatenate passing and rushing dataframes
        #skip first 3 of rushing df (Pos, G, GS)
        pass_stats = pd.concat([pass_df, rush_df.iloc[:,3:]], axis = 1)
    
    #if year == -1, load in passed in dataframe
    if year == -1:
        pass_stats = df
    
    #add some calculated columns
    pass_stats['AY/A'] = round(((pass_stats['Pass_Yds'] + (20 * \
                                 pass_stats['Pass_TD']) - (45 * \
                                 pass_stats['Int'])) / \
                                 (pass_stats['Pass_Att'])), 2 )   
        
        
    pass_stats['Total_TD'] = (pass_stats['Pass_TD'] + pass_stats['Rush_TD'])
    pass_stats['Total_Yds'] = (pass_stats['Pass_Yds'] + \
                               pass_stats['Rush_Yds'])
    pass_stats['Total_1D'] = (pass_stats['Pass_1D'] + pass_stats['Rush_1D'])
    pass_stats['Total_TOs'] = (pass_stats['Int'] + pass_stats['Fmb'])
    pass_stats['Int_Pct'] = round((pass_stats['Int'] \
                                   / pass_stats['Pass_Att'] * 100), 4)
    pass_stats['Pass_TD_Pct'] = round((pass_stats['Pass_TD'] \
                                       / pass_stats['Pass_Att'] * 100), 4)
    pass_stats['Pass_Yds_Att'] = round((pass_stats['Pass_Yds'] \
                                   / pass_stats['Pass_Att']), 2)
    pass_stats['Pass_Yds_Cmp'] = round((pass_stats['Pass_Yds'] \
                                    / pass_stats['Cmp']), 2) 
    pass_stats['TD_to_TO_Ratio'] = round(((pass_stats['Pass_TD'] + \
                                        pass_stats['Rush_TD']) / \
                                   (pass_stats['Int'] + \
                                      pass_stats['Fmb'])), 4)
    pass_stats['Tot_Yds_Gm'] = round(((pass_stats['Pass_Yds'] + \
                                       pass_stats['Rush_Yds']) / \
                                      pass_stats['G']), 4) 
    pass_stats['1D/G'] = round((pass_stats['Total_1D'] / pass_stats['G']), 2)    
    pass_stats['TD/G'] = round(((pass_stats['Pass_TD'] + \
                                 pass_stats['Rush_TD']) / pass_stats['G']), 2)
    
    pass_stats = pass_stats.fillna(value = 0)
    
    return pass_stats

#call function to reformat data   
pass_stats_2011 = reformat_data(2011)
pass_stats_2012 = reformat_data(2012)
pass_stats_2013 = reformat_data(2013)
pass_stats_2014 = reformat_data(2014)
pass_stats_2015 = reformat_data(2015) 
pass_stats_2016 = reformat_data(2016)
pass_stats_2017 = reformat_data(2017)
pass_stats_2018 = reformat_data(2018)
pass_stats_2019 = reformat_data(2019)
pass_stats_2020 = reformat_data(2020)

#call function to add dataframes together into one that combines 
# 5 years of passing data
#skip Pos column since its not numeric
df_passing = combine_df(pass_stats_2011.iloc[:, 1:], \
                        pass_stats_2012.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2013.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2014.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2015.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2016.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2017.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2018.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2019.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2020.iloc[:, 1:])

#add back the position column
df_passing.insert(0,'Pos', 'QB')

#reformat columns for final dataframe
df_passing = reformat_data(-1, df_passing)

#filter out Qbs that havent played a full season worth of games
df_passing = df_passing[df_passing.GS >= 15]

        
#export files to csv
#pass_stats_2011.to_csv('./2011_total_stats.csv')
#pass_stats_2012.to_csv('./2012_total_stats.csv')
#pass_stats_2013.to_csv('./2013_total_stats.csv')
#pass_stats_2014.to_csv('./2014_total_stats.csv')
#pass_stats_2015.to_csv('./2015_total_stats.csv')
#pass_stats_2016.to_csv('./2016_total_stats.csv')
#pass_stats_2017.to_csv('./2017_total_stats.csv')
#pass_stats_2018.to_csv('./2018_total_stats.csv')
pass_stats_2019.to_csv('./2019_total_stats.csv')
pass_stats_2020.to_csv('./2020_total_stats.csv')
df_passing.to_csv('./total_stats_10_years.csv')
