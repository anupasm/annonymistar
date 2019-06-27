import pandas as pd
import json
from sklearn_pandas import DataFrameMapper
from sklearn.preprocessing import LabelEncoder
import networkx as nx
from collections import Counter

data = json.load(open('interactionsWithReactions.json'))
for 
for interaction in data:
    group_id = interaction['groupId']
    time = interaction['time']
    interaction_type = interaction['interactionType']