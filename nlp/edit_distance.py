import numpy as np

def calculate(s, t):
    assert(len(s) == len(t))
    l = len(s) + 1
    m = np.zeros((l, l))
    m[:,0], m[0, :] = xrange(l), xrange(l)
    for i in xrange(1, l):
        for j in xrange(1, l):
            c1 = m[i-1, j] + 1
            c2 = m[i, j-1] + 1
            c3 = m[i-1, j-1] + 2 if s[i-1] != t[j-1] else m[i-1, j-1] 
            m[i, j] = min(c1, c2, c3)


    print m
    print m[l-1][l-1]

if __name__ == '__main__':
    s = 'execution'
    t = 'intention'
    calculate(s, t)
