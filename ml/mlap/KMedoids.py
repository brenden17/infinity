from sys import maxint

import unittest

import numpy as np

from functools import partial

from MLhelp import shape, distance

class KMedoids(object):
    assigneddata = None
    def __init__(self):
        pass

    @classmethod
    def train(cls, data, k=3, itercount=100):
        m, n = shape(data)
        #medoids = data[np.random.choice(m, k)] for numpy1.7
        medoids = data[np.random.randint(0, m, k)]
        old_medoids = None
        min_score = maxint

        scoretable = np.zeros((m, k+1))
        category = np.zeros((m, 1))
        cdata = np.hstack((data, category))
        manhatton = partial(distance, mode='manhatton')
        count = 0

        while not np.array_equal(old_medoids, medoids) and\
                count<itercount:
            count += 1

            for c in range(k):
                scoretable[:, c] = manhatton(data, medoids[c])

            mi = scoretable[:, :-1].argmin(axis=1)
            cdata[:, -1] = mi

            for i in range(m):
                scoretable[i, -1] = scoretable[i, mi[i]]

            score = scoretable[:, -1].sum()

            if min_score > score:
                min_score = score
                medoids = data[np.random.randint(0, m, k)]
                cls.assigneddata = cdata

            '''
            for c in range(k):
                print '--'
                print np.where(scoretable[:,-1]==c)
                print scoretable[np.where(scoretable[:,-1]==c)]
            medoids = data[np.random.randint(0, m, k)]
            '''

        print cdata
        print min_score

    @classmethod
    def score(cls, target):
        m, n = shape(cls.assigneddata)
        return float(np.sum(cls.assigneddata[:, -1]==target)) / float(m) * 100

class Test(unittest.TestCase):
    def test(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        KMedoids.train(data, k=3)
        self.assertEquals(1, KMedoids.score(target))

if __name__ == '__main__':
    unittest.main()
