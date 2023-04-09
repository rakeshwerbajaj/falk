#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:14:54 2023

@author: fnurakeshwer
"""

import mysql.connector 
from mysql.connector import Error
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()



def connection_to_database():
    
    server = "analysis-tool-nonprod.c4rbkrjinf7p.eu-central-1.rds.amazonaws.com" # replace with your server name
    database = "stocks-dev" # replace with your database name
    username = "admin" # replace with your username
    password = "nCk8Ll42KcLU5KdX631L" # replace with your password
    connection = mysql.connector.connect(host = server, user = username,password = password,database = database)
    
    cursor = connection.cursor()
    return connection




def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")
        

def read_database():
    q1 = """
    SELECT *
    FROM stocklist2; """
    conn = connection_to_database()
    results = read_query(conn, q1)
    print(len(results))
    
    #for result in results:
    #   print(result)
    df_from_database = pd.DataFrame()
    df_database2 = pd.DataFrame.from_records(results, columns=['stock_id','stockname', 'dividend', 'high_growth', 'leverman', 'Indexes' ,'stock_date','P_E_from_aktien_gude'])
    print(len(df_database2))
    return df_database2
        
     # master file   
     
# =============================================================================
#     df_1 = df_from_database[df_from_database['Indexes']=="DAX"]
#     df_2= df_from_database[df_from_database['Indexes']=="MDAX"]
#     df_3= df_from_database[df_from_database['Indexes']=="SDAX"]
#     df_4= df_from_database[df_from_database['Indexes']=="TecDAX"]
#     df_5= df_from_database[df_from_database['Indexes']=="CDAX"]
#     df_6= df_from_database[df_from_database['Indexes']=="Scale"]
#     df_7 =df_from_database[df_from_database['Indexes']=="Dow-Jones"]
#     df_14 =df_from_database[df_from_database['Indexes']=="EURO-STOXX-50"]
#     df_15 = df_from_database[df_from_database['Indexes']=="STOXX-Europe-600"]
#     
#     # welt calculation
#     dd1 = df_7.append(df_14, ignore_index=True)
#     df_welt = dd1.append(df_15, ignore_index=True)
#     
#     #calculation of deu
#     df_d1  = df_1.append(df_2, ignore_index=True)
#     df_d2 = df_d1.append(df_3, ignore_index=True)
#     df_d3 = df_d2.append(df_4, ignore_index=True)
#     df_deu = df_d3.append(df_5, ignore_index=True) 
#     
#     #df_master 
#     df_master = df_deu.append(df_welt, ignore_index=True)
#     
#     #start from here addition and 
#     df_master['points'] = df_master['dividend'] + df_master['high_growth'] + df_master['leverman']
#     
#     
# 
#    
#     df_master=df_master.drop_duplicates(subset = "stockname")
#     
#     #start from here addition and 
#     df_master['points'] = df_master['dividend'] + df_master['high_growth'] + df_master['leverman']
#      
#     df_m1 =  df_master.sort_values(by=['points'])
#     #df_m1 = df_m1[df_m1['points']>20]
#    # df_m1 = df_m1.iloc[:,[0,7,1,2,3,6,4,5]]
#     
# =============================================================================
    

#df_from_database = read_database() 









