import unittest

import numpy as np

from MLhelp import shape

class SelfOrganisingMap(object):
    def __init__(self, x, y, data, itercount=2000, size=0.5,
                    eta_bfinal=0.03,eta_nfinal=0.01,sizefinal=0.05):
        self.m, self.n = shape(data)
        self.x, self.y = x, y
        self.xy = x * y
        self.itercount = itercount

        self.size = size
        self.eta_bfinal = eta_bfinal
        self.eta_nfinal = eta_nfinal
        self.sizefinal = sizefinal

        self.gridmap = np.mgrid[0:1:np.complex(0, x), 0:1:np.complex(0, y)]
        self.weight = (np.random.rand(self.n, x*Y) - 0.5) * 2
        self.grid = np.zeros(self.xy, self.xy)

        for i in range(self.xy):
            for j in range(self.xy):
                self.grid[i, j] = np.sqrt((self.gridmap[0, i] - self.gridmap[0, j])**2 + (self.gridmap[1, i] - self.gridmap[1, j])**2)
                self.grid[j, i] = self.grid[i, j]

    def fwd(self, data):
        activation = np.sum((np.transpose(np.tile(data, (self.xy, 1))) -\
                        self.weight)**2, axis=0)
        return np.argmin(activation)


    def train(self):
        for ic in range(self.itercount):
            for i in range(self.n):
                item = self.data[i, :]
                best = self.fwd(item)
                self.weight[:, best] += self.eta_b * (item-self.weigh[:, best])
                neighbour = np.where(self.grid[best, :]<=self.size, 1, 0)
                neighbour[best] = 0
                self.weight += self.eta_n * neighbour *\
                    np.transpose((item - np.transpose(self.weight)))

            self.eta_b = self.eta_binit *\
                    np.power(self.eta_bfinal/self.eta_binit, float(ic)/self.itercount)
            self.eta_n = self.eta_ninit *\
                    np.power(self.eta_nfinal/self.eta_ninit, float(ic)/self.itercount)
            self.size = self.sizeinit *\
                     np.power(self.sizefinal/self.sizeinit, float(ic)/itercount)


    def predict(self):
        return 1

class Test(unittest.TestCase):
    def test_SOM(self):
        from sklearn.datasets import load_iris
        iris= load_iris()
        data = iris.data
        target = iris.target
        som= SelfOrganisingMap()
        som.train(data)
        self.assertEquals(100, som.predict())

if __name__ == '__main__':
    unittest.main()
