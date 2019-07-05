import pandas as pd
import networkx as nx
from collections import Counter
import math
import json
import Levenshtein as lev
import matplotlib.pyplot as plt
from itertools import combinations 
from sklearn.preprocessing import LabelEncoder
from sklearn_pandas import DataFrameMapper
import cost_cal
import random
import numpy as np
from collections import Counter

"""
Read the csv file(source,target,timestamp) and relabel vertices
"""
df = pd.read_csv("edge_list.csv")
V_u = df['source'].unique()
V_g = df['target'].unique() #V_g: group set

print("Unique user count",len(V_u))
print("Unique group count",len(V_g))

# df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True )
# encoders = [(["source"], LabelEncoder()), (["target"], LabelEncoder())]
# mapper = DataFrameMapper(encoders, df_out=True)
# new_cols = mapper.fit_transform(df.copy())
# df = pd.concat([df.drop(columns=["source", "target"]), new_cols], axis="columns")


"""
V_u(G): User set
V_g(G): Group set
"""
V_u = df['source'].unique()
V_g = df['target'].unique() #V_g: group set

print("Unique user count",len(V_u))
print("Unique group count",len(V_g))


DG=nx.from_pandas_edgelist(df, 'source', 'target',create_using=nx.DiGraph())
print(len(DG.nodes()))


colors = [node[1]['color'] for node in DG.nodes(data=True)]
pos = nx.spring_layout(DG)
# nx.set_node_attributes(DG,attributes,"size")
nx.draw(DG,pos = pos,with_labels=False,font_size=8,node_color=colors)
# nx.draw_networkx_edge_labels(DG,pos=pos,font_size=8)
plt.show()


"""
Neighbour count
"""
data=np.array([len(set(DG.neighbors(u))) for u in V_u])
c = Counter(data)
print(c)
