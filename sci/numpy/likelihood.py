import numpy as np
from scipy.misc import comb
import random
from operator import itemgetter

def maximumlikelihoodwithballs(totalball=20, wball=4, bball=2):
    results = []
    for wcount in range(wball, totalball-bball+1):
        n = np.array([wcount, totalball-wcount, totalball])
        k = np.array([wball, bball, wball+bball])
        result = comb(n, k)
        results.append((wcount, totalball-wcount, result[0] * result[1] / result[2]))
    print sorted(results, key=itemgetter(2), reverse=True)

if __name__ == '__main__':
   maximumlikelihoodwithballs(20, 4, 2) 
