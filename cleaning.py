# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:29:37 2021

@author: Justin Smith

This file contains helper functions that help reformat the data
"""
#specify working directory
import os
os.getcwd()
os.chdir(r'C:\Users\jds05\Desktop\qb_project')

#removes undesirable columns and values from dataframe
def cleanup (df, names):
    df =  df.drop(columns = ['Rate', 'QBR', 'Sk', 'Yds.1', 'NY/A', 
                                'ANY/A', 'Sk%', '4QC', 'Tm', 'Age',
                                'QBrec', 'Lng', 'Cmp%', 'TD%', 'Int%',
                                'Y/A', 'Y/C', 'Y/G', 'AY/A'],
                  errors = 'ignore')
    
    #if row contains a qb name
    df = df[(df.index.isin(names))] 
    
    #fill nulls wiht 0
    df = df.fillna(value = 0)
    
    return df

#selects all rows that are strictly QBs, does so by removing rows w/o qbrec
#since all qbs to have started a game have a record... regardless if position
#name was not listed
def get_qbs(df):
    df = df[((df['QBrec'].notnull()) & (df['QBrec'] != u''))] #has a qb record
    df = df.assign(Pos='QB')
    qb_names = df.index.tolist()
    #print(qb_names)
    return df, qb_names

#cleans the Player naming by removing symbols
def fix_names(df):
    
    #reset the index to modify Player name column
    df = df.reset_index()
    
    #irregular symbols to remove from name
    bad_chars = '*+'
    
    #strip the junk symbols off of the Player names
    df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: x.strip(bad_chars))
           
    #re establish the index
    df = df.set_index('Player')
    
    #return cleaned dataframe
    return df


#adds two dataframes together
def combine_df(df, df2):
    
    #add two dataframes together 
    df = df.add(df2, axis = 'index', fill_value = 0)
    
    return df


#renames rushing columns
def rename_rushing(df):
    df = df.rename(columns = {'Att': ' Rush_Att',
                             'Yds': 'Rush_Yds',
                             'TD':'Rush_TD',
                             '1D': 'Rush_1D'})
    return df


#renames passing columns
def rename_passing(df):
    df = df.rename(columns = {'Att': 'Pass_Att',
                             'Yds': 'Pass_Yds',
                             'TD':'Pass_TD',
                             '1D': 'Pass_1D'})
    return df
