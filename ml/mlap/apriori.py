from __future__ import division
from itertools import combinations, permutations
from collections import Iterable
import unittest
import numpy as np


class ExtendTuple(object):
    def __init__(self, data, base='set'):
        self.data = self._convert(data)
        self.base = base
        if base == 'set':
            self._set()

    def exclude(self, item):
        return [d for d in self.data if not d in item]

    def combinations(self):
        s, e = 1, len(self.data)
        l = list()
        for i in range(s, e):
            c = combinations(self.data, i)
            l.extend([e for e in c])
        #print l
        return l

    def generate_association(self):
        return [(e, self.exclude(e)) for e in self.combinations()]

    def _check_get_extendtuple(self, o):
        return o if type(o) == ExtendTuple else ExtendTuple(o, self.base)

    def _convert(self, d):
        if type(d) != tuple:
            try:
                return tuple(d) if isinstance(d, Iterable) else (d,)
            except:
                print 'Converting Error'
                print e
                raise
        return d

    def _set(self):
        self.data = tuple(set(self.data))

    def __add__(self, other):
        other = self._check_get_extendtuple(other)
        assert self.base == other.base
        return ExtendTuple(self.data + other.data, self.base)

    def __contains__(self, item):
        item = self._check_get_extendtuple(item)
        for d in item.data:
            if not d in self.data:
                return False
        return True

    def __len__(self):
        return len(self.data)

    def __eq__(self, other):
        other = self._check_get_extendtuple(other)
        assert self.base == other.base
        return self.data == other.data

    def __str__(self):
        return '%s, %s' % (str(self.data), self.base)

    def __repr__(self):
        return '%s, %s' % (str(self.data), self.base)

class Apriori(object):
    def __init__(self, data, minsup=2, minconf=0.7):
        self.data = data
        self.minsup = minsup
        self.minconf = minconf
        self.candirules = list()
        self.rules = list()

    def train(self):
        candirules = list()
        initc = self.initc()
        l = self.count_c(initc)
        while l:
            c = self.generate_c(l.keys(), initc)
            l = self.count_c(c)
            candirules.extend(l.keys()) if l.keys() else None
        #print candirules
        for rule in candirules:
            m = self.count_item(rule)
            for e in rule.generate_association():
                #print e
                n = self.count_item(e[0])
                self.rules.append(e) if m/n > self.minconf else None
        print self.rules

    def count_item(self, item):
        return sum([1 for d in self.data if item in d])
        '''
        c = 0
        for d in self.data:
            if item in d:
                c += 1
        return c
        '''

    def initc(self):
        s = set()
        for itemset in self.data:
            s.update(itemset.data)
        return [ExtendTuple(i) for i in s]

    def generate_c(self, l, initc):
        productlist = list()
        for litem in l:
            for citem in initc:
                if not citem in litem:
                    item = citem + litem
                    if not self.filtering(l, item):
                        continue
                    if not item in productlist:
                        productlist.append(item)
        return productlist

    def filtering(self, oldl, newitem):
        subset = combinations(newitem.data, len(oldl[0]))
        for ss in subset:
            if not ss in oldl:
                return False
        return True

    def count_c(self, c):
        l = dict()
        count = 0
        for item in c:
            for itemset in self.data:
                if item in itemset:
                    count += 1
            l[item] = count
            count = 0
        return {k:v for k, v in l.iteritems() if v >= self.minsup}

    def predict(self, item):
        return [rule[1] for rule in self.rules if item == rule[0]]


class Test(unittest.TestCase):
    def _test_extendtuple(self):
        a = ExtendTuple((1,3))
        b = ExtendTuple((3,1))
        self.assertEquals(True, a==b)
        a = ExtendTuple((1,3))
        b = ExtendTuple(2)
        self.assertEquals(False, a==b)
        d = a+b
        self.assertEquals(True, a in d)
        c = ExtendTuple({2,3,4})
        c.generate_association()
        c = ExtendTuple((1,2))
        print c.generate_association()
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
        data = map(lambda o: ExtendTuple(o), data)

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
        data = map(lambda o: ExtendTuple(o), data)
        apriori = Apriori(data)
        apriori.train()
        self.assertEquals([], apriori.predict((1,)))
        self.assertEquals([[2]], apriori.predict((4,)))
        self.assertEquals([[1], [2], [1,2]], apriori.predict((5,)))



if __name__ == '__main__':
    unittest.main()
