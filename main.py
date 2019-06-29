import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter
import math
import json
import Levenshtein as lev
import cost_cal
import matplotlib.pyplot as plt
from itertools import combinations 

df = pd.read_csv("edge_list.csv")
k = 4

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
first_week = per_day_data[0]

target_nodes = df['target'].unique()
G=nx.from_pandas_edgelist(first_week, 'source', 'target',create_using = nx.MultiDiGraph(),edge_attr=True)
user_list = [ u for u in G.node if not u in target_nodes]
neighbour_vector = {user:[] for user in user_list}
cost_vector = {user:[] for user in user_list}
annonymized_vector = []
# print(first_week)
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
groups = sorted(groups.items(),key = lambda x: len(x[1]),reverse = True) #sort group with highest size to lowest
# for k in groups:
    # print(k[0],k[1])
# print()

candidate_list = []
# while groups:
    # group = groups.pop()
for group in groups:
    candidates = []
    if len(group[1]) >= k: continue
    for sub_group in groups:
        if group[0] == sub_group[0]: continue
        # print(group[0],sub_group[0])
        cost = cost_cal.get_cost(group[0],sub_group[0])
        candidates.append((sub_group,cost))
    candidates.sort(key = lambda x: (x[1],-len(x[0][1])))
    # print(group)#,"--",candidates)
    candidate_list.append((group[0],len(group[1]),[(x[0][0],round(x[1],2),len(x[0][1])) for x in candidates]))
DG=nx.DiGraph()
attributes = {}
for c in candidate_list:
    main_string = c[0]
    main_size = c[1]
    match = c[2][0][0]
    cost = c[2][0][1]
    match_size = c[2][0][2]
    attributes.update({main_string:main_size})
    attributes.update({match:match_size})
    DG.add_weighted_edges_from([(main_string,match,cost)])


pos = nx.spring_layout(DG)
nx.set_node_attributes(DG,attributes,"size")
nx.draw(DG,pos = pos,with_labels=True,font_size=8,labels = dict(attributes))
nx.draw_networkx_edge_labels(DG,pos=pos,font_size=8)

sub_graphs = nx.weakly_connected_component_subgraphs(DG)

for i, sg in enumerate(sub_graphs):
    # print("subgraph {} has {} nodes".format(i, len(sg)))
    print("Nodes:", sg.nodes())
    all_nodes = list(sg.nodes())
    all_nodes.sort()
    # print("\tEdges:", [sg[k[0]][k[1]] for k in sg.edges()])
    sg.add_node("start")
    sg.add_node("end")
    sg.add_edges_from([(n,"end") for n in sg.nodes()])
    sg.add_edges_from([("start",n) for n in sg.nodes()])
    all_paths = []
    for path in nx.all_simple_paths(sg, source="start", target="end"):
        if len(path)>3: #start+end+1 node no use

            size_sum = sum([sg.node[x]['size'] for x in path[1:-1]])
            cost_sum = sum([sg[path[i]][path[i+1]]['weight'] for i in range(1,len(path)-2)])
            all_paths.append((path[1:-1],size_sum,cost_sum))
    all_paths.sort(key= lambda x : x[2])
    
    for path1 in all_paths:
        
        matched_set = path1[0]
        groups = [path1]
        for path2 in all_paths:
            if any(x in matched_set for x in path2[0]):
                continue
            else:
                matched_set += path2[0]
                groups.append(path2)
        matched_set.sort()
        print(matched_set)
        print(matched_set == all_nodes)

    print("--------------------\n")


# all_paths = []
# for path in nx.all_simple_paths(DG, source="start", target="end"):

#     size_sum = sum([DG.node[x]['size'] for x in path[1:-1]])
#     cost_sum = sum([DG[path[i]][path[i+1]]['weight'] for i in range(1,len(path)-2)])
#     # if size_sum >= k :
#     print(path[1:-1],size_sum,cost_sum)
#     all_paths.append((path[1:-1],size_sum,cost_sum))

# combination_list = list(range(len(all_paths)))
# for i in range(len(all_paths)):
#     print(list(combinations(combination_list,i)))