import random
from operator import itemgetter, mul
import numpy as np
from scipy.misc import comb
from scipy.stats import norm
import matplotlib.pylab as plt

def maximumlikelihoodwithballs(totalball=20, wball=4, bball=2):
    results = []
    for wcount in range(wball, totalball-bball+1):
        n = np.array([wcount, totalball-wcount, totalball])
        k = np.array([wball, bball, wball+bball])
        result = comb(n, k)
        results.append((wcount, totalball-wcount, result[0] * result[1] / result[2]))
    print sorted(results, key=itemgetter(2), reverse=True)

def maximumlikelihoodwithnorm():
    results = []
    n = np.array([0, 1, 2, 3])
    for m, k in ((1,2), (2,1), (1,1)):
        result = norm(loc=m, scale=k).pdf(n)
        results.append((m, k, reduce(mul, result)))
    print sorted(results, key=itemgetter(2), reverse=True)

if __name__ == '__main__':
   #maximumlikelihoodwithballs(20, 4, 2)
    maximumlikelihoodwithnorm()
