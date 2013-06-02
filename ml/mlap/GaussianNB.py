import unittest
from operator import mul

import numpy as np

from scipy.stats import norm

from MLhelp import pick, shape

import pylab as plt

class GaussianNB(object):
    def __init__(self, data=None, target=None):
        if data and target:
            self.initialise(data, target)

    def initialise(self, data, target):
        self.m, self.n = shape(data)
        self.data = data
        self.group = np.unique(target)
        self.target = target
        self.gaussians = None

    def creategaussian(self, ar):
        m, mu = norm.fit(ar)
        gaussian = norm(m, mu)
        return gaussian

    def train(self, data, target):
        self.initialise(data, target)
        self.gaussians = [[self.creategaussian(self.data[np.where(self.target==gid), f]) for f in range(self.n)] for gid in self.group]

    def predict(self, x):
        result = [[self.gaussians[c][f].pdf(x[f]) for f in range(self.n)] for c in range(len(self.group))]

        return self.group[np.argmax(np.array([reduce(mul, c) for c in result]))]

class Test(unittest.TestCase):
    def test_iris(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        x1 = np.array([0.7, 1.2, 4, 4.2])
        x2 = np.array([5.7,  2.8,  4.1,  1.3])
        gnb = GaussianNB()
        gnb.train(iris.data, iris.target)
        self.assertEquals(2, gnb.predict(x1))
        self.assertEquals(1, gnb.predict(x2))

if __name__ == '__main__':
    unittest.main()
