# -*- coding: utf-8 -*-
"""
Author: Macy Mora-Antoinette  		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
from util import get_data  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		   		   	 		  		  		    	 		 		   		 		  

def compute_portvals(  		  	   		   	 		  		  		    	 		 		   		 		  
    df,  		  	   		   	 		  		  		    	 		 		   		 		  
    start_val=100000,  		  	   		   	 		  		  		    	 		 		   		 		  
    commission=0,  		  	   		   	 		  		  		    	 		 		   		 		  
    impact=0,  		  	   		   	 		  		  		    	 		 		   		 		  
):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
    start_val: The starting value of the portfolio  		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  
    commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		  
    impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  
   :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		      
    #Get price history for the stock
    prices = get_data(list(df.columns), pd.date_range(pd.to_datetime(df.index[0]), pd.to_datetime(df.index[-1])))
    prices['Cash'] = 1.0
    prices.drop(columns = 'SPY', inplace = True)
    
    #Create trades dataframe
    col = list(df.columns)
    col.append('Cash')
    trades = pd.DataFrame(np.zeros(prices.shape), index = prices.index, columns = col)
    stock = list(df.columns)[0]
    for index, row in df.iterrows():
        #check that order was on a trading day. If it was, the date index will exist in prices
        if index in prices.index: 
            #Get order details         
            shares = row[stock]
            price = prices.loc[index][stock]
            #Execute order
            trades['Cash'][index] -= price*shares + commission + (price*shares*impact)
            trades[stock][index] += shares
                
    #Create holdings dataframe
    holdings = trades.copy()
    holdings['Cash'].iloc[0] += start_val
    holdings = holdings.cumsum(axis = 0)
    
    #Create values dataframe
    values = holdings * prices.values  		  	   		   	 		  		  		    	 		 		   		 		  
    
    #Return portfolio normalized value
    portvals = values.sum(axis = 1)
    portvals_norm = portvals/portvals.iloc[0]
    return portvals_norm, values		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		   	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    compute_portvals()  