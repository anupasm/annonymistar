import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter

import json
import matplotlib.pyplot as plt

df = pd.read_csv("edge_list.csv")


df = df.sort_values(by=['timestamp'])
df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True )
encoders = [(["source"], LabelEncoder()), (["target"], LabelEncoder())]
mapper = DataFrameMapper(encoders, df_out=True)
new_cols = mapper.fit_transform(df.copy())
df = pd.concat([df.drop(columns=["source", "target"]), new_cols], axis="columns")
u_user_list = df['source'].unique()
degree_vector = {user:[] for user in u_user_list}
# print(degree_vector)
per_day_data = [g for n, g in df.groupby(pd.Grouper(key='timestamp',freq='W'))]
week_neigbours
for week in per_day_data:
neighbors = []
    G=nx.from_pandas_edgelist(week, 'source', 'target',create_using = nx.MultiDiGraph(),edge_attr=True)
    for user in G.nodes():
        if user in u_user_list:
                sorted_edges= list(G.edges(user,data=True))
                sorted_edges.sort(key=lambda x:x[2]['timestamp'])
                neighbors.append({user:[ (group,time['timestamp']) for user,group,time in sorted_edges]})
        
        print(neighbors)

