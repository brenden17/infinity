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
        self.features = feature
        self.condition = condition
        self.children = []

    def add_child(self, node):
        if node in self.children:
            raise DuplicatedChild('Duplicate child child')
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
        return "<Node f:%s c:%s>" % (self.features, self.condition)

    def __str__(self):
        return "<Node f:%s c:%s>" % (self.features, self.condition)

class DecisionTree(object):
    def __init__(self, inputdata):
        self.root = TreeNode()
        self.inputdata = inputdata
        self.features = inputdata[0]
        self.data = inputdata[1:]
        self.m, self.n = shape(inputdata)
        self.RESULT = self.n - 1

    def entropy(self, p):
        return 0 if p==0 else -p * np.log2(p)

    def total_entropy(self, data):
        m, n = shape(data)
        uniques = np.unique(data[:, self.RESULT])
        e = 0
        for u in uniques:
            count = len(data[data[:, self.RESULT]==u])
            e += self.entropy(count/m)
        return e

    def total_part(self, data, feature):
        m, n = shape(data)
        featureunique = np.unique(data[:, feature])
        resultuniques = np.unique(data[:, self.RESULT])
        allsum = 0
        for fu in featureunique:
            partdata = data[data[:, feature]==fu]
            pdm, _ = shape(partdata)
            partsum = 0
            for u in resultuniques:
                rum, _ = shape(partdata[partdata[:, self.RESULT]==u])
                partsum = partsum - self.entropy(rum/pdm)
            allsum = allsum - (pdm/m*partsum)
        return allsum

    def infogain(self, data):
        m, n = shape(data)
        s = self.total_entropy(data)
        ds = [s-self.total_part(data,i) for i in range(n-1)]
        maxfeature = np.array(ds).argmax()
        featurevalues = np.unique(data[:, maxfeature])
        return maxfeature, featurevalues

    def create_node(self, data, feature=None, featurevalue=None):
        node = TreeNode() if feature==None else TreeNode(self.features[feature], featurevalue)
        if len(np.unique(data[:, self.RESULT])) == 1:
            return node
        mf, nfvs = self.infogain(data)
        for nfv in nfvs:
            child = self.create_node(data[data[:, mf]==nfv], mf, nfv)
            node.add_child(child)
        return node

    def create_tree(self):
        self.root = self.create_node(self.data)

    def prune(self):
        pass

    def display(self, node=None, indent=''):
        if not node:
            return None
        print indent + str(node)
        for c in node.children:
            self.display(c,indent + '  ')
        '''
        from collections import deque
        queue = deque()
        queue.append(node)
        while queue:
            node = queue.popleft()
            if not node:
                continue
            print indent + ' ' + str(node)
            for c in node.children:
                queue.append(c)
        '''

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
        dt.display(dt.root)

if __name__ == '__main__':
    unittest.main()
