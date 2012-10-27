'''
@author: Brenden
'''
import unittest
import threading

def locknrelease(threading):
    def _locknrelease(func):
        def __locknrelease(*args, **kwargs):
            threading.acquire()
            result = func(*args, **kwargs)
            threading.release()
            return result
        return __locknrelease
    return _locknrelease
            

lock = threading.Lock()

class ThreadSafeStack(object):
    """poor performance"""
    def __init__(self):
        self.l = []
    
    @locknrelease(lock)    
    def is_empty(self):
        return self.l == []
        
    @locknrelease(lock)
    def push(self, item):
        self.l.append(item)
    
    @locknrelease(lock)
    def pop(self):
        return self.l.pop() if self.l else None

class ThreadSafeQueue(object):
    """poor performance"""
    def __init__(self):
        self.l = []
    
    @locknrelease(lock)    
    def is_empty(self):
        return self.l == []
        
    @locknrelease(lock)
    def enqueue(self, item):
        self.l.append(item)
    
    @locknrelease(lock)
    def dequeue(self):
        return self.l.pop(0) if self.l else None

def selection_sort(l):
    n = len(l)
    m = 0
    for i in range(n):
        m = i
        for j in range(i+1, n):
            if l[m] > l[j]:
                m = j
        l[i], l[m] = l[m], l[i]
    return l

def insertion_sort(l):
    n = len(l)#        avl.display()  
    for i in range(1, n):
        for j in range(i, 0, -1):
            if l[j-1] > l[j]:
                l[j-1], l[j] = l[j], l[j-1]
            else:
                break
    return l

import random
def knuth_shuffle(l):
    n = len(l)
    for i in range(1, n):
        r = random.randint(0, i)
        l[i], l[r] = l[r], l[i]
    return l

def merge(ll, rl):
    nl = []
    lli, llm = 0, len(ll)
    rli, rlm = 0, len(rl)
    while(True):
        if llm == lli and rlm == rli:
            break
        if rlm == rli or lli < llm and ll[lli] <= rl[rli]:
            nl.append(ll[lli])
            lli = lli + 1
        else:
            nl.append(rl[rli])
            rli = rli + 1
    return nl    

def merge_sort(l):
    n = len(l)/2
    if n < 1:
        return l
    ll, rl = merge_sort(l[:n]), merge_sort(l[n:])
    return merge(ll, rl)

class ConvexHull(object):
    def __init__(self):
        pass

    def get_angle(self, p1, p2):
        import math
        deltax = abs(p1[0] - p2[0])
        deltay = abs(p1[1] - p2[1])
        
        angle_rad = math.atan2(deltay, deltax)
        return angle_rad * 180.0 / math.pi

    def polar_order(self, p, l): 
        nl = [(point, self.get_angle(p, point))for point in l]
        return [p[0] for p in sorted(nl, key=lambda p: p[1])]
    
    def ccw(self, p1, p2, p3):
        x, y = 0, 1
        v = (p2[x] - p1[x]) * (p3[y] - p3[y]) - (p2[y] - p1[y]) * (p3[x] - p1[x])
        return False if v < 0 else True
        
    def graham_scan(self, p, l):
        vertexs = [p]
        n = len(l)
        for i in range(n):
            if i == 0:
                vertexs.append(l[0])
                continue
            if self.ccw(vertexs[-2], vertexs[-1], l[i]):
                vertexs.append(l[i])
            else:
                vertexs.pop()
                vertexs.append(l[i])
        return vertexs

class Test(unittest.TestCase):
    def test_stack(self):
        s = ThreadSafeStack()
        s.push(1)
        self.assertEquals(False, s.is_empty())

    def test_queue(self):
        q = ThreadSafeQueue()
        q.enqueue(1)
        q.enqueue(2)
        self.assertEquals(False, q.is_empty())
        self.assertEquals(1, q.dequeue())
        self.assertEquals(2, q.dequeue())
        self.assertEquals(None, q.dequeue())

    def test_selection_sort(self):
        l = [7, 10, 5, 3, 8, 4, 2, 9, 6]
        r = [2, 3, 4, 5 ,6 ,7 ,8, 9, 10]
        self.assertEquals(r, selection_sort(l))
 
    def test_insertion_sort(self):
        l = [7, 10, 5, 3, 8, 4, 2, 9, 6]
        r = [2, 3, 4, 5 ,6 ,7 ,8, 9, 10]
        self.assertEquals(r, insertion_sort(l)) 
        
    def test_knuth_shuffle(self):
        l = [7, 10, 5, 3, 8, 4, 2, 9, 6]
        r = [2, 3, 4, 5 ,6 ,7 ,8, 9, 10]
#        self.assertEquals(r, knuth_shuffle(l))

    def test_merge(self):
        ll = [3, 4, 5]
        rl = [1, 4, 6]
        self.assertEquals([1, 3, 4, 4, 5, 6], merge(ll, rl))
    
    def test_merge_sort(self):
        l = [7, 10, 5, 3, 8, 4, 2, 9, 6]
        r = [2, 3, 4, 5 ,6 ,7 ,8, 9, 10]
        self.assertEquals(r, merge_sort(l))
        
    def test_polar_order(self):
        ch = ConvexHull()
        l = [(1, 1), (4, 1), (2, 2), (1, 3), (4, 3), (2, 4), (5, 4)]
        r = [(4, 1), (4, 3), (5, 4), (2, 2), (2, 4), (1, 3)]
        v = [(1, 1), (4, 1), (5, 4), (2, 4), (1, 3)]
        nl = ch.polar_order(l[0], l[1:])
        self.assertEquals(r, nl)
        self.assertEquals(v, ch.graham_scan(l[0], nl))
        
if __name__ == '__main__':
    unittest.main()
