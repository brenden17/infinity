'''
@author: Brenden
'''
import unittest
    
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
@total_ordering
class Node(object):
    def __init__(self, key=None, value=None, count=1):
        self.key = key
        self.value = value
        self.right = None
        self.left = None
        self.count = count
    
    def __eq__(self, other):
        if other == None:
            return False
        return self.key == other.key
    
    def __gt__(self, other):
        return self.key > other.key
        
class BinarySearchTree(object):
    def __init__(self):
        self.root = None
        
    def size(self, node):
        return 0 if node == None else node.count
    
    def depth(self, node):
        if node == None:
            return 0
        l = 1 + self.depth(node.left)
        r = 1 + self.depth(node.right)
        return l if l > r else r
    
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
            return None, 0
        num = 0
        while node.left:
            node = node.left
            num += 1
        return node, num
    
    def max(self, node):
        if node == None:
            return None, 0
        num = 0
        while node.right:
            node = node.right
            num += 1
        return node, num
    
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
            node, _ = self.min(tnode)
            node.right = self.delete_node(tnode.right)
            node.left = tnode.left
            
        node.count = 1 + self.size(node.left) + self.size(node.right)
        return node
    
    def delete(self, key):
        self.root = self._delete(self.root, key)
    
    def _display(self, node, graph):
        if not node:
            return None
        
        if str(node.key) not in graph:
            graph.add_node(str(node.key), radius=10, stroke=(0, 0, 0, 0.8))
            
        if node.right:
            if str(node.right.key) not in graph:
                graph.add_node(str(node.right.key), radius=10, stroke=(0, 0, 0, 0.8))
            graph.add_edge(graph[str(node.key)], graph[str(node.right.key)], stroke=(0, 0, 0, 0.6))
            self._display(node.right, graph)
        
        if node.left:
            if str(node.left.key) not in graph:
                graph.add_node(str(node.left.key), radius=10, stroke=(0, 0, 0, 0.8))
            graph.add_edge(graph[str(node.key)], graph[str(node.left.key)], stroke=(0, 0, 0, 0.6))
            self._display(node.left, graph)
            
    def display(self):
        from pattern.graph import Graph, export
        graph = Graph()
        self._display(self.root, graph)
        export(graph, 'avl', directed=True, weight=0.6, distance=6)
            
RED, BLACK = True, False
class RBNode(Node):
    def __init__(self, key, value, color=RED):
        Node.__init__(self, key, value)
        self.color = color
        
class RedBlackBST(BinarySearchTree):
    def __init__(self):
        BinarySearchTree.__init__(self)
        
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
            return RBNode(key, value)
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

class AVLTree(BinarySearchTree):
    def __init__(self):
        BinarySearchTree.__init__(self)
    
    def height_size(self, node):
        return 0 if not node else node.height
    
    def rotate_right(self, node):
        x = node.left
        node.left = x.right
        x.right = node
        node.hegiht = self.depth(node)
        return x
    
    def rotate_left(self, node):
        x = node.right
        node.right = x.left
        x.left = node
        node.hegiht = self.depth(node)
        return x

    def insert(self, node, key, value):
#        print '-' * 20
#        print 'key ', key
        if node == None:
            return Node(key, value)
        if node.key > key:
            node.left = self.insert(node.left, key, value)
        else:
            node.right = self.insert(node.right, key, value)
            
        # rebuild
        b = self.depth(node.left) - self.depth(node.right)
        if b == 2:
            leftsize = 0 if not node.left.left else self.depth(node.left.left)
            rightsize = 0 if not node.left.right else self.depth(node.left.right)
            if leftsize - rightsize == 1:
#                print 'rotate_right'
                node = self.rotate_right(node)
            if leftsize - rightsize == -1:
#                print 'rotate_left'
#                print 'rotate_right'
                node.left = self.rotate_left(node.left)
                node = self.rotate_right(node)
        
        if b == -2:
            leftsize = 0 if not node.right.left else self.depth(node.right.left)
            rightsize = 0 if not node.right.right else self.depth(node.right.right)
            if leftsize - rightsize == -1:
#                print 'rotate_left'
                node = self.rotate_left(node)
            if leftsize - rightsize == 1:
#                print 'rotate_right'
#                print 'rotate_left'
                node.right = self.rotate_right(node.right)
                node = self.rotate_left(node)

        node.count = 1 + self.size(node.left) + self.size(node.right)
        node.height = self.depth(node)
        return node
    
class Test(unittest.TestCase):
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
        """
             3
           2   4
         1       10
                   17
        """
        bst = BinarySearchTree()
        for e in l:
            key, value = e
            bst.put(key, value)
        self.assertEquals('C', bst.get(1))
        self.assertEquals('A', bst.get(3))
        self.assertEquals(6, bst.root.count)
        self.assertEqual(1, bst.min(bst.root)[0].key)
        self.assertEqual(2, bst.min(bst.root)[1])
        self.assertEqual(3, bst.max(bst.root)[1])
        self.assertEqual(4, bst.depth(bst.root))
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
    
    def test_AVL(self):
        avl = AVLTree()
        z = [(3, 'H'), (2, 'Y'), (1, 'F'), (4, 'M'), (5, 'J'), (6, 'E'), (7, 'K'), (16, 'C'), (15, 'P') ]
        for e in z:
            key, value = e
            avl.put(key, value)
#        avl.display()  

        
if __name__ == '__main__':
    unittest.main()
