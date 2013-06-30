import unittest
import numpy as np
from MLhelp import shape

class Bagging(object):
    def __init__(self):
        pass

    @classmethod
    def train(cls, data, model, m=5):
        _, n = shape(data)
        np.random.randint(0, n, (m, n))
        pass

class Test(unittest.TestCase):
    def a_test_iris(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        normalised_data = normalise(data)
        self.assertEquals(100, mlp.score(normalised_data, target))
        self.assertEquals([[0, 0, 1]], mlp.predict(np.array([[5,5,5,2]])))

if __name__ == '__main__':
    unittest.main()
