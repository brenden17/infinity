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
    return np.sqrt(np.sum((f(a) - f(b))**2))

class Test(unittest.TestCase):
    def test_distance(self):
        a = np.array([1, 2])
        b = np.array([2, 1])
        self.assertEquals(np.sqrt(2), distance(a, b))
        self.assertAlmostEquals(0.26, distance(a, b, func=gaussian), places=1)
        self.assertAlmostEquals(0.2117, distance(a, b, func=sigmod), places=3)

if __name__ == '__main__':
    unittest.main ()
