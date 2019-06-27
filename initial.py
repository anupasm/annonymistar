import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter

import json


df = pd.read_csv("edge_list.csv")[0:100]
df = df.sort_values(by=['timestamp'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit = 's')
per_day_data = [g for n, g in df.groupby(pd.Grouper(key='timestamp',freq='D'))]
for day in per_day_data:
        G=nx.from_pandas_edgelist(day, 'source', 'target',create_using = nx.MultiDiGraph(),edge_attr=True)
        for node,val in G.degree() :
                if val > 1:
                        print(node,val,[n for n in nx.all_neighbors(G, node)])
uniq_target = df.target.unique()
degree_sequence = sorted([d for n, d in G.degree() if n not in uniq_target], reverse=True)  # degree sequence
# degree = []
# print(len(df.target.unique()))
# print(len(df.source.unique()))

# for node,val in G.degree():
#     if not node in df.target.unique():
#         degree.append(val)
ones = []
for c,f in Counter(degree_sequence).items():
        if f == 1:
                ones.append(c)
ones.sort()
print(ones)