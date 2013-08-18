import numpy as np
import scipy as sp
from scipy import sparse

X = np.random.random((3, 5))
X[X<0.5]=0
print(X)

print(sp.__version__)
x_csr = sparse.csr_matrix(X)
x_csc = sparse.csc_matrix(X)
x_lil = sparse.lil_matrix(X)
print('-------')
print(x_csr)
print('-------')
print(x_csc)
print('-------')
print(x_lil)
print('-------')
