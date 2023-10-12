# -*- coding: utf-8 -*-
"""
Updated: 11 Oct 2023
Author: Macy Mora-Antoinette  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
import numpy as np
import pandas as pd	
from pandas.plotting import table  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		    	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
from Simulation import compute_portvals   		  	   		   	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
import ManualTrading as ms
from Scenario1 import Scenario1
from Scenario2 import Scenario2


if __name__ == "__main__": 
    
    # - PARAMETERS - #  
    sym = "AAPL"   
    comm = 9.95
    imp = 0.005
    cash = 100000
    #in-sample timeframe
    start = dt.datetime(2008, 1, 1)
    end = dt.datetime(2009,12,31)
    #out-of-sample timeframe
    start_test = dt.datetime(2010, 1, 1)
    end_test = dt.datetime(2011,12,31)
 
    # - IN-SAMPLE - # 
    #Manual Strategy  
    msTrader = ms.ManualTrading() # constructor 
    msTrades = msTrader.testPolicy(symbol=sym, sd=start, ed=end , sv = cash)  
    benchmark = msTrader.benchmark(symbol=sym, sd=start, ed=end , sv = cash) #Create benchmark - buy 1000 shares on day 1 and hold            
    #compute portfolio values
    msVals, _= compute_portvals(msTrades,start_val=cash, commission=comm, impact=imp)
    bench, _ = compute_portvals(benchmark,start_val=cash, commission=comm, impact=imp)
    #allocate entry points for long and short
    msLong = msTrades.loc[msTrades[sym]>0]
    msShort = msTrades.loc[msTrades[sym]<0]
    
    # - OUT-OF-SAMPLE - #
    #Manual Strategy   
    msTrades2 = msTrader.testPolicy(symbol=sym, sd=start_test, ed=end_test , sv = cash)  
    benchmark2 = msTrader.benchmark(symbol=sym, sd=start_test, ed=end_test , sv = cash) #Create benchmark - buy 1000 shares on day 1 and hold               
    #compute portfolio values
    msVals2, _= compute_portvals(msTrades2,start_val=cash, commission=comm, impact=imp)
    bench2, _ = compute_portvals(benchmark2,start_val=cash, commission=comm, impact=imp)
    #allocate entry points for long and short
    msLong2 = msTrades2.loc[msTrades2[sym]>0]
    msShort2 = msTrades2.loc[msTrades2[sym]<0]
    
    # - RETURN PORTFOLIO STATISTICS - #
    df = pd.DataFrame(np.zeros((4,3)),index=['Manual in-sample', 'Manual out-of-sample', 'Benchmark in-sample', 'Benchmark out-of-sample'],
                      columns=['Cumm Return', 'Mean Daily Ret', 'Std Daily Ret']) 
    #in-sample Manual Trading 
    df.iloc[0,0] = round(msVals.iloc[-1]/msVals.iloc[0]-1, 4)
    df.iloc[0,1] = round((msVals/msVals.shift(1)-1).mean(axis = 0), 4)
    df.iloc[0,2] = round((msVals/msVals.shift(1)-1).std(axis = 0), 4)
    #out-of-sample Manual Trading 
    df.iloc[1,0] = round(msVals2.iloc[-1]/msVals2.iloc[0]-1, 4)
    df.iloc[1,1] = round((msVals2/msVals2.shift(1)-1).mean(axis = 0), 4)
    df.iloc[1,2] = round((msVals2/msVals2.shift(1)-1).std(axis = 0), 4)
    #in-sample benchmark control
    df.iloc[2,0] = round(bench.iloc[-1]/bench.iloc[0]-1, 4)
    df.iloc[2,1] = round((bench/bench.shift(1)-1).mean(axis = 0), 4)
    df.iloc[2,2] = round((bench/bench.shift(1)-1).std(axis = 0), 4)
    #out-of-sample benchmark control
    df.iloc[3,0] = round(bench2.iloc[-1]/bench2.iloc[0]-1, 4)
    df.iloc[3,1] = round((bench2/bench2.shift(1)-1).mean(axis = 0), 4)
    df.iloc[3,2] = round((bench2/bench2.shift(1)-1).std(axis = 0), 4)
   
    # - PLOTTING - #    
    #statistics table   
    fig, ax = plt.subplots()#figsize=(12, 2)) # set size frame
    ax.xaxis.set_visible(False)  # hide the x axis
    ax.yaxis.set_visible(False)  # hide the y axis
    ax.set_frame_on(False)  # no visible frame, uncomment if size is ok
    tabla = table(ax, df, loc='upper right')# where df is your data frame
    tabla.auto_set_font_size(False) # Activate set fontsize manually
    tabla.set_fontsize(12) 
    plt.savefig('table1.png', bbox_inches='tight')
    plt.show()

    # in-sample
    plt.plot(msVals.index, msVals, "blue", label = "Manual Trading")    
    plt.plot(bench.index, bench, "turquoise", label = "Benchmark")
    [plt.axvline(x = idx, color = "blue", linestyle = '--', label = "long entry") for idx in msLong.index]
    [plt.axvline(x = idx, color = "black", linestyle = '--', label = "short entry") for idx in msShort.index]
    plt.legend(framealpha = 1)
    plt.xlabel("Date")
    plt.ylabel("Normalized Return") 
    plt.title(sym+" Stock Return In-Sample")
    plt.xticks(rotation=60)  
    plt.savefig('figure1.png', bbox_inches='tight')
    
    # out-of-sample
    plt.figure()
    plt.plot(msVals2.index, msVals2, "blue", label = "Manual Trading")
    plt.plot(bench2.index, bench2, "turquoise", label = "Benchmark")
    [plt.axvline(x = idx, color = "blue", linestyle = '--', label = "long entry") for idx in msLong2.index]
    [plt.axvline(x = idx, color = "black", linestyle = '--', label = "short entry") for idx in msShort2.index]
    plt.legend(framealpha = 1)
    plt.xlabel("Date")
    plt.ylabel("Normalized Return")
    plt.title(sym+" Stock Return Out-of-Sample")
    plt.xticks(rotation=60)
    plt.savefig('figure2.png', bbox_inches='tight')
    
    
    # - EXPERIMENTS - #
    Scenario1(sym)
    Scenario2(sym)

