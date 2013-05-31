import unittest

import numpy as np

from MLhelp import shape, distance,  get_randomseed, distance

class KMean(object):
    centroid = None
    def __init__(self):
        pass

    @classmethod
    def train(cls, data, target, k=3, itercount=60, score=True):
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
        while not np.array_equal(old_centroid, cls.centroid) and count<itercount:
            old_centroid = cls.centroid.copy()
            count = count + 1

            for c in range(k):
                scoretable[:, c] = distance(cdata[:, :-1], cls.centroid[c, :])

            cdata[:, -1] = scoretable.argmin(axis=1)

            for c in range(k):
                cls.centroid[c, :] = \
                        cdata[np.where(cdata[:,-1]==c)].mean(axis=0)[:-1]

        #print cls.centroid
        return None if not score else float(np.sum(cdata[:, -1]==target)) / float(m) * 100

class Test(unittest.TestCase):
    def test_kmean(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        target = iris.target
        self.assertEquals(1, KMean.train(data,target, k=3))

if __name__ == '__main__':
    unittest.main ()
