# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 03:50:29 2013

@author: brenden
"""
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler, Normalizer
from sklearn.cross_validation import cross_val_score,ShuffleSplit


path_to_csv = '/media/sda3/data/study/brenden17.bitbucket.org/source/mlr/ch3/wisc_bc_data.csv'
#data = np.genfromtxt(path_to_csv, dtype=float, delimiter=',', names=True)
rawdata = np.array(pd.read_csv(path_to_csv))
X = rawdata[:, 2:]
y = rawdata[:, 1]

le = LabelEncoder()
y = le.fit(y).transform(y)

print('============== Simple KNN ================')
knn = KNeighborsClassifier(n_neighbors=21)
knn.fit(X, y)
print knn.score(X, y)

print('============== KNN with StardardScale ================')
SX = StandardScaler().fit(X).transform(X)
knn.fit(SX, y)
print knn.score(SX, y)

"""
NX = Normalizer().fit(X).transform(X)
knn.fit(NX, y)
print knn.score(NX, y)
"""

print('============== KNN with cross validate ================')
print cross_val_score(knn, X, y, cv=5)
print cross_val_score(knn, SX, y, cv=5)

cv = ShuffleSplit(X.shape[0], n_iter=5, test_size=0.3, random_state=0)
print cross_val_score(knn, X, y, cv=cv)
print cross_val_score(knn, SX, y, cv=cv)