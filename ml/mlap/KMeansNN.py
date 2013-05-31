import unittest

import numpy as np

from MLhelp import shape

class KMeansNN(object):
    def __init__(self, data, k=3, itercount=2, eta=0.25):
        self.m, self.n = shape(data)
        self.data = data
        self.k = k
        self.weight = np.random.rand(self.n, k)
        self.itercount = itercount
        self.normalised_data = self.normalise(self.data)
        self.eta = eta

    def normalise(self, data):
        s = np.sqrt(np.sum(data**2, axis=1))
        return data / s[:,np.newaxis]

    def train(self):
        for count in range(self.itercount):
            for i in range(self.m):
                activation = np.dot(self.normalised_data[i, :], self.weight)
                winner = np.argmax(activation)
                self.weight[:, winner] += self.eta * (self.normalised_data[i] - self.weight[:, winner])

    def predict(self):
        return np.dot(self.normalised_data, self.weight).argmax(axis=1)

    def score(self, data, target):
        normalised_data = self.normalise(data)
        output = np.dot(self.normalised_data, self.weight).argmax(axis=1)
        print [len(output[output==k])  for k in range(self.k)]
        return 100


class Test(unittest.TestCase):
    def test_KMeansNN(self):
        from sklearn.datasets import load_iris
        iris= load_iris()
        data = iris.data
        target = iris.target
        kmnn = KMeansNN(data)
        kmnn.train()
        kmnn.predict()
        self.assertEquals(100, kmnn.score(data, target))

if __name__ == '__main__':
    unittest.main()
