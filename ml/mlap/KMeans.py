import unittest

import numpy as np

from MLhelp import shape, distance,  get_randomseed, distance

from silhouette import Silhouette as sh

class KMeans(object):
    centroid = None
    assigneddata = None
    k = 0

    def __init__(self):
        pass

    @classmethod
    def train(cls, data, k=3, itercount=60):
        m, n = shape(data)
        category = np.zeros((m, 1))
        cls.centroid = get_randomseed(data, (k, n))
        cls.k = k

        '''
        u = m / k
        d = [(u*i, u*(i+1), i) for i in range(k)]
        for s, e, i in d:
            category[s:e] = i
        '''
        cdata = np.hstack((data, category))

        scoretable = np.zeros((m, k))
        old_centroid = None

        count = 0
        while not np.array_equal(old_centroid, cls.centroid) and\
                 count<itercount:
            old_centroid = cls.centroid.copy()
            count += 1

            for c in range(k):
                scoretable[:, c] = distance(cdata[:, :-1], cls.centroid[c, :])

            cdata[:, -1] = scoretable.argmin(axis=1)

            for c in range(k):
                cls.centroid[c, :] = \
                        cdata[np.where(cdata[:,-1]==c)].mean(axis=0)[:-1]

        cls.assigneddata = cdata

    @classmethod
    def score(cls):
        return sh.score(cls.assigneddata)

    @classmethod
    def assigngroup(data, k=0, centroid=None):
        m, n = shape(data)
        category = np.zeros((m, 1))
        scoretable = np.zeros((m, k))

        if centroid:
            cls.centroid = centroid
        if k:
            cls.k = k

        cdata = np.hstack((data, category))

        for c in range(cls.k):
            scoretable[:, c] = distance(cdata[:, :-1], cls.centroid[c, :])

        cdata[:, -1] = scoretable.argmin(axis=1)
        return cdata

    @classmethod
    def match(cls, data, k=3, itercount=50):
        result = dict()
        for i in range(itercount):
            cls.train(data, k)
            print cls.centroid
            print cls.assigneddata
            score = cls.score()
            print score
            result[score] = cls.centroid
        print sorted(result.items(), reverse=True)
        return sorted(result.items(), reverse=True)[0][1]

class Test(unittest.TestCase):
    def test_kmeans(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        #KMeans.train(data, k=3)
        KMeans.match(data, k=3)
        self.assertEquals(1, KMeans.score())

    def _test_max_kmeans(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        KMeans.match(data, target, 3)
        '''
        print sh.score(KMeans.assigneddata)
        #self.assertEquals(1, KMeans.score(target))
        KMeans.match(data, target, 2)
        print sh.score(KMeans.assigneddata)
        KMhkeans.match(data, target, 4)
        print sh.score(KMeans.assigneddata)
        #KMeans.match(data, target, 15)
        '''

if __name__ == '__main__':
    unittest.main ()
