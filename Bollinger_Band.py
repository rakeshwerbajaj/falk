#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:27:58 2023

@author: fnurakeshwer
"""

import yfinance
import pandas as pd
import requests
import yfinance as yf
# =============================================================================
# import statistics as st
# =============================================================================
import pandas_ta as pta
from reading_database import read_database

import numpy as np
import time
import mysql.connector 
from mysql.connector import Error
#from dashboard import read_database2, connection_to_database


# simple moving average
def sma(data, window):
    sma = data.rolling(window = window).mean()
    return sma


# upper limit and lower limit 
def bb(data, sma, window):
    std = data.rolling(window = window).std()
    upper_bb = sma + std * 2
    lower_bb = sma - std * 2
    return upper_bb, lower_bb

def implement_bb_strategy(data, lower_bb, upper_bb):
    buy_price = []
    sell_price = []
    bb_signal = []
    signal = 0
    
    for i in range(len(data)):
        if data[i-1] > lower_bb[i-1] and data[i] < lower_bb[i]:
            if signal != 1:
                buy_price.append(data[i])
                sell_price.append(np.nan)
                signal = 1
                bb_signal.append('buy')
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append('hold')
        elif data[i-1] < upper_bb[i-1] and data[i] > upper_bb[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(data[i])
                signal = -1
                bb_signal.append('sell')
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                bb_signal.append('hold')
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            bb_signal.append('hold')
            
    return buy_price, sell_price, bb_signal


def my_bb(df_m1):
    bb_list = []
    for p in df_m1['symbols']:
        ticker = yf.Ticker(p)
        df_prices = ticker.history(interval='1d', period="max")
        df_prices['sma'] = sma(df_prices['Close'],14)
        df_prices['upper_bb'], df_prices['lower_bb'] = bb(df_prices['Close'], df_prices['sma'],14)
        df_prices = df_prices.dropna()
        buy_price, sell_price, bb_signal  = implement_bb_strategy(df_prices['Close'], df_prices['lower_bb'], df_prices['upper_bb'])
        df_prices['signal'] = bb_signal
        bb_list.append(df_prices['signal'][-1])
    df_m1['BB'] = bb_list    
    
    


    
    return df_m1
    
    
