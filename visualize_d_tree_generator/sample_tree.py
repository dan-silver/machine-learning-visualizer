from sklearn.tree import DecisionTreeClassifier
import dummy_data
from convert_tree_to_json import ConvertTreeToJSON

data, labels = dummy_data.generate(20*1000, ['Age', 'Weight', 'Hair Color', 'Birth City', 'Current City'])

# create decision tree
dt = DecisionTreeClassifier()
dt.fit(data[0], data[1])

json_generator = ConvertTreeToJSON(dt, labels)
json = json_generator.convert()

text_file = open("data.json", "w")
text_file.write(json)
text_file.close()