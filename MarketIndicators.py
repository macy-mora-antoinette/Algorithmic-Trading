# -*- coding: utf-8 -*-
"""
Author: Macy Mora-Antoinette  		  	   		   	 		  		  		    	 		 		   		 		  
		  	   		   	 		  		  		    	 		 		   		 		  
"""  

import pandas as pd
from datetime import timedelta
import datetime as dt
import matplotlib.pyplot as plt
from util import get_data    		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    
def Bollinger(prices, n):
    # - Extracting data 2n days (safety factor 2x) beforehand to compute moving average - #
    symbol = prices.columns[0]
    idx = prices.index
    sd=prices.index[0] #save original start date
    ed=prices.index[-1] #save original end date
    prices = get_data([symbol],pd.date_range(sd - timedelta(days = 2*n), ed))
    prices.drop(columns = 'SPY', inplace = True) #drop SPY column
    # - Compute Bollinger Band - #
    SMA = prices.rolling(window=n,min_periods=n).mean()    
    std = prices.rolling(window=n,min_periods=n).std()
    # - Return the original dates only - #
    bb = (prices - SMA.values)/(2*std.values)
    return bb.loc[idx]

def GoldenX(prices, n, m):
    """
    n is for short SMA
    m is for long SMA
    m > n
    """
    # - Extracting data 2m days (safety factor 2x) beforehand to compute moving average - #
    symbol = prices.columns[0]
    idx = prices.index
    sd=prices.index[0] #save original start date
    ed=prices.index[-1] #save original end date
    prices = get_data([symbol],pd.date_range(sd - timedelta(days = 2*m), ed))
    prices.drop(columns = 'SPY', inplace = True) #drop SPY column
    # - Compute Golden Crossings - #
    short = prices.rolling(window=n,min_periods=n).mean()#/prices.iloc[0]  
    long = prices.rolling(window=m,min_periods=m).mean()#/prices.iloc[0]
    gold = 1-(short/long.values)
    # - Return the original dates only - #
    return gold.loc[idx]

def MACD(prices, n, m):
    """
    n is for short EMA
    m is for long EMA
    m > n
    """
    # - Extracting data 2m days (safety factor 2x) beforehand to compute moving average - #
    symbol = prices.columns[0]
    idx = prices.index
    sd=prices.index[0] #save original start date
    ed=prices.index[-1] #save original end date
    prices = get_data([symbol],pd.date_range(sd - timedelta(days = 2*m), ed))
    prices.drop(columns = 'SPY', inplace = True) #drop SPY column
    # - Compute MACD - #
    long = prices.ewm(span=n, min_periods=n, adjust=False).mean()
    short = prices.ewm(span=m, min_periods=m, adjust=False).mean()
    #signal = prices.ewm(span=9, min_periods=9, adjust=False).mean()
    macd = (short - long.values)#/signal.values
    # - Return the original dates only - #
    return macd.loc[idx]
   
if __name__ == "__main__":    
    #Import price history
    symbol='JPM'
    sd=dt.datetime(2008, 1, 1)
    ed=dt.datetime(2009,12,31)
    prices = get_data([symbol],pd.date_range(sd , ed))
    prices.drop(columns = 'SPY', inplace = True) #drop SPY column
    normed = prices/prices.iloc[0]-1
    
    #Plotting Bollinger Bands   
    bb = Bollinger(prices, 20)
    plt.figure()
    plt.plot(bb[symbol], label="bollinger band value")
    plt.plot(prices.index, normed, label = 'JPM')
    plt.axhline(y = 1, color = 'black')
    plt.axhline(y = -1, color = 'black')
    plt.title("Bolinger Bands")
    plt.legend(loc="lower right")
    plt.xticks(rotation=60)
    plt.xlabel("Dates")
    plt.ylabel("Normalized Price")
 
    #Plotting Golden Crossing
    gold = GoldenX(prices, 25, 100)
    plt.figure()
    plt.plot(gold[symbol], label="Golden crossing")
    plt.plot(prices.index, normed, label = 'JPM')
    plt.axhline(y = 0, color = 'black')
    plt.title("Golden Crossing")
    plt.legend(loc="lower right")
    plt.xticks(rotation=60)
    plt.xlabel("Dates")
    plt.ylabel("Normalized Price")
       
    #Plotting MACD
    macd = MACD(prices, 12, 26)
    plt.figure()
    plt.plot(macd[symbol], label="MACD")
    plt.plot(prices.index, normed, label = 'JPM')
    plt.axhline(y = 0, color = 'black')
    plt.title("MACD")
    plt.legend(loc="lower right")
    plt.xticks(rotation=60)
    plt.xlabel("Dates")
    plt.ylabel("Normalized Price")
    