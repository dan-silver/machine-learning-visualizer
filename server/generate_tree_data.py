from __future__ import division
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import sklearn.tree
from sklearn import tree
import json
import random
from math import log10, floor

def round_sig(x, sig=4):
  return round(x, sig-int(floor(log10(x)))-1)

import dummy_data
data, labels = dummy_data.generate(20*1000, ['Age', 'Weight', 'Hair Color', 'Birth City', 'Current City'])

# create decision tree
dt = DecisionTreeClassifier()
dt.fit(data[0], data[1])

def print_tree(t, side, root=0):
    left_child = t.children_left[root]
    right_child = t.children_right[root]
    dataPercentage = round_sig(t.n_node_samples[root] / dt.tree_.n_node_samples[0] * 100) # this nodes count / the root nodes count
    if left_child == sklearn.tree._tree.TREE_LEAF:
        return {
            'name': 'leaf',
            'side': side,
            'count': t.n_node_samples[root],
            'dataPercentage': dataPercentage
        }
    else:
        left_child = print_tree(t, 'left', root=left_child)
        right_child = print_tree(t, 'right', root=right_child)
        return {
            'side': side,
            'feature': labels[t.feature[root]],
            'featureIdx': t.feature[root],
            'threshold': t.threshold[root],
            'count': t.n_node_samples[root],
            'impurity': round_sig(t.impurity[root]),
            'children': [left_child, right_child],
            'dataPercentage': dataPercentage
        }

nodes = print_tree(dt.tree_, 'top')

# hack to generate png from python
# import os

# tree.export_graphviz(dt, out_file='tree.dot')
# os.system("dot -Tpng tree.dot -o tree.png")

json_data = json.dumps(nodes) # Add indent=4, separators=(',', ': ') for human readable version

text_file = open("data.json", "w")
text_file.write(json_data)
text_file.close()