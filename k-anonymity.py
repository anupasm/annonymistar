# import pandas as pd 
# import networkx as nx
# import numpy as np
# data = pd.read_csv("edge_list.csv",usecols =['from','to']) 
# G =nx.from_pandas_edgelist(data,"from","to")
# A = nx.to_numpy_matrix(G)
# print(A)

from numpy import genfromtxt
import numpy as np
mydata = genfromtxt('edge_list.csv', delimiter=',')
print(mydata[1:,1:])
print(type(mydata))