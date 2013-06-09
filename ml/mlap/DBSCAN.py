'''
http://en.wikipedia.org/wiki/DBSCAN
'''
import unittest

import numpy as np

from MLhelp import shape, distance

class DBSCAN(object):
    MARK = 0
    GROUP = 0
    MARKED = 1
    NOISE = -1
    def __init__(self, data, eps, minpts):
        self.m, self.n = shape(data)
        self.data = data
        self.markeddata = np.hstack((data, np.zeros((self.m, 2))))
        self.eps = eps
        self.minpts = minpts

    def do(self):
        DBSCAN.MARK = self.n
        DBSCAN.GROUP = self.n + 1
        C = 0

        for i in range(self.m):
            if self.markeddata[i, DBSCAN.MARK] == DBSCAN.MARKED:
                continue
            self.markeddata[i, DBSCAN.MARK] = DBSCAN.MARKED
            neighborpts = self.regionquery(self.data[i])

            if len(neighborpts) < self.minpts:
                self.markeddata[i, DBSCAN.GROUP] = DBSCAN.NOISE
            else:
                C = C + 1
                self.expandcluster(i, neighborpts, C)

        print len(self.markeddata[:, DBSCAN.GROUP]==-1)
        print '%d groups - %f, %d' % (C, self.eps, self.minpts)
        return C


    def regionquery(self, item):
        indexes = np.where(distance(self.data, item)<self.eps)
        return indexes[0]

    def expandcluster(self, dataid, neighborpts, C):
        self.markeddata[dataid, DBSCAN.GROUP] = C

        for nid in neighborpts:
            if self.markeddata[nid, DBSCAN.MARK] != DBSCAN.MARKED:
                self.markeddata[nid, DBSCAN.MARK] = DBSCAN.MARKED
                newneighborpts = self.regionquery(self.data[nid])

                if len(newneighborpts) >= self.minpts:
                    #neighborpts = np.concatenate((neighborpts, newneighborpts))
                    self.expandcluster(nid, newneighborpts, C)

            if self.markeddata[nid, DBSCAN.GROUP] == 0:
                self.markeddata[nid, DBSCAN.GROUP] = C

class Test(unittest.TestCase):
    def test_iris(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        params = [
                    {'eps':0.43, 'minpts':5},
                    {'eps':0.43, 'minpts':9},
                    {'eps':0.42, 'minpts':5},
                    {'eps':0.42, 'minpts':9},
                    {'eps':0.42, 'minpts':10},
                    {'eps':0.41, 'minpts':6},
                    {'eps':0.41, 'minpts':8},
                    ]
        #for p in params:
        #    dbscan = DBSCAN(data,**p)
        #    dbscan.do()

        #dbscan = DBSCAN(data, eps=0.54, minpts=12)
        #dbscan.do()
        dbscan = DBSCAN(data, eps=0.42, minpts=4)
        dbscan.do()
        print dbscan.markeddata
        #print dbscan.markeddata[:, DBSCAN.GROUP]==1

        '''
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import axes3d
        import numpy as np
        fig = plt.figure(figsize=(10, 7))
        ax = fig.gca(projection='3d')
        ax.scatter(dbscan.markeddata[:,0],
                    dbscan.markeddata[:,1],
                    dbscan.markeddata[:,2],
                    c=dbscan.markeddata[:,5].astype(np.float))
        plt.show()
        '''

if __name__ == '__main__': 
    unittest.main()
