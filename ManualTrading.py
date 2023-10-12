""" 		  	   		   	 		  		  		    	 		 		   		 		  
Author: Macy Mora-Antoinette 
Manually selecting stock market values from indicators		  	   		   	 		  		  		    	 		 		   		 		  
		  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt 		  	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd
from util import get_data		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
import numpy as np 	  	   		
from MarketIndicators import Bollinger, GoldenX, MACD  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
class ManualTrading(object):  		  	   		   	 		  		  		    	 		 		   		 		  
		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
    def __init__(self):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
         		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
	  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  
    def benchmark(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		   	 		  		  		    	 		 		   		 		  
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Control assumes initial investment of all shares and holding over a given time course  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol: The stock symbol 	  	   		   	 		  		  		    	 		 		   		 		  
        sd: start date - datetime 		  	   		   	 		  		  		    	 		 		   		 		  
        ed: end date - datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        sv: portfolio first value		  	   		   	 		  		  		    	 		 		   		 		  
        """  
        #create Benchmark
        prices = get_data([symbol], pd.date_range(sd, ed))
        prices.drop(columns = 'SPY', inplace = True) #drop SPY column
        bench = pd.DataFrame(np.zeros(prices.shape), index = prices.index, columns = [symbol])
        bench.iloc[0][symbol] += 1000 #buy 1000 shares on day 1 and hold
        return bench		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    # this method should use the existing manual policy and test it against new data  		  	   		   	 		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		   	 		  		  		    	 		 		   		 		  
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Tests your learner using data outside of the training data  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol: The stock symbol 	  	   		   	 		  		  		    	 		 		   		 		  
        sd: start date - datetime 		  	   		   	 		  		  		    	 		 		   		 		  
        ed: end date - datetime  		  	   		   	 		  		  		    	 		 		   		 		  
        sv: portfolio first value		  	   		   	 		  		  		    	 		 		   		 		  
        return: A Pandas DataFrame with values representing trades for each day. 
                possible values: +1000 = BUY
                                 -1000 = SELL
                                     0 = NO ACTION  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		   		  		    	 		 		   		 		    
    	#Get price history for the stock  	   		   	 		  		  		    	 		 		   		 		       		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		         
        prices = get_data([symbol], pd.date_range(sd, ed))
        prices.drop(columns = 'SPY', inplace = True) #drop SPY column
        
        #create indicators. Relabel their values to indicate 0 (hold), 1 (long), -1 (short)
        #Bollinger Bands
        bb = Bollinger(prices, 20)
        bb[(bb<1) & (bb>-1)] = 0
        bb[bb<=-1]= 1
        bb[bb>=1]= -1
        #Golden Crossing
        gold = GoldenX(prices, 25, 100)
        gold[gold<0] = -1
        gold[gold>=0] = 1
        #Moving Average Convergence Divergence (MACD)
        macd = MACD(prices, 12, 26)
        macd[macd >= 0] = -1
        macd[macd < 0] = 1
                    	
        #Create communal indicator 
        ind = pd.concat([bb, gold, macd], axis = 1).mode(axis = 1).mean(axis=1)
           
        #Create the trades dataframe df
        df = pd.DataFrame(np.zeros(prices.shape), index = prices.index, columns = [symbol])
        stocks_owned = 0
        for i in range(ind.size-1):       
            #if indicators say to long
            if ind[i] == 1: 
                if stocks_owned == 0: #and if you don't own any shares
                    stocks_owned += 1000
                    df.iloc[i][symbol] += 1000 #buy new shares
                elif stocks_owned == 1000: #and if you already own shares
                    pass #hold
                elif stocks_owned == -1000: #and if you short sold shares
                    stocks_owned += 2000
                    df.iloc[i][symbol] += 2000 #return shorted shares and buy new shares      
            #if indicators say to short
            elif ind[i] == -1:  
                if stocks_owned == 0: #and if you don't own any shares
                    stocks_owned -= 1000
                    df.iloc[i][symbol] -= 1000 #short sell shares
                elif stocks_owned == 1000: #and if you own shares
                    stocks_owned -= 2000
                    df.iloc[i][symbol] -= 2000 #sell old shares and short sell new shares
                elif stocks_owned == -1000: #and if you short sold shares
                    pass #hold   		   	 		  		  		    	 		 		   		 		  
        #return trades dataframe
        return df		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    print("passed")  		  	   		   	 		  		  		    	 		 		   		 		  
