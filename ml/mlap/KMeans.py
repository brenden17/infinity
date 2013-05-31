import unittest

import numpy as np

from MLhelp import shape, distance,  get_randomseed, distance

class KMeans(object):
    centroid = None
    assigneddata = None

    def __init__(self):
        pass

    @classmethod
    def train(cls, data, k=3, itercount=60):
        m, n = shape(data)
        category = np.zeros((m, 1))
        cls.centroid = get_randomseed(data, (k, n))

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
            count = count + 1

            for c in range(k):
                scoretable[:, c] = distance(cdata[:, :-1], cls.centroid[c, :])

            cdata[:, -1] = scoretable.argmin(axis=1)

            for c in range(k):
                cls.centroid[c, :] = \
                        cdata[np.where(cdata[:,-1]==c)].mean(axis=0)[:-1]

        cls.assigneddata = cdata

    @classmethod
    def score(cls, target):
        m, n = shape(cls.assigneddata)
        return float(np.sum(cls.assigneddata[:, -1]==target)) / m * 100

    @classmethod
    def match(cls, data, target, k=3, itercount=100):
        result = dict()
        for i in range(itercount):
            cls.train(data, k)
            score = cls.score(target)
            result[score] = cls.centroid
        return sorted(result.items(), reverse=True)[0][1]

class Test(unittest.TestCase):
    def _test_kmeans(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        KMeans.train(data, k=3)
        self.assertEquals(1, KMeans.score(target))

    def test_max_kmeans(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        KMeans.match(data, target)
        #self.assertEquals(1, KMeans.score(target))

if __name__ == '__main__':
    unittest.main ()
