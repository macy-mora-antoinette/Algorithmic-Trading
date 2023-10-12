"""  		  	   		   	 		  		  		    	 		 		   		 		  
Author: Macy Mora-Antoinette  		 		 		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		 
 		  	   		   	 		  		  		    	 		 		   		 		  
""" 	  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
import numpy as np  		  	   		   	 		  		  		    	 		 		   		 		  
from scipy.stats import mode	  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
class BaggingTrees(object):  		  	   		   	 		  		  		    	 		 		   		 		  
 		  	   		   	 		  		  		    	 		 		   		 		  
    def __init__(self, learner, bags, kwargs = {}, boost = False):  		  	   		   	 		     
        	
        self.learners = []  
        for i in range(0,bags):  
            self.learners.append(learner(**kwargs)) 	   		   	 		  		  		    	 		 		   		 		  
        pass		  	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		  	  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
    def add_evidence(self, xdat, ydat):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Add training data to each learner  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        xdat: A set of feature values used to train the learner    	   		   	 		  		  		    	 		 		   		 		   		  	   		   	 		  		  		    	 		 		   		 		  
        ydat: The value we are attempting to predict given the X data   	   		   	 		  		  		    	 		 		   		 		  
        """

        xdat = np.array(xdat)
        ydat = np.array(ydat)
        
        #call each learner and add evidence
        for tree in self.learners:
            idx = np.random.randint(ydat.size, size = ydat.size)
            self.tree = tree.add_evidence(xdat[idx,:], ydat[idx]) # training step
        return self.tree
    
       		  		    	 		 		   		 		           		  	   		   	 		  		  		    	 		 		   		 		    		  	   		   	 		  		  		    	 		 		   		 		  
    def query(self, vals):  		  	   		   	 		  		  		    	 		 		   		 		  
        """  		  	   		   	 		  		  		    	 		 		   		 		  
        Approximate a few test vals provided the given model.  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
        vals: A numpy array with each row corresponding to a specific query 	 		  		  		    	 		 		   		 		  
        return: The predicted result of the input data according to the trained model  		  	   		   	 		  		  		    	 		 		   		 		  
        """
        vals = np.array(vals)
        #query each learner
        self.pred = np.empty((vals.shape[0],len(self.learners)))
        i = 0
        for tree in self.learners:
            self.pred[:,i] = tree.query(vals)# query
            i+= 1
        #return mode of learners
        return mode(self.pred, axis = 1)[0]         		   	 		  		  		    	 		 		   		 		            		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
  		  	   		   	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		  	   		   	 		  		  		    	 		 		   		 		  
    print("passed bagging trees")  		  	   		   	 		  		  		    	 		 		   		 		  
