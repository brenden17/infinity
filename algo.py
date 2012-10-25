'''
Created on 2012. 10. 10.

@author: Brenden

'''
te
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
    n = len(l)
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

class BinaryHeap(object):
    def __init__(self):
        self.l = [None]
        self.n = 0
        
    def swim(self, k):
        while k > 1 and self.l[k] < self.l[k/2]:
            self.l[k], self.l[k/2] = self.l[k/2], self.l[k]
            k = k/2
                
    def sink(self, k):
        while k*2 <= self.n:
            j = k * 2
            if j < self.n and self.l[j] > self.l[j+1]:
                j = j + 1
            if self.l[k] < self.l[j]:
                break
            self.l[k], self.l[j] = self.l[j], self.l[k]
            k = j

    def insert(self, item):
        self.l.append(item)
        self.n = len(self.l) - 1
        self.swim(self.n)
        
    def delmax(self):
        m = self.l[1]
        self.l[1], self.l[self.n] = self.l[self.n], self.l[1]
        self.l.pop()
        self.n = len(self.l) - 1
        self.sink(1)
        return m
    
    def get_list(self):
        return self.l[1:]
    
class HeapSort(BinaryHeap):
    def __init__(self, l):
        # override values
        self.l = [None] + l
        self.n = len(self.l) - 1
        self.nl = []
        
    def build(self):
        """step 1 - heap ordered"""
        for i in range(self.n/2, 0, -1):
            self.sink(i)
        
    def sortdown(self):
        """step 2 - """
        while self.n > 0:
            self.l[1], self.l[self.n] = self.l[self.n], self.l[1]
            self.nl.append(self.l.pop())
            
            self.n = len(self.l) - 1
            self.sink(1)
    
    def sort(self):
        """step 1,2"""
        self.build()
        self.sortdown()
        return self.nl

from functools import total_ordering
RED, BLACK = True, False

@total_ordering
class Node(object):
    def __init__(self, key=None, value=None, count=1, color=RED):
        self.key = key
        self.value = value
        self.right = None
        self.left = None
        self.count = count
        self.color = color
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.key == other.key
    
    def __gt__(self, other):
        return self.key > other.key
        
class BinarySearchTree(object):
    def __init__(self):
        self.root = None
        self.depth = 0
        
    def size(self, node):
        return 0 if node == None else node.count
    
    def insert_old(self, parent, node):
        if parent.key > node.key:
            if parent.left:
                self.insert_old(parent.left, node)
            else:
#                print 'made new left node ', node.key
                parent.left = node
        else:
            if parent.right:
                self.insert_old(parent.right, node)
            else:
#                print 'made new right node ', node.key
                parent.right = node
        parent.count = 1 + self.size(parent.left) + self.size(parent.right)
        
    def put_old(self, key, value):
        node = Node(key, value)
        if self.root:
            self.insert_old(self.root, node) 
            self.root.count = 1 + self.size(self.root.left) + self.size(self.root.right)
        else:
            self.root = node
        
    def insert(self, node, key, value):
        if node == None:
            return Node(key, value)
        if node.key > key:
            node.left = self.insert(node.left, key, value)
        else:
            node.right = self.insert(node.right, key, value)
        node.count = 1 + self.size(node.left) + self.size(node.right)
        return node
    
    def put(self, key, value):
        self.root = self.insert(self.root, key, value)
        
    def get(self, key):
        if not self.root:
            return None
        
        node = self.root
        while True:
            if node.key == key:
                return node.value
            elif node.key > key:
                if not node.left:
                    return None
                node = node.left
            else:
                if not node.right:
                    return None
                node = node.right
        return None
    
    def floor(self, key):
        """largest key <= to a given key"""
        
    
    def ceiling(self, key):
        """smallest key >= to a given key"""
        pass
    
    def min(self, node):
        if node == None:
            return None
        while node.left:
            node = node.left
        return node
    
    def max(self, node):
        if node == None:
            return None
        while node.right:
            node = node.right
        return node
    
    # implementation not finished 
    def delete_old(self, key):
        if not self.root:
            return None
        
        node = self.root
        parent = self.root
        while True:
            if node.key == key:
                if parent == node:
                    self.root = None
                return node
            elif node.key > key:
                if not node.left:
                    return None
                node = node.left
            else:
                if not node.right:
                    return None
                node = node.right
        return None
    
    def delete_node(self, node):
        if node.left == None:
            return node.right
        node.left = self.delete_node(node.left)
        node.count = 1 + self.size(node.left) + self.size(node.right)
    
    
    def delete_minnode(self):
        self.root = self.delete_node(self.root)
        
    def _delete(self, node, key):
        if node == None:
            return None
        if node.key > key:
            self._delete(node.left, key)
        elif node.key < key:
            self._delete(node.right, key)
        else:
            if node.right == None:
                return node.left
            if node.left == None:
                return node.right
            
            tnode = node
            node = self.min(tnode)
            node.right = self.delete_node(tnode.right)
            node.left = tnode.left
            
        node.count = 1 + self.size(node.left) + self.size(node.right)
        return node
    
    def delete(self, key):
        self.root = self._delete(self.root, key)
        
    def display(self):
        if not self.root:
            print ''

