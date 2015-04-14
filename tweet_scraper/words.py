from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pandas as pd
import numpy as np

data = pd.read_csv('tweets.csv')
train, test = train_test_split(data, test_size=0.2, random_state=42)

# generate training data
train_data   = train[:, 0]
train_labels = train[:, 1].tolist()

# Generate test data
test_data   = test[:, 0]
test_labels = test[:, 1].tolist()


text_clf = Pipeline([('vect', CountVectorizer()),
                      ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB()),
])

# Train the classifier
text_clf = text_clf.fit(train_data, train_labels)

# Predictions on the test set
predicted = text_clf.predict(test_data)

# determine the accuracy
print np.mean(predicted == test_labels)