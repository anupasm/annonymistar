import pandas as pd 
import networkx as nx
import numpy as np
data = pd.read_csv("edge_list.csv",usecols =['from','to']) 
from_list =list(data['from'])
to_list = list(data['to'])
from_uniq = list(pd.unique(from_list))
to_uniq = list(pd.unique(to_list))
for i in range(len(from_list)):
    row = "{0},{1}".format(from_uniq.index(from_list[i]),to_uniq.index(to_list[i]))
    print(row)
    # print(uniq.index(row'),uniq.index(x2))

# G =nx.from_pandas_edgelist(data,"from","to")
# A = nx.to_numpy_matrix(G)
# print(A)

