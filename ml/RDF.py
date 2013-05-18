import unittest

import numpy as np

from MLhelp import shape, normalise

from NN import Perceptron

def convert_target(target):
    m, n = shape(target)
    t = np.zeros((m, 3))
    t[np.where(target==0), 0] = 1
    t[np.where(target==1), 1] = 1
    t[np.where(target==2), 2] = 1
    return t

class RDFNetwork(object):
    '''Radial Basis Function Network'''
    def __init__(self, data, target, count=5, sigma=0, normalise=False):
        self.dm, self.dn = shape(data)
        self.data = data
        self.target = target
        self.count = count
        self.normalise = normalise
        self.hidden = np.zeros((self.dm, self.count+1))

        if sigma == 0:
            d = (data.max(axis=0) - data.min(axis=0)).max()
            self.sigma = d / np.sqrt(2*self.count)
        else:
            self.sigma = sigma

        self.pcn = Perceptron(self.hidden[:, :-1], target, itercount=3000)

        self.weight = np.zeros((self.dn, self.count))

    def train(self, data=None, target=None):
        if data is not None:
            self.dm, self.dn = shpae(data)
            self.data = np.hstack((data, -np.ones((dm, 1))))

        if target is not None:
            self.target = target

        indices = range(self.dm)
        np.random.shuffle(indices)

        for i in range(self.count):
            self.weight[:, i] = self.data[indices[i], :]

        for i in range(self.count):
            self.hidden[:, i] = np.exp(-np.sum(self.data - np.ones((1, self.dn)) * self.weight[:, i]**2, axis=1) / (2*self.sigma**2))

        if self.normalise:
            pass

        self.pcn.train(self.hidden[:, :-1], self.target)

    def fwd(self, data=None):
        if data is not None:
            self.dm, self.dn = shape(data)

        hidden = np.zeros((self.dm, self.count+1))

        for i in range(self.count):
            hidden[:, i] = np.exp(-np.sum(data - np.ones((1, self.dn)) * self.weight[:, i]**2, axis=1) / (2*self.sigma**2))

        if self.normalise:
            pass

        output = self.pcn.fwd(hidden[:, :-1])
        return output

    def score(self, input_data, target):
        output = self.fwd(input_data)
        m = input_data.shape[0]
        s = np.sum([(output[i]==target[i]).all() for i in range(m)])
        return float(s) / float(m) * 100.0

class Test(unittest.TestCase):
    def test_rdf(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = convert_target(iris.target)

        normalise_data = normalise(data)
        rdf = RDFNetwork(normalise_data, target, 1)
        rdf.train()
        print rdf.score(normalise_data, target)
        #self.assertEquals(1,1)

if __name__ == '__main__':
    unittest.main()
