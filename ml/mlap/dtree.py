from __future__ import division
import unittest
import numpy as np
from MLhelp import shape
from tree import Tree, TreeNode

class DuplicatedChild(Exception):
    pass

class TreeNode(object):
    def __init__(self, feature=None, condition=None, parent=None):
        self.parent = parent
        self.feature = feature
        self.condition = condition
        self.children = []

    def add_child(self, node):
        #if node in self.children:
        #    raise DuplicatedChild('Duplicate child child')
        if node:
            node.parent = self
        self.children.append(node)

    def remove_child(self, node):
        if not node in self.children:
            raise DoesnotExistedChild('Does not existed child')
        node.parent = None
        self.children.remove(node)

    def create_child(self, feature, condition):
        new_node = TreeNode(self, feature, condtion)
        self.add_child(new_node)
        return new_node

    def __repr__(self):
        return "<Node f:%s c:%s>" % (self.feature, self.condition)

class DecisionTree(object):
    def __init__(self, inputdata):
        self.root = TreeNode()
        self.inputdata = inputdata
        self.feature = inputdata[0]
        self.data = inputdata[1:]
        self.m, self.n = shape(inputdata)
        self.restfeature = inputdata[0]
        self.RESULT = self.n - 1

    def entropy(self, p):
        return 0 if p==0 else -p * np.log2(p)

    def sum_entropy(self, data):
        m, n = shape(data)
        uniques = np.unique(data[:, self.RESULT])
        e = 0
        for u in uniques:
            count = len(data[data[:, self.RESULT]==u])
            e += self.entropy(count/m)
        return e

    def count(self, data, feature):
        m, n = shape(data)
        ss = np.unique(data[:, feature])
        uniques = np.unique(data[:, self.RESULT])
        allsum = 0
        for s in ss:
            a = data[ data[:, feature]==s]
            am, an = shape(a)
            partsum = 0
            for u in uniques:
                cm, cn = shape(a[a[:, self.RESULT]==u])
                partsum = partsum - self.entropy(cm/am)
            allsum = allsum - (am/m*partsum)
        return allsum

    def infogain(self, data):
        m, n = shape(data)
        s = self.sum_entropy(data)
        ds = [s-self.count(data,i) for i in range(n-1)]
        maxfeature = np.array(ds).argmax()
        featurevalues = np.unique(data[:, maxfeature])
        return maxfeature, featurevalues

    def create_node(self, data, feature=None, featurevalue=None):
        print '-----------------------------------------------------------'
        print data
        print feature, featurevalue
        print len(np.unique(data[:, self.RESULT]))
        node = TreeNode() if feature==None else TreeNode(self.feature[feature], featurevalue)
        if len(np.unique(data[:, self.RESULT])) == 1:
            print node
            return node
        mf, nfvs = self.infogain(data)
        print self.feature[mf], nfvs
        print node
        for nfv in nfvs:
            child = self.create_node(data[data[:, mf]==nfv], mf, nfv)
            node.add_child(child)
        return node

    def create_tree(self):
        self.root = self.create_node(self.data)

    def display(self):
        from collections import deque
        queue = deque()
        queue.append(self.root)
        while queue:
            node = queue.popleft()
            if not node:
                continue
            print node
            for c in node.children:
                queue.append(c)

class Test(unittest.TestCase):
    def test(self):
        data = np.array([['Deadline','Party','Lazy','Activity'],
                        ['Urgent','Yes','Yes','Party'],
                        ['Urgent','No','Yes','Study'],
                        ['Near','Yes','Yes','Party'],
                        ['None','Yes','No','Party'],
                        ['None','No','Yes','Pub'],
                        ['None','Yes','No','Party'],
                        ['Near','No','No','Study'],
                        ['Near','No','Yes','TV'],
                        ['Near','Yes','Yes','Party'],
                        ['Urgent','No','No','Study']])
        dt = DecisionTree(data)
        dt.create_tree()
        #dt.display()

if __name__ == '__main__':
    unittest.main()
