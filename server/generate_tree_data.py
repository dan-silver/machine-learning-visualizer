import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import sklearn.tree
from sklearn import tree
import json
import random

# dummy data:
import dummy_data
data, labels = dummy_data.generate(20*1000, ['Age', 'Weight', 'Hair Color'])

# create decision tree
dt = DecisionTreeClassifier()
dt.fit(data[0], data[1])

def print_tree(t, root=0):
    left_child = t.children_left[root]
    right_child = t.children_right[root]
     
    if left_child != sklearn.tree._tree.TREE_LEAF:
        this_branch = {
        	'name': '%s < %.2f' % (labels[t.feature[root]], t.threshold[root]),
        	'count': t.n_node_samples[root],
        	'impurity': t.impurity[root]
        }

        children = []
        left_child = print_tree(t, root=left_child)
        right_child = print_tree(t, root=right_child)
        if left_child:
          children.append(left_child)
        if right_child:
          children.append(right_child)
        
        this_branch['children'] = children
    	return this_branch
    else:
      return {
        'name': 'leaf',
        'count': t.n_node_samples[root]
      }



nodes = print_tree(dt.tree_)

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