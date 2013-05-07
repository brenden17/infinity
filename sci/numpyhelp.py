from operator import mul

import numpy as np

from scipy.stats import norm

from sklearn.datasets import load_iris

import pylab as plt

def pick(ar, condition):
    condtioned_ar = np.where(ar>condition, True, False)
    return np.extract(condtioned_ar, ar)

def test_pick():
    ar = np.array([[1,2,3,4],[3,4,5,6]])
    print pick(ar, 3)

def creategaussian(ar, plot=True):
    m, mu = norm.fit(ar)
    gaussian = norm(m, mu)
    if plot:
        s = np.unique(ar)
        y = gaussian.pdf(s)
        plt.plot(s, y)
    return gaussian

def test_gaussianNB(plot=True):
    iris = load_iris()
    m, f = iris.data.shape
    x = np.array([0.7, 1.2, 4, 4.2])
    FEATURES = range(f)
    CATEGORIES = ['SETOSA', 'VERSICOLOR', 'VIRGINCA']
    GROUP = ((0, 50), (50, 100), (100, 150))

    gaussians = [[creategaussian(iris.data[s:e, f]) for f in FEATURES] for (s,e) in GROUP]

    result = [[gaussians[c][f].pdf(x[f]) for f in FEATURES] for c in range(len(CATEGORIES))]
    print CATEGORIES[np.argmax(np.array([reduce(mul, c) for c in result]))]

    plt.show()

if __name__ == '__main__':
    test_gaussianNB()

