from numpy import random, argsort, sqrt
from pylab import plot, show

def distance(x, D):
    return sqrt(((D-x)**2).sum(axis=0))
    

def knn_search(x, D, K):
    ndata = D.shape[1]
    K = K if K < ndata else ndata
    sqd = distance(x, D)
    idx = argsort(sqd)
    return idx[:K]

data = random.rand(2, 200)
x = random.rand(2, 1)
n = knn_search(x, data, 10)

plot(data[0,:], data[1,:], 'ob', x[0,0], x[1,0], 'or')
plot(data[0,n], data[1,n], 'o', markerfacecolor='None', markersize=15,
markeredgewidth=1)
show()
