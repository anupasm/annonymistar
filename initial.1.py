import pandas as pd
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter

import json


data = json.load(open('interactionsWithReactions.json'))
nint = []
reaction_types = []
for user in data:
        nint.append(len(data[user]))
        for interaction in data[user]:
                reaction_types.append(interaction['interactionType'])
                group_id = interaction['groupId']
                time = interaction['time']
                interaction_type = interaction['interactionType']
                if interaction_type == 'comment':
                        print("{0},{1},{2}".format(user,group_id,time))
                # print("{0},{1}".format(user,group_id))


