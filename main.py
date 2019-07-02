import pandas as pd
import networkx as nx
from collections import Counter
import math
import json
import Levenshtein as lev
import matplotlib.pyplot as plt
from itertools import combinations 
import merge
from sklearn.preprocessing import LabelEncoder
from sklearn_pandas import DataFrameMapper

k = 4

"""
Read the csv file(source,target,timestamp) and relabel vertices
"""
df = pd.read_csv("edge_list.csv")
df = df.sort_values(by=['timestamp'])
df['timestamp'] = pd.to_datetime(df['timestamp'], infer_datetime_format=True )
encoders = [(["source"], LabelEncoder()), (["target"], LabelEncoder())]
mapper = DataFrameMapper(encoders, df_out=True)
new_cols = mapper.fit_transform(df.copy())
df = pd.concat([df.drop(columns=["source", "target"]), new_cols], axis="columns")


"""
V_u(G): User set
V_g(G): Group set
"""
V_u = df['source'].unique()
V_g = df['target'].unique() #V_g: group set

degree_vector = {user:[] for user in V_u} #initialize degree

"""
G = G_1,G_2 ... G_T
Group data week by week.
"""
per_day_data = [g for n, g in df.groupby(pd.Grouper(key='timestamp',freq='W'))]
week_neigbours = []
first_week = per_day_data[0]

G=nx.from_pandas_edgelist(first_week, 'source', 'target',create_using = nx.MultiDiGraph(),edge_attr=True)
user_list = [ u for u in G.node if not u in V_g] #V_u(G_t): user set of this week
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


merges = []
groups = sorted(groups.items(),key = lambda x: len(x[1]),reverse = True) #sort group with highest size to lowest
merge.merge_groups(groups,k)

































    # print("\tEdges:", [sg[k[0]][k[1]] for k in sg.edges()])
    # sg.add_node("start")
    # sg.add_node("end")
    # sg.add_edges_from([(n,"end") for n in sg.nodes()])
    # sg.add_edges_from([("start",n) for n in sg.nodes()])
    # all_paths = []
    # for path in nx.all_simple_paths(sg, source="start", target="end"):
    #     if len(path)>3: #start+end+1 node no use

    #         size_sum = sum([sg.node[x]['size'] for x in path[1:-1]])
    #         cost_sum = sum([sg[path[i]][path[i+1]]['weight'] for i in range(1,len(path)-2)])
    #         all_paths.append((path[1:-1],size_sum,cost_sum)) # connected path, size of path, sum of costs
    # all_paths.sort(key= lambda x : x[2]) #sort by sum of costs lesser to higher
    
    # #for each path find non overalaping path such that cost is minimum and all nodes included
    # merged_groups = []
    # posible_set = []

    # print("------------")
    # print("all paths",all_paths)
    # for i, path1 in enumerate(all_paths):
    #     matched_set = path1[0] 
    #     groups = [path1]
    #     all_paths_check = all_paths[i+1:].copy()
    #     all_paths_check.append(([],0,0)) #cheking itself with empty
    #     for path2 in all_paths_check:        
    #         print(path1,"against",path2)
    #         if any(x in matched_set for x in path2[0]):
    #             print("overlapped")
    #         else:
    #             print("non overlap")
    #             posible_set.append((matched_set,path2[2])) #node set and cost

    #         print()
    #             continue
    #         else:
    #             print("non overlap")
    #             matched_set += path2[0]
    #             groups.append(path2)
    #     matched_set.sort()
    #     # print(matched_set)
    #     # print(matched_set == all_nodes)
    #     if matched_set == all_nodes:
    #         posible_set.append((matched_set,path2[2])) #node set and cost
    
    # print("possible set")
    # for p in posible_set:
    #     print(p[0],p[1])
    # # merged_groups.append(sorted(posible_set,lambda x: x[1])[0]) #append the lowest cost set

    # print("--------------------\n")


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