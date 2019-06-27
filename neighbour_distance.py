import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter
import math
import json
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

def get_min_distance_vect(u1,n1,week_neigbours):
    min_vector = []
    for u2, n2 in week_neigbours:
        if u1 == u2: continue
        #encode integers to values
        n1_e = ''.join([str(chr(n[0]+40)) for n in n1])
        n2_e = ''.join([str(chr(n[0]+40)) for n in n2])
        #Levenshtein of two words
        dist = lev.distance(n1_e,n2_e)
        # print(u1,u2,[n[0] for n in n1],[n[0] for n in n2],dist)
        min_vector.append((u2,dist))
    min_vector.sort(key = lambda x: x[1])    
    return min_vector
# week_neigbours[0].sort(key = lambda x:x.count())

min_vectors_week = {}
for u1, n1 in week_neigbours[0].items():
    min_vector = get_min_distance_vect(u1,n1,week_neigbours[0].items())
    min_vectors_week.update({u1:min_vector})
    # print(u1,min_vector)

sorted_with_max_0 = sorted(min_vectors_week.items(), key=lambda uv: Counter(v[1] for v in uv[1])[0],reverse=True)

selected_nodes = {}
group_no = 0

for users in sorted_with_max_0:
    # print(users[0])
    if users[0] in selected_nodes.keys(): 
        group = selected_nodes[users[0]]
    else:#if node has not been already added
        group = group_no
        selected_nodes.update({users[0]:group})
        group_no += 1

    # count = 0
    for node in users[1]:
        if node[1] == 0:
            # print(node[0],"added to ",group)
            selected_nodes.update({node[0]:group})

        # if not node[1] == 0 and count >= k:
        #     print("k exceeded")
        #     break
        
        # # if node[0] in selected_nodes.keys():
        # #     print(node[0],"alread in list")
        # #     count +=1
        # #     continue
        # print(node[0],"added to ",group)
        # selected_nodes.update({node[0]:group})
        # count +=1

processed_neigbours = {}

for i in range(group_no):
    keys_iter = filter(lambda n: selected_nodes[n] == i, selected_nodes.keys()) 
    group_list = list(keys_iter)
    if len(group_list) >= k:
        for j in group_list:
            group = 'g'+str(i)
            processed_neigbours.update({group:week_neigbours[0][j]})
            # print({group:week_neigbours[0][j]})
            break
    else:
        for j in group_list:
            processed_neigbours.update({j:week_neigbours[0][j]})
            # print({j:week_neigbours[0][j]})

COST_WEIGHTS = {
    "insert":1,
    "replace":5,
    "delete": 3
}

def get_consecutive_count(word,char):
    count=0
    for i in word:
        if i == char:
            count+=1
        else:
            break
    return count

def exec_op(op,source_word,pos,char):

    part1 = source_word[:pos-1] if pos != 0 else ''
    part2 = source_word[pos+1:] if pos+1 < len(source_word) else ''  
    consecutive_count_1 = get_consecutive_count(part1[::-1],char)
    consecutive_count_2 = get_consecutive_count(part2,char)
    total = consecutive_count_1+consecutive_count_2+1 #min 1 (denote the inserted char)
    cost = COST_WEIGHTS[op]/(total)
    print(op,"total",total,"cost",cost)
    return cost

def exec_ops(ops,source_word,target_word):
    cost = 0
    
    for op in ops:
        action = op[0]
        source_pos = op[1]
        target_pos = op[2]
        if op[0] == 'delete':
            cost += exec_op(action,source_word,source_pos,source_word[source_pos])
        else:
            cost += exec_op(action,source_word,source_pos,target_word[target_pos])
    return cost
        
def exec_insert(op,source_word,target_word):
    insert_pos = op[1]
    insert_char = target_word[op[2]]
    part1 = source_word[:insert_pos-1] if insert_pos != 0 else ''
    part2 = source_word[insert_pos+1:] if insert_pos+1 < len(source_word) else ''  
    consecutive_count_1 = get_consecutive_count(part1[::-1],insert_char)
    consecutive_count_2 = get_consecutive_count(part2,insert_char)
    total = consecutive_count_1+consecutive_count_2+1 #min 1 (denote the inserted char)
    cost = COST_WEIGHTS['insert']/(total)
    adjusted_word = part1 + insert_char + part2

    return adjusted_word,cost

n1_e ='rrrr'
n2_e = 'rrertr'
print(n1_e,n2_e)       
ops = lev.editops(n1_e,n2_e)
print(ops)
print("cost:",exec_ops(ops,n1_e,n2_e))

def adjust_neighbors(u1,n1,week_neigbours):
    min_vector = []
    for u2, n2 in week_neigbours:
        if (type(u1) ==str) or (type(u1) ==str and type(u2) ==str) or u1 == u2:
            continue
        #encode integers to values
        n1_e = ''.join([str(chr(n[0]+40)) for n in n1])
        n2_e = ''.join([str(chr(n[0]+40)) for n in n2])
        #Levenshtein of two words
        dist = lev.distance(n1_e,n2_e)
            # print(u1,u2,[n[0] for n in n1],[n[0] for n in n2])
        print(u1,u2,n1_e,n2_e)       
        ops = lev.editops(n1_e,n2_e)
        print(ops)
        print("cost:",exec_ops(ops,n1_e,n2_e))

                        # print()
        # print(u1,u2,[n[0] for n in n1],[n[0] for n in n2],dist)

        min_vector.append((u2,dist))
    min_vector.sort(key = lambda x: x[1])    
    return min_vector

# for n,v in processed_neigbours.items():
#     adjust_neighbors(n,v,processed_neigbours.items())
    # print(n,[x[0] for x in v])
