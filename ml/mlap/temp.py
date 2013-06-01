import unittest

import numpy as np

class Name(object):
    def __init__(self):
        pass

    @classmethod
    def call(cls):
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
