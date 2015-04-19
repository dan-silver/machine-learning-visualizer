from __future__ import division
import sklearn.tree
from sklearn import tree
import json
from math import log10, floor

def round_sig(x, sig=4):
  return round(x, sig-int(floor(log10(x)))-1)

class ConvertTreeToJSON(object):
    def __init__(self, tree, labels):
        self.dt = tree
        self.labels = labels
        self.t = tree.tree_

    def print_tree(self, side, root=0):
        left_child = self.t.children_left[root]
        right_child = self.t.children_right[root]
        dataPercentage = round_sig(self.t.n_node_samples[root] / self.dt.tree_.n_node_samples[0] * 100) # this nodes count / the root nodes count
        if left_child == sklearn.tree._tree.TREE_LEAF:
            return {
                'name': 'leaf',
                'side': side,
                'count': self.t.n_node_samples[root],
                'dataPercentage': dataPercentage
            }
        else:
            left_child = self.print_tree('left', root=left_child)
            right_child = self.print_tree('right', root=right_child)
            return {
                'side': side,
                'feature': self.labels[self.t.feature[root]],
                'featureIdx': self.t.feature[root],
                'threshold': self.t.threshold[root],
                'count': self.t.n_node_samples[root],
                'impurity': round_sig(self.t.impurity[root]),
                'children': [left_child, right_child],
                'dataPercentage': dataPercentage
            }


    def convert(self):
        nodes = self.print_tree('top')

        # hack to generate png from python
        # import os

        # tree.export_graphviz(dt, out_file='tree.dot')
        # os.system("dot -Tpng tree.dot -o tree.png")

        return json.dumps(nodes) # Add indent=4, separators=(',', ': ') for human readable version