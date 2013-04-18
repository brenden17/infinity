import numpy as np
from sklearn.decomposition import PCA, RandomizedPCA
import pylab as pl


def process_PCA():
    x = np.array([[-1,-1],[-2,-1],[-3,-2],[1,1],[2,1],[3,2]])

    pca = PCA(n_components=2)
    trans_x = pca.fit_transform(x)

    pl.plot(x[:,0], x[:,1], 'ro')
    pl.plot(trans_x[:,0], trans_x[:,1], 'bo')

    rpca = RandomizedPCA(n_components=2)
    trans_rx = rpca.fit_transform(x)

    pl.plot(trans_rx[:,0], trans_rx[:,1], 'go')
    pl.show()

if __name__ == '__main__':
    process_PCA()

