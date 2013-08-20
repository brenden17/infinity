from __future__ import print_function

from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import numpy as np

categories = [
        'alt.atheism',
        'comp.graphics',
        'sci.space',
        ]
dataset = fetch_20newsgroups(subset='all', categories=categories,
                                shuffle=True, random_state=42)

#print(len(dataset.data))
labels = dataset.target
true_k = np.unique(labels).shape[0]

vectorizer = TfidfVectorizer(max_df=0.5)
X = vectorizer.fit_transform(dataset.data)

lsa = TruncatedSVD(3)
X = lsa.fit_transform(X)
X = Normalizer(copy=False).fit_transform(X)

km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)

km.fit(X)
#print(km.labels_)

print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
print("Adjusted Rand-Index: %.3f"
              % metrics.adjusted_rand_score(labels, km.labels_))
print("Silhouette Coefficient: %0.3f"
              % metrics.silhouette_score(X, labels, sample_size=1000))