class RedBlackBST(BinarySearchTree):
    
    def is_red(self, node):
        return node.color == RED if node else False
    
    def rotate_left(self, h):
        if not self.is_red(h.right):
            return None
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = RED
        return x
    
    def rotate_right(self, h):
        if not self.is_red(h.left):
            return None
        x = h.left
        h.left = x.right
        x.color, x.right = h.color, h
        h.color = RED
        return x
    
    def flip_color(self, h):
#        if self.is_red(h) or \
        if not self.is_red(h.left) or \
            not self.is_red(h.right):
            return None
        h.color = RED
        h.left.color = BLACK
        h.right.color = BLACK
        
    def insert(self, node, key, value):
#        print '-' * 20
#        print 'key ', key
        if node == None:
            return Node(key, value)
        if node.key > key:
            node.left = self.insert(node.left, key, value)
        else:
            node.right = self.insert(node.right, key, value)
            
        node.count = 1 + self.size(node.left) + self.size(node.right)
        
        if self.is_red(node.right) and not self.is_red(node.left):
#            print 'rotate_left'
            node = self.rotate_left(node)
        if self.is_red(node.left) and self.is_red(node.left.left):
#            print 'rotate_right' bst.get(3)
            node = self.rotate_right(node)
        if self.is_red(node.right) and self.is_red(node.left):
#            print 'flip_color'
            self.flip_color(node)
        return node
    
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
        
    def test_binary_heap(self):
        bh = BinaryHeap()
        bh.insert(2)
        bh.insert(3)
        bh.insert(4)
        bh.insert(1)
        bh.delmax()
        bh.insert(5)
        self.assertEquals([2,3,4,5], bh.get_list())
    
    def test_heap_sort(self):
        l = [3,2,1,5,6,2]
        hs = HeapSort(l)
        hs.sort()
        self.assertEquals([1,2,2,3,5,6], hs.sort())
    
    def test_eq(self):
        n1 = Node(1, 'A')
        n2 = Node(2, 'B')
        self.assertEquals(True, n1==n1)
        self.assertEquals(False, n2==n1)
        
    def test_binary_search_tree(self):
        l = (3, 'A'), (2, 'B'), (1, 'C'), (4, 'D'), (10, 'E'), (17, 'F')
        bst = BinarySearchTree()
        for e in l:
            key, value = e
            bst.put(key, value)
        self.assertEquals('C', bst.get(1))
        self.assertEquals('A', bst.get(3))
        self.assertEquals(6, bst.root.count)
        self.assertEqual(1, bst.min(bst.root).key)
        bst.delete(3)
        self.assertEquals(5, bst.root.count)        

               
    def test_LLRB(self):
        from string import ascii_uppercase
        from random import shuffle, seed
        l = zip(xrange(1, 27), ascii_uppercase)
        seed(5)
        shuffle(l)
        rbt = RedBlackBST()
        size = 14
#        print l[:size]
        for e in l[:size]:
            key, value = e
            rbt.put(key, value)
        self.assertEquals(size, rbt.root.count)
            
if __name__ == '__main__':
    unittest.main()
