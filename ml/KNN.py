import unittest
import operator

import numpy as np

from MLhelp import gaussian, shape, get_most_likely_group

class KNN(object):
    def __init__(self):
        pass

    @classmethod
    def predict(cls, d, data, target, candi=5, mode='category'):
        indexes = np.argsort(np.sqrt(np.sum((data - d)**2, axis=1)))
        candicates = target[indexes][:candi]

        if mode == 'category':
            return get_most_likely_group(candicates)
        elif mode == 'reg':
            return candicates.mean()
        else:
            return None

class Test(unittest.TestCase):
    def test_knn(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        target = iris.target
        d = np.array([3.2,  1.4,  5.4,  1.3])
        self.assertEquals(1, KNN.predict(d, data, target))

if __name__ == '__main__':
    unittest.main ()
