import sklearn
from sklearn import datasets

def generate(n_samples, features):
	n_features = len(features)
	data = sklearn.datasets.make_blobs(n_samples=n_samples, n_features=n_features, centers=10, cluster_std=1.0, center_box=(-10.0, 10.0), shuffle=True, random_state=None)
	return (data, features)