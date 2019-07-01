import cost_cal
import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter
import math
import json
import Levenshtein as lev
import matplotlib.pyplot as plt
from itertools import combinations 

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

    sub_graphs = nx.weakly_connected_component_subgraphs(DG)
    return sub_graphs
import random
def merge(return_groups,sub_graphs,merged_group_list):
    cost = 0
    temp = dict(return_groups)
    # print(temp)
    for sg in sub_graphs:
        sizes = nx.get_node_attributes(sg,'size')
        sorted_edges = sorted(sg.edges(data=True),key= lambda x: (x[2]['weight'])/(sizes[x[0]]+sizes[x[1]]))
        print("sorted_edges",sorted_edges)
        merge = sorted_edges[0] #least cost
        cost += merge[2]['weight']
        print(merge[0], "goes to",merge[1],"at cost",merge[2]['weight'],"total",cost)
        replacing_group = temp.pop(merge[0]) 
        temp[merge[1]] += replacing_group
        merged_group_list[merge[0]] = merge[1]

        print("edges",sg.edges())
        print()
        

    return_groups = [(k,v) for k,v in temp.items()]
    return return_groups,cost,merged_group_list

"""
groups: combined groups
k: k-annonymity param

"""
def merge_groups(groups,k):
    candidate_list = []#candidate_list : [(group,its_length),[list of other groups (group,cost,size)]]
    group_count = len(groups)
    merged_group_list = {}
    #calculating the cost of transforming group x group
    return_groups = groups.copy()
    total_cost = 0
    while True:
        group_count,candidate_list = get_group_costs(return_groups,group_count,k)
        # for c in candidate_list:
        #     print(c)
        # break
        if not group_count: break

        sub_graphs = get_sub_graphs(candidate_list)

        return_groups, cost,merged_group_list = merge(return_groups,sub_graphs,merged_group_list)
        
        for m,v in merged_group_list.items():
            print(m,v)
        group_count = len(return_groups)
        total_cost += cost
        print()
        print("^^^^^^^^^^^^",group_count,total_cost)
        print()

    print(len(return_groups),total_cost)

        
