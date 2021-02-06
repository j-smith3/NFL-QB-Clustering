# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 16:16:20 2021

@author: Justin Smith

This file imports 5 csv files containing yearly football data. It then 
refines it into QB passing/rushing datframes from years 2016-2020 and includes
a summarized dataframe for the 5 combined years of data. These 6 dataframes 
are then exported back to CSV files in their final data format.
"""

# Import data manipulation modules
import pandas as pd
import os
from cleaning import cleanup, fix_names, combine_df, rename_passing, \
     rename_rushing

#specify working directory
os.getcwd()
os.chdir(r'C:\Users\jds05\Desktop\qb_project')

def reformat_data(year):    
    
    #define file names
    pass_file_name = str(year) + '_passing_stats.csv'
    rush_file_name = str(year) + '_rushing_stats.csv'
    
    #load in files
    pass_df = pd.read_csv(pass_file_name, index_col = 0)
    rush_df = pd.read_csv(rush_file_name, index_col = 0)
    
    #remove undesirable columns
    pass_df = cleanup(pass_df)
    rush_df = cleanup(rush_df)
    
    #cleanup Player name column
    pass_df = fix_names(pass_df)
    rush_df = fix_names(rush_df)
    
    #Rename columns to better identify attributes (i.e. Yds vs Pass_Yds)
    pass_df = rename_passing(pass_df)
    rush_df = rename_rushing(rush_df)
    
    #concatenate passing and rushing dataframes
    #skip first 3 of rushing df (Pos, G, GS)
    pass_stats = pd.concat([pass_df, rush_df.iloc[:,3:]], axis = 1)
    
    #add some calculated columns
    pass_stats['Total_TD'] = (pass_stats['Pass_TD'] + pass_stats['Rush_TD'])
    pass_stats['Total_Yds'] = (pass_stats['Pass_Yds'] + \
                               pass_stats['Rush_Yds'])
    pass_stats['Total_1D'] = (pass_stats['Pass_1D'] + pass_stats['Rush_1D'])
    pass_stats['Total_TOs'] = (pass_stats['Int'] + pass_stats['Fmb'])
    pass_stats['Int_Pct'] = round((pass_stats['Int'] \
                                   / pass_stats['Pass_Att']), 4)
    pass_stats['Pass_TD_Pct'] = round((pass_stats['Pass_TD'] \
                                       / pass_stats['Pass_Att']), 4)
    pass_stats['Pass_Yds_Att'] = round((pass_stats['Pass_Yds'] \
                                   / pass_stats['Pass_Att']), 2)
    pass_stats['Pass_Yds_Cmp'] = round((pass_stats['Pass_Yds'] \
                                    / pass_stats['Cmp']), 2) 
    
    return pass_stats

#call function to reformat data    
pass_stats_2016 = reformat_data(2016)
pass_stats_2017 = reformat_data(2017)
pass_stats_2018 = reformat_data(2018)
pass_stats_2019 = reformat_data(2019)
pass_stats_2020 = reformat_data(2020)

#call function to add dataframes together into one that combines 
# 5 years of passing data
#skip Pos column since its not numeric
df_passing = combine_df(pass_stats_2016.iloc[:, 1:], \
                        pass_stats_2017.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2018.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2019.iloc[:, 1:])
df_passing = combine_df(df_passing, pass_stats_2020.iloc[:, 1:])

#add back the position column
df_passing.insert(0,'Pos', 'QB')

# recalculate final summarized df to accurately represent values.
# The combine_df function added all corresponding values, which you
# would not want to do that for the certain columns like yards per attempt
df_passing['Yds_Att'] = round((df_passing['Pass_Yds'] \
                               / df_passing['Pass_Att']), 2)
df_passing['Yds_Cmp'] = round((df_passing['Pass_Yds'] \
                                / df_passing['Cmp']), 2 )
df_passing['Int_Pct'] = round((df_passing['Int'] \
                               / df_passing['Pass_Att']), 4)
df_passing['Pass_TD_Pct'] = round((df_passing['Pass_TD'] \
                                   / df_passing['Pass_Att']), 4)
df_passing['Pass_Yds_Att'] = round((df_passing['Pass_Yds'] \
                                   / df_passing['Pass_Att']), 2)
df_passing['Pass_Yds_Cmp'] = round((df_passing['Pass_Yds'] \
                                    / df_passing['Cmp']), 2) 
    
#filter out Qbs that havent played a full season worth of games
df_passing = df_passing[df_passing.GS >= 16]

        
#export files to csv
pass_stats_2016.to_csv(r'C:\Users\jds05\Desktop\qb_project\2016_total_stats.csv')
pass_stats_2017.to_csv(r'C:\Users\jds05\Desktop\qb_project\2017_total_stats.csv')
pass_stats_2018.to_csv(r'C:\Users\jds05\Desktop\qb_project\2018_total_stats.csv')
pass_stats_2019.to_csv(r'C:\Users\jds05\Desktop\qb_project\2019_total_stats.csv')
pass_stats_2020.to_csv(r'C:\Users\jds05\Desktop\qb_project\2020_total_stats.csv')
df_passing.to_csv(r'C:\Users\jds05\Desktop\qb_project\total_stats_5_years.csv')