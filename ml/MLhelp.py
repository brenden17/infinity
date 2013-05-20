import unittest

import numpy as np

from scipy.stats import norm


def shape(a):
    #return a.shape if a.ndim>1 else a.shape[0], 1
    if a.ndim>1:
        return a.shape
    else:
        return 1, a.shape[0]

def threshold(ar, value=0.5, highbase=1, lowbase=0):
    return np.where(ar>value, highbase, lowbase)

def sigmod(z, beta=1):
    return 1.0 / (1.0 + np.exp(-beta * z))

def gaussian(ar,mean=0, dev=1):
    return norm.pdf(ar, loc=mean, scale=dev)

def softmax(ar):
    normalise = np.sum(np.exp(ar), axis=1) * np.ones((1, shape(ar)[0]))
    return np.transpose(np.transpose(np.exp(ar))/normalise)

def normalise(ar):
    mean_ar = ar - ar.mean(axis=0)
    return mean_ar/ar.std(axis=0)

def distance(a, b, func=None):
    f = func if func is not None else lambda x:x
    return np.sqrt((np.power(f(a) - f(b), 2).sum(axis=1)))

def count_item(ar):
    count = np.bincount(ar)
    mark = np.nonzero(count)[0]
    return sorted(zip(mark, count[mark]), key=lambda x:x[1], reverse=True)

def get_most_likely_group(ar):
    return count_item(ar)[0][0]


def get_randomseed(ar, size):
    m, n = size
    seed = np.zeros(shape=size)
    armax, armin = ar.max(axis=0), ar.min(axis=0)
    for i in range(n):
        seed[:, i] = np.random.randint(armin[i], armax[i], size=m)
    return seed

class Test(unittest.TestCase):
    def test_distance(self):
        a = np.array([1, 2])
        b = np.array([2, 1])
        self.assertEquals(np.sqrt(2), distance(a, b))
        self.assertAlmostEquals(0.26,
                                distance(a, b, func=gaussian), places=1)
        self.assertAlmostEquals(0.2117,
                                distance(a, b, func=sigmod), places=3)
    def test_count_item(self):
        c = np.array([100, 100, 1, 50,50, 30, 150, 150, 100])
        self.assertEquals([(100, 3), (50, 2), (150, 2), (1, 1), (30, 1)], 
                            count_item(c))
        self.assertEquals(100, get_most_likely_group(c))

    def test_get_randomsee(self):
        ar = np.array([[1, 5, 10], [2,6,11], [4, 9, 15]])
        get_randomseed(ar, (2,3))

if __name__ == '__main__':
    unittest.main ()
