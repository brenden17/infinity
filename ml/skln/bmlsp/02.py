from cStringIO import StringIO
import pandas as pd
from common import loadzipdata
import pylab as pl
import numpy as np
from sklearn.svm import SVC
from sklearn.cluster import KMeans
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn.decomposition import PCA


def get_data_by_pd(rawdata):
    df = pd.read_csv(StringIO(rawdata), header=None, delimiter='\t')
    return df

def resolve():
    print('===== load data =====')
    df = loadzipdata('02', 'seeds.tsv', get_data_by_pd)
    for i, x in enumerate(np.unique(df.X7)):
        df['X7'][df.X7==x] = i
    data = df[df.columns[0:7]].values
    target = df.X7.values

    print('===== preprocessing : selectk with SVM =====')
    feats = SelectKBest()
    clf = SVC()
    k = [1, 2, 6, 7]
    c = [0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
    degree = [1, 3, 5]
    gamma= [0.0, 0.2, 2.4]
    pipe = Pipeline([('feats', feats), ('svm', clf)])
    estimator = GridSearchCV(pipe, dict(feats__score_func=[f_regression], 
                                        feats__k=k,
                                        svm__degree=degree,
                                        svm__gamma=gamma,
                                        svm__C=c))

    estimator.fit(data, target)
    print(estimator.score(data, target))
    print(estimator.best_estimator_)

    print('===== preprocessing : pca with SVM =====')
    pca = PCA()
    pca.fit(data)
    n_components = [2, 3, 4]

    pipe = Pipeline([('pca', pca), ('svm', clf)])
    estimator = GridSearchCV(pipe, dict(pca__n_components=n_components,
                                        svm__degree=degree,
                                        svm__gamma=gamma,
                                        svm__C=c))

    estimator.fit(data, target)
    print(estimator.score(data, target))
    print(estimator.best_estimator_)


    """

    pipe = Pipeline([('feats', feats), ('svm', clf)])
    estimator = GridSearchCV(pipe, dict(feats__score_func=[f_regression], feats__k=k))

    estimator.fit(data, target)
    print estimator.score(data, target)


    """


    """
    #clf = KMeans(init='k-means++', n_clusters=3)
    clf = KMeans(init='random', n_clusters=3)
    clf.fit(data)
    print clf.score(data)


    from sklearn.naive_bayes import GaussianNB
    gnb = GaussianNB()
    gnb.fit(data, target)
    print gnb.score(data, target)
    """


if __name__ == '__main__':
    resolve()

