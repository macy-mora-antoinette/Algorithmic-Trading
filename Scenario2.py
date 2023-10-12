# -*- coding: utf-8 -*-
"""
Author: Macy Mora-Antoinette  		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
import numpy as np
from pandas.plotting import table
import pandas as pd   	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
from Simulation import compute_portvals
import matplotlib.pyplot as plt
import AlgorithmicTrading as sl


#if __name__ == "__main__": 
def Scenario2(sym): 
    
    # - PARAMETERS - #   
    comm = 9.95
    impact = np.array([0, 0.005, 0.1, 0.5])
    #impact = np.array([0.005, 0.5])
    colors = ['black', 'springgreen', 'turquoise', 'seagreen']
    cash = 100000
    #in-sample timeframe
    start = dt.datetime(2008, 1, 1)
    end = dt.datetime(2009,12,31)
    #out-of-sample timeframe
    start_test = dt.datetime(2010, 1, 1)
    end_test = dt.datetime(2011,12,31)
    
    # - RETURN PORTFOLIO STATISTICS - #
    df = pd.DataFrame(np.zeros((8,4)),index=['Forest in-sample', 'Forest in-sample', 'Forest in-sample', 'Forest in-sample',
                                             'Forest out-of-sample', 'Forest out-of-sample', 'Forest out-of-sample', 'Forest out-of-sample'],
                      columns=['Impact', 'Cumm Return', 'Sharpe Ratio', 'No. Trades']) 
    
    # - IN-SAMPLE - #  
    #Random Forest
    Traders = [] 
    i = 0
    plt.figure()
    for imp in impact:
        Traders.append(sl.AlgorithmicTrading(impact = imp, commission=comm)) # constructor 
        slTrader = Traders[i]
        slTrader.add_evidence(symbol=sym, sd=start, ed=end, sv = cash)
        slTrades = slTrader.testPolicy(symbol=sym, sd=start, ed=end, sv = cash)
        slVals, _= compute_portvals(slTrades,start_val=cash, commission=comm, impact=imp)
        #Portfolio Statistics
        df.iloc[i,0] = imp 
        df.iloc[i,1] = round(slVals.iloc[-1]/slVals.iloc[0]-1, 4)
        df.iloc[i,2] = round((slVals/slVals.shift(1)-1).mean(axis = 0) / (slVals/slVals.shift(1)-1).std(axis = 0), 4)
        df.iloc[i,3] = (slTrades.loc[slTrades[sym]!=0]).size
        plt.plot(slVals.index, slVals, color = colors[i], label = "impact "+str(impact[i]))
        i+=1
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Normalized Return") 
    plt.title("Scenario 2: Impact Effects on "+sym+" In-Sample Return")
    plt.xticks(rotation=60)
    plt.savefig('figure5.png', bbox_inches='tight')
    
    # - OUT-OF-SAMPLE - #  
    #Random Forest
    i = 0
    plt.figure()
    for imp in impact:
        slTrader = Traders[i]
        slTrades = slTrader.testPolicy(symbol=sym, sd=start_test, ed=end_test, sv = cash)
        slVals, _= compute_portvals(slTrades,start_val=cash, commission=comm, impact=imp)
        #Portfolio Statistics
        df.iloc[i+4,0] = imp
        df.iloc[i+4,1] = round(slVals.iloc[-1]/slVals.iloc[0]-1, 4)
        df.iloc[i+4,2] = round((slVals/slVals.shift(1)-1).mean(axis = 0) / (slVals/slVals.shift(1)-1).std(axis = 0), 4)
        df.iloc[i+4,3] = (slTrades.loc[slTrades[sym]!=0]).size
        plt.plot(slVals.index, slVals, color = colors[i], label = "impact "+str(impact[i]))
        i+=1
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Normalized Return") 
    plt.title("Scenario 2: Impact Effects on "+sym+" Out-of-Sample Return")
    plt.xticks(rotation=60)
    plt.savefig('figure6.png', bbox_inches='tight')
   
    # - PLOTTING - #    
    #statistics table   
    fig, ax = plt.subplots()#figsize=(8, 4)) # set size frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
    tabla = table(ax, df, loc='upper right')# where df is your data frame
    tabla.auto_set_font_size(False) # Activate set fontsize manually
    tabla.set_fontsize(12) # if ++fontsize is necessary ++colWidths
    plt.savefig('table2.png', bbox_inches='tight')
    plt.show()
 