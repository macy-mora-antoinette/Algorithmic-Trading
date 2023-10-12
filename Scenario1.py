# -*- coding: utf-8 -*-
"""
Author: Macy Mora-Antoinette  		  	   		   	 		  		  		    	 		 		   		 		  
		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		   	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
from Simulation import compute_portvals
import matplotlib.pyplot as plt
import ManualTrading as ms
import AlgorithmicTrading as sl

 
#if __name__ == "__main__":
def Scenario1(sym): 
    
    # - PARAMETERS - #    
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
    #Random Forest 
    slTrader = sl.AlgorithmicTrading(impact = imp, commission=comm) # constructor 
    slTrader.add_evidence(symbol=sym, sd=start, ed=end, sv = cash) # training phase 
    slTrades = slTrader.testPolicy(symbol=sym, sd=start, ed=end, sv = cash) # testing phase
    #compute portfolio values
    slVals, _= compute_portvals(slTrades,start_val=cash, commission=comm, impact=imp)
    msVals, _= compute_portvals(msTrades,start_val=cash, commission=comm, impact=imp)
    bench, _ = compute_portvals(benchmark,start_val=cash, commission=comm, impact=imp)
    
    # - OUT-OF-SAMPLE - #
    #Manual Strategy   
    msTrades2 = msTrader.testPolicy(symbol=sym, sd=start_test, ed=end_test , sv = cash)  
    benchmark2 = msTrader.benchmark(symbol=sym, sd=start_test, ed=end_test , sv = cash) #Create benchmark - buy 1000 shares on day 1 and hold               
    #Random Forest 
    slTrades2 = slTrader.testPolicy(symbol=sym, sd=start_test, ed=end_test , sv = cash) # testing phase
    #compute portfolio values
    slVals2, _= compute_portvals(slTrades2,start_val=cash, commission=comm, impact=imp)
    msVals2, _= compute_portvals(msTrades2,start_val=cash, commission=comm, impact=imp)
    bench2, _ = compute_portvals(benchmark2,start_val=cash, commission=comm, impact=imp)
    
    # - PLOTTING - #
    # in-sample
    plt.figure()
    plt.plot(slVals.index, slVals, "blueviolet", label = "Random Forest")
    plt.plot(msVals.index, msVals, "mediumvioletred", label = "Manual Strategy")    
    plt.plot(bench.index, bench, "coral", label = "Benchmark")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Normalized Return") 
    plt.title("Scenario 1: "+sym+" Stock Return In-Sample")
    plt.xticks(rotation=60)  
    plt.savefig('figure3.png', bbox_inches='tight')
    
    # out-of-sample
    plt.figure()
    plt.plot(slVals2.index, slVals2, "blueviolet", label = "Random Forest")
    plt.plot(msVals2.index, msVals2, "mediumvioletred", label = "Manual Strategy")
    plt.plot(bench2.index, bench2, "coral", label = "Benchmark")
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Normalized Return")
    plt.title("Scenario 1: "+sym+" Stock Return Out-of-Sample")
    plt.xticks(rotation=60)
    plt.savefig('figure4.png', bbox_inches='tight')
   