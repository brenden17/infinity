cimport numpy as np
cimport cython

def mul_v1(arr):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i, j] = i + j

def mul_v2(np.ndarray[np.float64_t, ndim=2] arr):
    cdef int i,j
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            arr[i, j] = i + j

@cython.boundscheck(False)
def mul_v3(np.ndarray[np.float64_t, ndim=2] arr):
    cdef int i,j
    with nogil:
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                arr[i, j] = i + j

