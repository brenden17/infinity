def f(x):
    return x**3 + 2*x**2

def integrate_v1(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx

def integrate_v2(double a, double b, int N):
    cdef:
        double s
        double dx
        int i
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx

import cython

@cython.locals(a=cython.double, b=cython.double, n=cython.int)
def integrate_v3(a, b, N):
    cdef:
        double s
        double dx
        int i
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx
