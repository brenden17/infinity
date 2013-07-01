'''
http://scikit-learn.org/stable/auto_examples/cluster/plot_cluster_iris.html
'''
import numpy as np
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D

from sklearn.cluster import KMeans
from sklearn import datasets

np.random.seed(5)

centers = [[1,1], [-1,-1], [1,-1]]
iris = datasets.load_iris()
X = iris.data
y = iris.target

estimators = { 'k3' : KMeans(n_clusters=3),
                'k8' : KMeans(n_clusters=8),
                'ki' : KMeans(n_clusters=3, n_init=1, init='random')}

fignum = 1
for name, est in estimators.iteritems():
    fig = pl.figure(fignum, figsize=(4, 3))
    pl.clf()
    ax = Axes3D(fig, rect=[0,0,.95,1], elev=48, azim=134)

    pl.cla()
    est.fit(X)
    labels = est.labels_

    ax.scatter(X[:,3], X[:,0], X[:,2], c=labels.astype(np.float))

    ax.w_xaxis.set_ticklabels([])
    ax.w_yaxis.set_ticklabels([])
    ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel('Patal')
    ax.set_ylabel('Sepal')
    ax.set_zlabel('Petal')
    fignum = fignum + 1


'''
flg = pl.figure(fignum, figsize=(4,3))
ax.scatter(X[:,3], X[:,0], X[:,2], c=labels.astype(np.float))
pl.clf()

for name, label in [('Setosa', 0),
                    ('Versicolour', 1),
                    ('Virginica', 2)]:
    ax.text3D(X[y == label, 3].mean(),
              X[y == label, 0].mean() + 1.5,
              X[y == label, 2].mean(), name,
              horizontalalignment='center',
              bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))
# Reorder the labels to have colors matching the cluster results
y = np.choose(y, [1, 2, 0]).astype(np.float)
ax.scatter(X[:, 3], X[:, 0], X[:, 2], c=y)

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])
ax.set_xlabel('Petal width')
ax.set_ylabel('Sepal length')
ax.set_zlabel('Petal length')
'''
pl.show()
