import unittest

import numpy as np

from MLhelp import shape, distance,  get_randomseed

class KMean(object):
    def __init__(self):
        pass

    @classmethod
    def predict(cls, data, target, k=3, itercount=60):
        m, n = shape(data)
        category = np.zeros((m, 1))
        centroid = get_randomseed(data, (k, n))
        print 'start-------------------------'
        print 'init centroid================='
        print centroid

        '''
        u = m / k
        d = [(u*i, u*(i+1), i) for i in range(k)]
        for s, e, i in d:
            category[s:e] = i
        '''
        cdata = np.hstack((data, category))

        score = np.zeros((m, k))
        old_centroid = None

        count = 0
        while not np.array_equal(old_centroid,centroid) and count<itercount:
            old_centroid = centroid.copy()
            count = count + 1

            for c in range(k):
                score[:, c] = np.sqrt(np.power(cdata[:, :-1] - centroid[c, :], 2).sum(axis=1))
            #print score
            #print score.argmin(axis=1)
            cdata[:, -1] = score.argmin(axis=1)
            #print '++++++++++++++++++++++++++++++++'
            #print cdata
            #print '++++++++++++++++++++++++++++++++'

            for c in range(k):
                centroid[c, :] =\
                        cdata[np.where(cdata[:,-1]==c)].mean(axis=0)[:-1]
            print 'count %d========================'% count
            print centroid
        print 'result==============================================='
        #print centroid
        print np.sum(cdata[:, -1] == target)
#        cls.score(cdata, target)
#    def score(cls, cdata, target):
        print float(np.sum(cdata[:, -1]==target)) / float(cdata.shape[0]) * 100
        return float(np.sum(cdata[:, -1]==target)) / float(cdata.shape[0]) * 100

class Test(unittest.TestCase):
    def test_kmean(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        '''
        data = np.array([[1,10],
                            [1,11],
                            [1,13],
                            [2,10],
                            [2,11],
                            [2,14],
                            [10,1],
                            [10,2],
                            [10,3],
                            [11,1],
                            [11,2],
                            [11,2],
                            ])
        '''
        target = iris.target
        #d = np.array([3.2,  1.4,  5.4,  1.3])
        self.assertEquals(1, KMean.predict(data,target, k=3))

if __name__ == '__main__':
    unittest.main ()
