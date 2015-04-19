from sklearn.tree import DecisionTreeClassifier
import dummy_data
from convert_tree_to_json import ConvertTreeToJSON

# Generate some data
data, labels = dummy_data.generate(20*1000, ['Age', 'Weight', 'Hair Color', 'Birth City', 'Current City'])

# Create a decision tree - http://scikit-learn.org/stable/modules/tree.html#classification
dt = DecisionTreeClassifier()
dt.fit(data[0], data[1])

# Generate JSON that represents the tree's structure
json = ConvertTreeToJSON(dt, labels).convert()

# Save the json to a file
text_file = open("data.json", "w")
text_file.write(json)
text_file.close()