"""		  	   		   	 		  		  		    	 		 		   		 		  
Author: Macy Mora-Antoinette  	   		   	 		  		  		    	 		 		   		 		  
"""  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  
import pandas as pd
from scipy.stats import mode 		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
class RandomTrees(object):  		  	   		   	 		  		  		    	 		 		   		 		  
    """  				   		  	   		   	 		  		  		    	 		 		   		 		  		 	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
    """  		  	   		   	 		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size = 1):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		           		  	   		   	 		  		  		    	 		 		   		 		  
        """  		

        self.leaf_size = leaf_size	   		   	 		  		  		    	 		 		   		 		  
        pass    		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    def add_evidence(self, xdat, ydat):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Add training data to learner  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        xdat: A set of feature values used for training 		  	   		   	 		  		  		    	 		 		   		 		  
        ydat: the true values given xdat  		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
        """  		
        	   		   	 		  		  		    	 		 		   		 		    	
        #2 indicates a leaf since all other response values will be -1, 0, 1
        if xdat.shape[0] == 1: return np.array([100, ydat[0], np.nan, np.nan])
        if (ydat == ydat[0]).all(): return np.array([100, ydat[0], np.nan, np.nan])
        if (xdat.shape[0] <= self.leaf_size): return np.array([100, mode(ydat)[0][0], np.nan, np.nan])
        else:
            #determine random feature i
            i = np.random.choice(xdat.shape[1])
            j, k = np.random.choice(xdat.shape[0], 2)
            
            #Determine new branches from split
            SplitVal = (xdat[j,i] + xdat[k,i] )/2
            #SplitVal = np.median(xdat[:,i])
            leftBranch = xdat[xdat[:,i] <= SplitVal]
            rightBranch = xdat[xdat[:,i] > SplitVal]
            
            #Bypass exception if split does not work
            while leftBranch.size == 0 or rightBranch.size == 0:
                return np.array([100, mode(ydat)[0][0], np.nan, np.nan])
            #Use split if it works
            else:
                lefttree = self.add_evidence(leftBranch, ydat[xdat[:,i] <= SplitVal]) 
                righttree = self.add_evidence(rightBranch, ydat[xdat[:,i] > SplitVal])     
            
            if lefttree.shape[0] != lefttree.size:
                root = np.array([i, SplitVal, 1, lefttree.shape[0] + 1])
            else:
                root = np.array([i, SplitVal, 1, 2])
            self.table = np.vstack((root, lefttree, righttree))
            return 	self.table
  	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		           		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    def query(self, vals):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Approximate test values provided the model.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        vals: A numpy array with each row corresponding to a specific query		  	   		   	 		  		  		    	 		 		   		 		  
        return: The predicted result from the model  	   		   	 		  		  		    	 		 		   		 		  
        """ 	   		   	 		  		  		    	 		 		   		 		    	
        vals = np.array(vals)
        #create numpy array for prediction(s)
        pred = np.empty((vals.shape[0]))
        #loop over each entry in vals	  		   	 		  		  		    	 		 		   		 		  
        for point in range(vals.shape[0]):
            x = vals[point,:]
            #go down table until leaf (100) appears
            row = 0
            while self.table[row,0] != 100:
                #extract tree table contents
                #check if left branch
                if x[int(self.table[row,0])] <= self.table[row,1]:
                    row += int(self.table[row,2]) #row jumps based on left branch
                #check if Right branch
                else:
                    row += int(self.table[row,3]) #row jumps based on right branch
            #add prediction value
            pred[point] = self.table[row,1]
            
        return pred	   		   	 		  		  		    	 		 		   		 		            		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    print("passed random trees")  		  	   		   	 		  		  		    	 		 		   		 		  
