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
from scipy import stats
k = 2
flag = 0

def normalized_hist(freq_list):
    imhist,bins = np.histogram(freq_list,20,density=True)
    stats.ks_2samp(, rvs2)
    rvs1 = stats.norm.rvs(size=5, loc=0., scale=1)
    print(rvs1)
    print(imhist)
    print(bins)

def plot_hist(c,id,type):
    plt.clf()
    plt.bar(c.keys(),c.values())
    plt.xlabel('Neighbour Size')
    plt.ylabel('Users')
    plt.yscale('log')
    plt.savefig(type+'_week_'+str(id)+'.png')

def get_group_costs(return_groups,group_count,k):
    candidate_list = []
    for group in return_groups:
        candidates = []
        if len(group[1]) >= k: 
            group_count -= 1
            continue 
        for sub_group in return_groups:
            if group[0] == sub_group[0]: continue
            cost = cost_cal.get_cost(group[0],sub_group[0])
            candidates.append((sub_group,cost))
        candidates.sort(key = lambda x: (x[1],-len(x[0][1])))  #group by cost and size
        candidate_list.append((group[0],len(group[1]),[(x[0][0],round(x[1],2),len(x[0][1])) for x in candidates]))
    return group_count,candidate_list

def get_sub_graphs(candidate_list):
    DG=nx.DiGraph() #create graph such that (node -> closest patern)
    attributes = {}
    for c in candidate_list:
        #node values
        main_string = c[0]
        main_size = c[1]
        #lowest cost + biggest size group
        match = c[2][0][0]
        cost = c[2][0][1]
        match_size = c[2][0][2]
        attributes.update({main_string:main_size})
        attributes.update({match:match_size})
        DG.add_weighted_edges_from([(main_string,match,cost)])
        

    # pos = nx.spring_layout(DG)
    nx.set_node_attributes(DG,attributes,"size")
    # nx.draw(DG,pos = pos,with_labels=True,font_size=8,labels = dict(attributes))
    # nx.draw_networkx_edge_labels(DG,pos=pos,font_size=8)
    # plt.show()
    sub_graphs = nx.weakly_connected_component_subgraphs(DG)
    return sub_graphs

def merge(return_groups,sub_graphs,merged_group_list,dummy):
    cost = 0
    temp = dict(return_groups)
    for sg in sub_graphs:
        sizes = nx.get_node_attributes(sg,'size')
        sorted_edges = sorted(sg.edges(data=True),key= lambda x: (x[2]['weight']))#/(sizes[x[0]]+sizes[x[1]]))
        merge = sorted_edges[0] #least cost

        cost_to_create = cost_cal.cost_to_create(merge[0],sizes[merge[1]])
        if merge[2]['weight'] > cost_to_create :
            cost += cost_to_create
            for i in range(sizes[merge[1]]):
                dummy += 1
                temp[merge[0]] += ['D'+str(dummy)]
            # merged_group_list[merge[0]] = (merge[0],merge[2]['weight'],(sizes[merge[1]]+sizes[merge[0]]))
            continue

        cost += merge[2]['weight']
        # if merge[0]== 2942:
        
        replacing_group = temp.pop(merge[0]) 
        # print(replacing_group,merge[0], "goes to",merge[1],"at cost",merge[2]['weight'],"total",cost)
        temp[merge[1]] += replacing_group
        
        merged_group_list[merge[0]] = (merge[1],merge[2]['weight'],(sizes[merge[1]]+sizes[merge[0]]))

        if flag: print("edges",sg.edges())
        

    return_groups = [(k,v) for k,v in temp.items()]
    # for r in return_groups:
    #     print(r)
    
    return return_groups,cost,merged_group_list,dummy

