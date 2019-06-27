import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter

import json


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
for day in per_day_data:
    # print("----day start----")
    G=nx.from_pandas_edgelist(day, 'source', 'target',create_using = nx.MultiDiGraph(),edge_attr=True)
    for u in u_user_list:
        if u not in G.nodes:
            degree_vector[u].append(0)
    for node,val in G.degree() :
        degree_vector[node].append(val)

vector = [y for x,y in degree_vector.items()]
vector_set = set()
for x in vector:
    vector_set.add(tuple(x))

print([y for x,y in Counter([tuple(t) for t in vector]).items() if y == 2])
print(len(vector))

# uniq_target = df.target.unique()
# degree_sequence = sorted([d for n, d in G.degree() if n not in uniq_target], reverse=True)  # degree sequence
# degree = []
# print(len(df.target.unique()))
# print(len(df.source.unique()))

# for node,val in G.degree():
#     if not node in df.target.unique():
#         degree.append(val)
# ones = []
# for c,f in Counter(degree_sequence).items():
#         if f == 1:
#                 ones.append(c)
# ones.sort()
# print(ones)