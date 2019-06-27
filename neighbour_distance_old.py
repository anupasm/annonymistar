import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter

import json
import matplotlib.pyplot as plt
import Levenshtein as lev

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
for week in per_day_data:
    neighbors = {}
    G=nx.from_pandas_edgelist(week, 'source', 'target',create_using = nx.MultiDiGraph(),edge_attr=True)
    for user in G.nodes():
        if user in u_user_list:
            sorted_edges= list(G.edges(user,data=True))
            sorted_edges.sort(key=lambda x:x[2]['timestamp'])
            details = {user:[(group,time['timestamp']) for user,group,time in sorted_edges]}
            neighbors.update(details) 
    week_neigbours.append(neighbors)




selected_nodes = {}
encoded_neighbors = []
group_no = 0

def get_min_distance_vect(u1,n1,week_neigbours):
    min_vector = []
    for u2, n2 in week_neigbours:
        if u1 == u2: continue
        #encode integers to values
        n1_e = ''.join([str(chr(n[0]+40)) for n in n1])
        n2_e = ''.join([str(chr(n[0]+40)) for n in n2])

        #Levenshtein of two words
        dist = lev.distance(n1_e,n2_e)
        min_vector.append((u2,dist))
    min_vector.sort(key = lambda x: x[1])    
    return min_vector

print(len(week_neigbours[0]))
for u1, n1 in week_neigbours[0].items():
    min_vector = get_min_distance_vect(u1,n1,week_neigbours[0].items())
    if u1 in selected_nodes.keys(): 
        group = selected_nodes[u1]
    else:#if node has not been already added
        group = group_no
        group_no += 1

    count = 0
    for node in min_vector:
        if not node[1] == 0 and count >= k:
            break
        
        if node[0] in selected_nodes.keys():
            continue
        selected_nodes.update({node[0]:group})
        count +=1

for i in range(group_no+1):
    keys_iter = filter(lambda k: selected_nodes[k] == i, selected_nodes.keys()) # return an iterator

    for j in keys_iter:
        print(week_neigbours[0][j])

    print("xxxxxxxxxxxxxxxxxxxxxxxxxxxx")