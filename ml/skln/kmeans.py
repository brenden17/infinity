from sklearn.cluster import KMeans
from sklearn.datasets import load_iris

iris = load_iris()
x = iris.data

km1 = KMeans(init='k-means++', n_clusters=3)
km1.fit(x)
print km1.labels_
print km1.cluster_centers_
print km1.score(x)

km2 = KMeans(init='random', n_clusters=3)
km2.fit(x)
print km2.labels_
print km2.cluster_centers_
print km2.score(x)

