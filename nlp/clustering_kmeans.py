"""
http://scikit-learn.org/stable/auto_examples/document_clustering.html
"""

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn import metrics

from sklearn.cluster import KMeans, MiniBatchKMeans

import logging
from optparse import OptionParser
import sys
from time import time

import numpy as np

#logging.basicConfig(level=logging.INFO, format)

op = OptionParser()
op.add_option('--no-minibatch', action='store_false', dest='minibatch', 
                default=True, help='Use ordinary k-means algoriths.')
op.add_option('--no-idf', action='store_false', dest='use_idf', 
                default=True, help='')
op.add_option('--use-hashing', action='store_true', default=False,
                help='')
op.add_option('--n-features', type=int, default=10000,
                help='')

op.print_help()

(opts, args) = op.parse_args()
if len(args) > 0:
    op.error('This script takes no arguments.')
    sys.exit(1)

categories = ['alt.atheism',
                'talk.religion.misc',
                'comp.graphics',
                'sci.space']

print categories

dataset = fetch_20newsgroups(subset='all', categories=categories,
                                shuffle=True, random_state=42)

print len(dataset.data)
print len(dataset.target_names)

labels = dataset.target
true_k = np.unique(labels).shape[0]

t0 = time()
if opts.use_hashing:
    if opts.use_idf:
        hasher = HashingVectorizer(n_features=opts.n_features,
                                    stop_words='english', non_negative=True,
                                    norm=None, binary=False)
        vectorizer = Pipeline((
                                ('hasher', hasher),
                                ('tf_idf', TfidTransformer())
                    ))
    else:
        vectorizer = HashingVectorizer(n_features=opts.n_features,
                                        stop_words='english',
                                        non_negative=False,
                                        norm='l2',
                                        binary=False)

else:
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=opts.n_features,
                                stop_words='english', use_idf=opts.use_idf)

X = vectorizer.fit_transform(dataset.data)

print time() - t0

if opts.minibatch:
    km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                        init_size=1000, batch_size=1000, verbose=1)

else:
    km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,
verbose=1)

km.fit(X)
print "done in %0.3fs" % (time() - t0)
print

print "Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_)
print "Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_)
print "V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_)
print "Adjusted Rand-Index: %.3f" % \
    metrics.adjusted_rand_score(labels, km.labels_)
print "Silhouette Coefficient: %0.3f" % metrics.silhouette_score(
    X, labels, sample_size=1000)