"""
groups: combined groups  [ list of (string,[node list])]
k: k-annonymity param

"""
def merge_groups(groups,k):

    #candidate_list : [(group,its_length),[list of other groups (group,cost,size)]]
    candidate_list = []
    
    #group count initially
    group_count = len(groups)

    #merged groups : [group1: (<group2 which group1 merged to>,<cost>,<total size>)]
    merged_group_list = {} 

    return_groups = groups.copy()

    """
    calculating the cost of transforming group x group
    """
    total_cost = 0

    """
    For newly created nodes
    """
    dummy = 0
    while True:

        """
        calculate the cost of transforming into other group/string
        """
        group_count,candidate_list = get_group_costs(return_groups,group_count,k)
        
        #every groups is at least k size group_count will be zero
        if not group_count: 
            break

        """
        create indipendent sub graphs of dependencies
        """ 
        sub_graphs = get_sub_graphs(candidate_list)

        
        """
        merge groups with lowest cost of each sub graph, returns merged graphs
        """
        return_groups, cost, merged_group_list,dummy = merge(return_groups,sub_graphs,merged_group_list,dummy)

        group_count = len(return_groups) #update count
        total_cost += cost #update cost


    action_count = {'insert':0,'replace':0,'delete':0}
    total = 0
    for m,v in merged_group_list.items():
        # print(m,v)
        cost, action_count = cost_cal.get_cost(m,v[0],action_count)
        total += cost

    print(action_count,total)

    return return_groups

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

"""
Original G
"""
G_org = nx.from_pandas_edgelist(df, 'source', 'target',create_using = nx.MultiDiGraph())

"""
G = G_1,G_2 ... G_T
Group data week by week.
"""
per_week_data = [g for n, g in df.groupby(pd.Grouper(key='timestamp',freq='W'))]


final_list = []
"""
For every t generate graph G_t and find k-annonymity
"""
for i,week in enumerate(per_week_data):
    G=nx.from_pandas_edgelist(week, 'source', 'target',create_using = nx.MultiDiGraph(),edge_attr=True)

    #V_u(G_t): user set of this week
    user_list = [ u for u in G.node if u in V_u] 
    neighbour_vector = {user:[] for user in user_list}


    """
    Creation of neighbour vector for all edges
    Neighbours are sorted by timestamp
    """
    for user in G.nodes():
        if user in user_list:
            sorted_edges= list(G.edges(user,data=True))
            sorted_edges.sort(key=lambda x:x[2]['timestamp']) #sort by timestamp
            details = {user:[(group,time['timestamp']) for user,group,time in sorted_edges]}
            neighbour_vector.update(details) 

    """
    Sort vertices which has highest number of neighbours
    """
    neighbour_vector = sorted(neighbour_vector.items(),key=lambda x:len(x[1]),reverse=True)

    """
    Frequency graphs
    """
    # data=np.array([len(u[1]) for u in neighbour_vector])
    # c = Counter(data)
    # plot_hist(c,i,'original')
    # print("Week",i,": Neighbour Counts:",dict(c))

    normalized_hist([len(u[1]) for u in neighbour_vector])
    """
    Encode neighbour vector into Unicode strings.
    Group Users into string/neighbourhood groups
    """
    groups = {}
    for node in neighbour_vector:
        sig = ''.join([str(chr(n[0]+40)) for n in node[1]])
        if not sig in groups.keys():
            groups[sig] = [node[0]]
        else:
            groups[sig].append(node[0])


    #sort group with highest size to lowest
    groups = sorted(groups.items(),key = lambda x: len(x[1]),reverse = True) 
    week_final = merge_groups(groups,k)
    final_list.append(week_final)
    break

"""
Create the new k-anonymous graph
"""
G_dash = nx.MultiDiGraph()
for i,week in enumerate(final_list):
    frequency = []
    for group in week:
        actual_neighbours = [(ord(c)-40) for c in group[0]]
        for node in group[1]:
            frequency.append(len(actual_neighbours))
            for an in actual_neighbours:
                G_dash.add_edge(node,an)

    c = Counter(frequency)
    plot_hist(c,i,'processed')
    
    print("Processed Week",i,": Neighbour Counts:",dict(c))

# nx.write_gexf(G_dash, "output.gexf")


nx.write_edgelist(G_org, "input.csv", delimiter=',',data=False)
nx.write_edgelist(G_dash, "output.csv", delimiter=',',data=False)




























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