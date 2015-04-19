# machine-learning-visualizer
Starting with decision trees, plan to add more classifiers

Video of decision tree path visualization - https://www.youtube.com/watch?v=Attpwnz1IQE
![screenshot](http://i.imgur.com/sugduZd.png)


### Visualizing a decision tree
1.  Create a decision tree with scikit-learn's DecisionTreeClassifier
2.  Generate json from the tree's structure
3.  (Temporary) Use a webserver to serve the SVG.  ```python -m SimpleHTTPServer```
4.  (Temporary) Visit localhost:8000/tree.html

From sample_tree.py
```python
from sklearn.tree import DecisionTreeClassifier
import dummy_data
from convert_tree_to_json import ConvertTreeToJSON

data, labels = dummy_data.generate(20*1000, ['Age', 'Weight', 'Hair Color', 'Birth City', 'Current City'])

# Create a decision tree - http://scikit-learn.org/stable/modules/tree.html#classification
dt = DecisionTreeClassifier()
dt.fit(data[0], data[1])

# Generate JSON that represents the tree's structure
json_generator = ConvertTreeToJSON(dt, labels)
json = json_generator.convert()

# Save the json to a file
text_file = open("data.json", "w")
text_file.write(json)
text_file.close()
```

