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

json_data = json.dumps(nodes, indent=4, separators=(',', ': '))

text_file = open("data.json", "w")
text_file.write(json_data)
text_file.close()


# def treeToJson(decision_tree, feature_names=None):
#   from warnings import warn
 
#   js = ""
 
#   def node_to_str(tree, node_id, criterion):
#     if not isinstance(criterion, sklearn.tree.tree.six.string_types):
#       criterion = "impurity"
 
#     value = tree.value[node_id]
#     if tree.n_outputs == 1:
#       value = value[0, :]
 
#     jsonValue = ', '.join([str(x) for x in value])
 
#     if tree.children_left[node_id] == sklearn.tree._tree.TREE_LEAF:
#       return '"id": "%s", "criterion": "%s", "impurity": "%s", "samples": "%s", "value": [%s]' \
#              % (node_id, 
#                 criterion,
#                 tree.impurity[node_id],
#                 tree.n_node_samples[node_id],
#                 jsonValue)
#     else:
#       if feature_names is not None:
#         feature = feature_names[tree.feature[node_id]]
#       else:
#         feature = tree.feature[node_id]
 
#       if "=" in feature:
#         ruleType = "="
#         ruleValue = "false"
#       else:
#         ruleType = "<="
#         ruleValue = "%.4f" % tree.threshold[node_id]
 
#       return '"id": "%s", "rule": "%s %s %s", "%s": "%s", "samples": "%s"' \
#              % (node_id, 
#                 feature,
#                 ruleType,
#                 ruleValue,
#                 criterion,
#                 tree.impurity[node_id],
#                 tree.n_node_samples[node_id])
 
#   def recurse(tree, node_id, criterion, parent=None, depth=0):
#     tabs = "  " * depth
#     js = ""
 
#     left_child = tree.children_left[node_id]
#     right_child = tree.children_right[node_id]
 
#     js = js + "\n" + \
#          tabs + "{\n" + \
#          tabs + "  " + node_to_str(tree, node_id, criterion)
 
#     if left_child != sklearn.tree._tree.TREE_LEAF:
#       js = js + ",\n" + \
#            tabs + '  "left": ' + \
#            recurse(tree, \
#                    left_child, \
#                    criterion=criterion, \
#                    parent=node_id, \
#                    depth=depth + 1) + ",\n" + \
#            tabs + '  "right": ' + \
#            recurse(tree, \
#                    right_child, \
#                    criterion=criterion, \
#                    parent=node_id,
#                    depth=depth + 1)
 
#     js = js + tabs + "\n" + \
#          tabs + "}"
 
#     return js
 
#   if isinstance(decision_tree, sklearn.tree.tree.Tree):
#     js = js + recurse(decision_tree, 0, criterion="impurity")
#   else:
#     js = js + recurse(decision_tree.tree_, 0, criterion=decision_tree.criterion)
 
#   return js

# print treeToJson(dt.tree_, df.columns)