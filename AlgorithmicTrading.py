""" 		  	   		   	 		  		  		    	 		 		   		 		  
Author: Macy Mora-Antoinette	

Implements investment with strategy  that can learn a trading policy using the same indicators used in ManualTrading. 	  	   		   	 		  		  		    	 		 		   		 		  
"""  		
  	   		   	 		  		  		    	 		 		   		 		  
from datetime import timedelta
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  
import datetime as dt  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
import RandomTrees as rt
import BaggingTrees as bt  		  	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd  		  	   		   	 		  		  		    	 		 		   		 		  
from util import get_data
from MarketIndicators import Bollinger, GoldenX, MACD    		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
class AlgorithmicTrading(object):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		     		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
    impact: The market impact of each transaction, defaults to 0.0  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
    commission: The commission amount charged, defaults to 0.0   		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    # constructor  		  	   		   	 		  		  		    	 		 		   		 		  
    def __init__(self, impact=0.0, commission=0.0):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        	  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
		  	   		   	 		  		  		    	 		 		   		 		  
        self.impact = impact  		  	   		   	 		  		  		    	 		 		   		 		  
        self.commission = commission  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    # this method should create a QLearner, and train it for trading  		  	   		   	 		  		  		    	 		 		   		 		  
    def add_evidence(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2008, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2009, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		   	 		  		  		    	 		 		   		 		  
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Trains your algorithmic trader over a given time frame.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol: The stock symbol 		  	   		   	 		  		  		    	 		 		   		 		  
        sd: start date - datetime  	   		   	 		  		  		    	 		 		   		 		  
        ed: end date - datetime 		  	   		   	 		  		  		    	 		 		   		 		  
        sv: initial value of portfolio  		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
	  		    	 		 		   		 		  
        #Get price history for the stock
        #Extracting data 2n days (safety factor 2x) beforehand to compute return over n days
        n=15 #no. days to go back
        pricesn = get_data([symbol],pd.date_range(sd - timedelta(days = 2*n), ed))
        pricesn.drop(columns = 'SPY', inplace = True)
        #prices over actual period of interest
        prices = get_data([symbol],pd.date_range(sd, ed))
        prices.drop(columns = 'SPY', inplace = True)
        prices = prices - self.commission
               
        #create classifications (hold/cash:0, long:1, short:-1) as the y response
        ret = pricesn.shift(n)/pricesn - 1 #classified by return over n days
        YBUY = 0.05 + self.impact
        YSELL = -0.05 + self.impact
        ret[ret>=YBUY] = 1 #long
        ret[ret<=YSELL] = -1 #short
        ret[(ret<YBUY) & (ret>YSELL)] = 0 #cash/hold
        ydata = ret.loc[prices.index]
        
        #create indicators as features in the x dataframe
        prices = pricesn.loc[prices.index]    
        bb = Bollinger(prices, 20) #Bollinger Bands
        gold = GoldenX(prices, 25, 100) #Golden Crossing
        macd = MACD(prices, 12, 26) #Moving Avg Convergence-Divergence
        xdata = pd.concat([bb, gold, macd], axis = 1)  	 		  		  		    	 		 		   		 		  
        
        #Create a Random Forest by nesting the RTLeaner within BaggingTrees
        # no. bags = no. trees desired in forest 	   		   	 		  		  		    	 		 		   		 		  
        self.learner = bt.BaggingTrees(learner = rt.RandomTrees, kwargs = {"leaf_size":5}, bags = 30, boost = False)   		  	   		   	 		  		  		    	 		 		   		 		  
        self.learner.add_evidence(xdata, ydata)  # train it 	  	   		   	 		  		  		    	 		 		   		 		  	   		   	 		  		  		    	 		 		   		 		  
         		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  
    # this method should use the existing policy and test it against new data  		  	   		   	 		  		  		    	 		 		   		 		  
    def testPolicy(  		  	   		   	 		  		  		    	 		 		   		 		  
        self,  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol="IBM",  		  	   		   	 		  		  		    	 		 		   		 		  
        sd=dt.datetime(2009, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        ed=dt.datetime(2010, 1, 1),  		  	   		   	 		  		  		    	 		 		   		 		  
        sv=10000,  		  	   		   	 		  		  		    	 		 		   		 		  
    ):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Testing Algorithmic trading model using data outside of the training data  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        symbol: The stock symbol 		  	   		   	 		  		  		    	 		 		   		 		  
        sd: start date - datetime  	   		   	 		  		  		    	 		 		   		 		  
        ed: end date - datetime 		  	   		   	 		  		  		    	 		 		   		 		  
        sv: initial value of portfolio  		  	   		   	 		  		  		    	 		 		   		 		  
        return: A Pandas DataFrame with values representing trades for each day
        possible values:  +1000 = BUY   		  	   		   	 		  		  		    	 		 		   		 		  
                          -1000 = SELL 
                              0 = NO ACTION
        """	 
		  		  		    	 		 		   		 		  
        #Get price history for the stock
        prices = get_data([symbol],pd.date_range(sd, ed))
        prices.drop(columns = 'SPY', inplace = True)
        
        #create indicators as features in the x dataframe   
        bb = Bollinger(prices, 20) #Bollinger Bands
        gold = GoldenX(prices, 25, 100) #Golden Crossing
        macd = MACD(prices, 12, 26) #Moving Avg Convergence-Divergence
        xdata = pd.concat([bb, gold, macd], axis = 1)
        xdata.columns.values[0] = "bb"
        xdata.columns.values[1] = "gold"
        xdata.columns.values[2] = "macd"  	 		  		  	   		   	 		  		  		    	 		 		   		 		  
        
        #get trading predictions
        trades = self.learner.query(xdata)  		   	 		  		  		    	 		 		   		 		  
        
        #Create the trades dataframe df
        df = pd.DataFrame(np.zeros(prices.shape), index = prices.index, columns = [symbol])
        stocks_owned = 0

        for i in range(trades.size-1):       

            #if indicators say to long
            if trades[i] == 1: 
                if stocks_owned == 0: #and if you don't own any shares
                    stocks_owned += 1000                   
                    df.iloc[i][symbol] += 1000 #buy new shares                    
                elif stocks_owned == 1000: #and if you already own shares
                    continue #hold
                elif stocks_owned == -1000: #and if you short sold shares
                    stocks_owned += 2000
                    df.iloc[i][symbol] += 2000 #return shorted shares and buy new shares
                              
            #if indicators say to short
            elif trades[i] == -1:  
                if stocks_owned == 0: #and if you don't own any shares
                    stocks_owned -= 1000
                    df.iloc[i][symbol] -= 1000 #short sell shares
                   
                elif stocks_owned == 1000: #and if you own shares
                    stocks_owned -= 2000
                    df.iloc[i][symbol] -= 2000 #sell old shares and short sell new shares
                elif stocks_owned == -1000: #and if you short sold shares
                    continue #hold   		   	 		  		  		    	 		 		   		 		  


  		  	  		   	 		  		  		    	 		 		   		 		  
        return df	  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    print("passed algorithmic trading")  		  	   		   	 		  		  		    	 		 		   		 		  
