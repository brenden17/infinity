import unittest

import numpy as np

from scipy.stats import norm


def shape(a):
    #return a.shape if a.ndim>1 else a.shape[0], 1
    if a.ndim>1:
        return a.shape
    else:
        return 1, a.shape[0]

def sum(a, axis=None):
    m, n = shape(a)
    return a.sum() if axis==1 and m==1 else a.sum(axis=axis)

def threshold(ar, value=0.5, highbase=1, lowbase=0):
    return np.where(ar>value, highbase, lowbase)

def sigmod(z, beta=1):
    return 1.0 / (1.0 + np.exp(-beta * z))

def gaussian(ar, mean=0, dev=1):
    return norm.pdf(ar, loc=mean, scale=dev)

def softmax(ar):
    normalise = np.sum(np.exp(ar), axis=1) * np.ones((1, shape(ar)[0]))
    return np.transpose(np.transpose(np.exp(ar))/normalise)

def normalise(ar):
    mean_ar = ar - ar.mean(axis=0)
    return float(mean_ar)/float(ar.std(axis=0))

def distance(a, b, func=None):
    f = func if func is not None else lambda x:x
    return np.sqrt(sum(np.power(f(a) - f(b), 2), axis=1))

def count_item(ar):
    count = np.bincount(ar)
    mark = np.nonzero(count)[0]
    return sorted(zip(mark, count[mark]), key=lambda x:x[1], reverse=True)

def get_most_likely_group(ar):
    return count_item(ar)[0][0]

def get_randomseed(ar, shape):
    m, n = shape
    seed = np.zeros(shape=shape)
    armax, armin = ar.max(axis=0), ar.min(axis=0)
    for i in range(n):
        seed[:, i] = np.random.randint(armin[i], armax[i], size=m)
    return seed

def maxican(x, y):
    return (1-(x**2 + y**2)) / np.exp(-0.5*(x**2 + y**2)/2)

def draw(x, y=None, func=None):
    import pylab as pl
    if y is None and func is not None:
        y = func(x)
    pl.plot(x, y)
    pl.show()

class Test(unittest.TestCase):
    def test_distance(self):
        a = np.array([1, 2])
        b = np.array([2, 1])
        self.assertEquals(np.sqrt(2), distance(a, b))
        self.assertAlmostEquals(0.2117,
                                distance(a, b, func=sigmod), places=3)
        self.assertAlmostEquals(0.26,
                                distance(a, b, func=gaussian), places=1)
        a = np.array([[1, 2], [2,1]])
        b = np.array([[2, 1], [1,2]])
        self.assertTrue(np.array_equal(np.array([np.sqrt(2), np.sqrt(2)]),
                            distance(a,b)))

    def test_count_item(self):
        c = np.array([100, 100, 1, 50,50, 30, 150, 150, 100])
        self.assertEquals([(100, 3), (50, 2), (150, 2), (1, 1), (30, 1)],
                            count_item(c))
        self.assertEquals(100, get_most_likely_group(c))

    def test_get_randomsee(self):
        ar = np.array([[1, 5, 10], [2,6,11], [4, 9, 15]])
        get_randomseed(ar, (2,3))

    def test_draw(self):
        x = np.linspace(-4, 4, 1000)
        y = np.linspace(-4, 4, 1000)
        draw(x, maxican(x, y))

    def _test_draw(self):
        x = np.linspace(-4, 4, 1000)
        draw(x, func=gaussian)

if __name__ == '__main__':
    unittest.main ()
