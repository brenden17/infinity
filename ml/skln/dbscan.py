'''
from : http://jaquesgrobler.github.io/online-sklearn-build/auto_examples/cluster/plot_dbscan.html
'''
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

centers = [[1,1], [-1,-1], [1,-1]]
x, labels_true = make_blobs(n_samples=750, 
                        centers=centers, cluster_std=0.4, random_state=0)


X = StandardScaler().fit_transform(x)

db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples = db.core_sample_indices_
labels = db.labels_

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

import pylab as pl

unique_labels = set(labels)
colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
for k, col in zip(unique_labels, colors):
    if k == -1:
        col = 'k'
        markersize = 6
    class_members = [index[0] for index in np.argwhere(labels==k)]
    class_core_samples = [index for index in core_samples if labels[index] == k]

    for index in class_members:
        x = X[index]
        if index in core_samples and k != 1:
            markersize = 14
        else:
            markersiaze = 6
        pl.plot(X[0], X[1], 'o', markerfacecolor=col, markeredgecolor='k',
                    markersize=markersize)

pl.show()

