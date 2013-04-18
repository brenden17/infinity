import numpy as np
from numpy import array, dot, transpose, cov
from numpy.linalg import inv

def lda(x1, x2):
    if not isinstance(x1, np.matrix): 
        x1 = np.matrix(x1).T
    if not isinstance(x2, np.matrix): 
        x2 = np.matrix(x2).T

    s1, mu1 = cov(x1), x1.mean(axis=1)
    s2, mu2 = cov(x2), x2.mean(axis=1)
    s = s1 + s2
    mu = mu1-mu2
    v = inv(s) *  mu
    return v

if __name__ == '__main__':
    """
    x1 = array([(4,2),(2,4),(2,3),(3,6),(4,4)])
    x2 = array([(9,10),(6,8),(9,5),(8,7),(10,8)])
    lda(x1, x2)
    """
    x1 = array([(4,1),(2,4),(2,3),(3,6),(4,4)])
    x2 = array([(9,10),(6,8),(9,5),(8,7),(10,8)])
    lda(x1, x2)
    """
    x1 = array([(1,2),(2,3),(3,3),(4,5),(5,5)])
    x2 = array([(1,0),(2,1),(3,1),(3,2),(5,3),(6,5)])
    lda(x1, x2)
    """
