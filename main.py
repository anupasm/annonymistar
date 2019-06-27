import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter
import math
import json
import Levenshtein as lev
import cost_cal
df = pd.read_csv("edge_list.csv")
k = 3

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
week_neigbours = []
first_week = per_day_data[0][10:20]

target_nodes = df['target'].unique()
G=nx.from_pandas_edgelist(first_week, 'source', 'target',create_using = nx.MultiDiGraph(),edge_attr=True)
user_list = [ u for u in G.node if not u in target_nodes]
neighbour_vector = {user:[] for user in user_list}
cost_vector = {user:[] for user in user_list}
annonymized_vector = []
print(first_week)
for user in G.nodes():
    if user in user_list:
        sorted_edges= list(G.edges(user,data=True))
        sorted_edges.sort(key=lambda x:x[2]['timestamp'])
        details = {user:[(group,time['timestamp']) for user,group,time in sorted_edges]}
        neighbour_vector.update(details) 


neighbour_vector = sorted(neighbour_vector.items(),key=lambda x:len(x[1]),reverse=True)

groups = {}
for node in neighbour_vector:
    sig = ''.join([str(chr(n[0]+40)) for n in node[1]])
    if not sig in groups.keys():
        groups[sig] = [node[0]]
    else:
        groups[sig].append(node[0])

# for k,v in groups.items():
    # print(k,[x[0] for x in v])
# print()
groups = sorted(groups.items(),key = lambda x: len(x[1]),reverse = True)
candidate_list = []
while groups:
    group = groups.pop()
    candidates = []
    for sub_group in groups:
        print(group[0],sub_group[0])
        cost = cost_cal.get_cost(group[0],sub_group[0])
        candidates.append((sub_group,cost))
    candidates.sort(key = lambda x: (x[1],-len(x[0][1])))
    candidate_list.append((group,candidate_list))

for c in candidate_list:
    print([x[1] for x in c])
print()
    # if len(neighbour_vector) >= (2*k-1):
    #     candidates = candidates[:(k-1)]
    # else:
    #     candidates = [ c for c in candidates if not c in annonymized_vector]
    
