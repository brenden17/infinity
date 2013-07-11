import operator
from collections import OrderedDict
import unittest
import numpy as np


class DuplicatedChild(Exception):
    pass


class TreeNode(object):
    def __init__(self, item=-1, count=0, link=None, parent=None):
        self.item = item
        self.count = count
        self.link = link
        self.parent = parent
        self.children = []

    def add_child(self, node):
        if node in self.children:
            raise DuplicatedChild('Duplicate child child')
        node.parent = self
        self.children.append(node)

    def remove_child(self, node):
        if not node in self.children:
            raise DoesnotExistedChild('Does not existed child')
        node.parent = None
        self.children.remove(node)

    def create_child(self, item=-1, count=1, link=None, parent=None):
        new_node = TreeNode(item, count, link, parent=self)
        self.add_child(new_node)
        return new_node

    def __str__(self):
        return "<Node i:%d c:%d>" % (self.item, self.count)

    def __repr__(self):
        return "<Node i:%d c:%d>" % (self.item, self.count)

class FPTree(object):
    def __init__(self, data):
        self.data = data
        self.ordered_data = self.order_data()
        self.hashtable = self.create_hashtable()
        self.root = TreeNode()

    def count_item(self):
        s = set()
        for itemset in self.data:
            s.update(itemset)
        d = dict()
        count = 0
        for item in s:
            for itemset in self.data:
                if item in itemset:
                    count += 1
            d[item] = count
            count = 0
        o = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
        return o.keys()

    def create_hashtable(self):
        highfrequent = self.count_item()
        return dict(map(lambda x: (x, None), highfrequent))

    def order_data(self):
        highfrequent = self.count_item()
        return [[i for i in highfrequent if i in d] for d in self.data]

    def train(self):
        for data in self.ordered_data:
            node = self.root
            for item in data:
                node = self.create_node(node, item)

    def create_node(self, node, item):
        for c in node.children:
            if c.item == item:
                c.count += 1
                return c
        link = self.hashtable[item] if self.hashtable[item] else None
        newnode = node.create_child(item, 1, link)
        self.hashtable[item] = newnode
        return newnode

    def generate_frequent_pattern(self, item):
        node = self.hashtable.get(item)
        l = [node]
        while node.link:
            node = node.link
            l.append(node)

        setlist = list()
        for n in l:
            s = set()
            while n.parent:
                n = n.parent
                s.add(n)
            setlist.append(s)
        return reduce(lambda x, y: x&y, setlist) - {self.root} | {node}

    def display(self, node=None, indent=''):
        if not node:
            return None
        print indent + str(node)
        for c in node.children:
            self.display(c, indent + '  ')

class Test(unittest.TestCase):
    def test(self):
        data = [
                (1, 2, 5),
                (2, 4),
                (2, 3),
                (1, 2, 4),
                (1, 3),
                (2, 3),
                (1, 3),
                (1, 2, 3, 5),
                (1, 2, 3),
                ]
        fptree = FPTree(data)
        fptree.train()
        fptree.display(fptree.root)
        fptree.generate_frequent_pattern(3)
        fptree.generate_frequent_pattern(4)
        fptree.generate_frequent_pattern(5)
        #self.assertEquals([[0, 0, 1]], mlp.predict(np.array([[5,5,5,2]])))

if __name__ == '__main__':
    unittest.main()
