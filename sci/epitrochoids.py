'''
http://en.wikipedia.org/wiki/Hypotrochoid
'''
import numpy as np
import pylab as pl

def hypotorochoids(R=5, r=3, d=5):
    t = np.linspace(-4*np.pi, 4*np.pi, 300)
    x = (R-r) * np.cos(t) + d * np.cos((R-r)*t / r)
    y = (R-r) * np.sin(t) - d * np.sin((R-r)*t / r)
    return x, y

def draw():
    x, y = hypotorochoids(R=5, r=3, d=5)
    pl.plot(x, y, 'r')
    pl.axis('equal')
    pl.show()

if __name__ == '__main__':
    draw()
