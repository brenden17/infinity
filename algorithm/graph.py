from Queue import Queue, PriorityQueue
from Queue import Queue

import numpy as np

class Edge(object):
    def __init__(self, startv=None, tov=None, weight=1):
        self.startv = startv
        self.tov = tov
        self.weight = weight

    def __repr__(self):
        return '%d-%d %f' % (self.startv, self.tov, self.weight)

class Vertex(object):
    def __init__(self, i, name='', edge=None):
        self.i = i
        self.name = name
        self.edge = edge

class Graph(object):
    def __init__(self, source=None, bi=False):
        self.verteces = set()
        self.edges = set()
        self.adj = {}
        self.matrix = None
        self.bi = False
        if source:
            self.read_source(source, bi)

    def parse(self, line):
        l = line.split(' ')
        (vs, weight) = (l[0], float(l[1])) if len(l) == 2 else (l[0], None)
        startv, tov = map(int, vs.split('-'))
        return startv, tov, weight

    def add_vertex_edge(self, startv, tov, weight=None, bi=False):
        self.verteces.add(startv)
        self.verteces.add(tov)

        if weight:
            b = Edge(startv, tov, weight)
            self.edges.add(b)
        else:
            b = tov

        if startv in self.adj:
            self.adj[startv].append(b)
        else:
            self.adj[startv] = [b]

        if bi:
            #b = Edge(startv, tov, weight) if weight else startv
            if weight:
                b = Edge(startv, tov, weight)
                self.edges.add(b)
            else:
                b = tov
            if tov in self.adj:
                self.adj[tov].append(b)
            else:
                self.adj[tov] = [b]

    def read_source(self, source, bi=False):
        self.bi = bi
        for line in source:
            startv, tov, weight = self.parse(line)
            self.add_vertex_edge(startv, tov, weight, bi)

    def __repr__(self):
        return ''.join(['%s : %s\n' % (key, item) for key, item in self.adj.items()])

class GraphUtil(object):
    def __init__(self):
        pass

    def convert_matrix(cls, graph):
        vertexcount = len(graph.verteces)

        mat = np.zeros((vertexcount, vertexcount))
        for startv, l in graph.adj.items():
            for b in l:
                (tov, weight) = (b.tov, b.weight) if isinstance(b,Edge) else (b, 1)
                mat[startv][tov] = weight

        graph.matrix = mat
        return graph

    def convert_link(cls, graph):
        row, col = graph.matrix.shape
        graph.adj.clear()

        for startv in xrange(row):
            for tov in xrange(col):
                weight = graph.matrix[startv][tov]
                if weight == 0:
                    continue

                b = Edge(startv, tov, weight) if weight!=1 else tov
                if startv in graph.adj:
                    graph.adj[startv].append(b)
                else:
                    graph.adj[startv] = [b]
                if graph.bi:
                    b = Edge(startv, tov, weight) if weight!=1 else startv
                    if startv in graph.adj:
                        graph.adj[tov].append(b)
                    else:
                        graph.adj[tov] = [b]
        return graph

TRUE, FALSE = 1, 0
class GraphSearcher(object):
    VERTEX, MARK, TO, GROUP = 0, 1, 2, 3
    def __init__(self, graph=None):
        if graph:
            self._init_graph(graph)

    def _init_graph(self, graph):
        self.graph = graph
        vertexcount = len(graph.verteces)
        self.dfstable = np.zeros((vertexcount, 4), dtype=np.int8)
        self.bfstable = np.zeros((vertexcount, 4), dtype=np.int8)
        self.group_count = 0
        self.topological_order = list()

    def set_tables(self, verteces):
        vertexcount = len(verteces)
        self.dfstable = np.zeros((vertexcount, 4), dtype=np.int8)
        self.bfstable = np.zeros((vertexcount, 4), dtype=np.int8)

    def depth(self, startv, graph=None):
        if graph:
            self._init_graph(graph)
        if self.graph:
            return None
        #self._depth(startv)
        for v in self.graph.verteces:
            if not self.dfstable[v][GraphSearcher.MARK]:
                self._depth(v)
                self.group_count += 1
        print self.dfstable
        print self.topological_order

    def _depth(self, v):
        self.dfstable[v][GraphSearcher.MARK] = TRUE
        self.dfstable[v][GraphSearcher.VERTEX] = v
        self.dfstable[v][GraphSearcher.TO] = v
        self.dfstable[v][GraphSearcher.GROUP] = self.group_count
        for w in self.graph.adj[v]:
            if not self.dfstable[w][GraphSearcher.MARK]:
                self._depth(w)
                self.dfstable[w][GraphSearcher.TO] = v
                self.dfstable[w][GraphSearcher.GROUP] = self.group_count

        self.topological_order.append(v)

    def breadth(self, s):
        self._breadth(s)
        for v in self.graph.verteces:
            if not self.bfstable[v][GraphSearcher.MARK]:
                self._breadth(v)
        print self.bfstable

    def _breadth(self, s):
        q = Queue()
        q.put(s)
        self.bfstable[s][GraphSearcher.VERTEX] = s
        self.bfstable[s][GraphSearcher.MARK] = TRUE
        self.bfstable[s][GraphSearcher.TO] = s
        while not q.empty():
            v = q.get()
            for w in self.graph.adj[v]:
                if not self.bfstable[w][GraphSearcher.MARK]:
                    q.put(w)
                    self.bfstable[w][GraphSearcher.VERTEX] = w
                    self.bfstable[w][GraphSearcher.MARK] = TRUE
                    self.bfstable[w][GraphSearcher.TO] = v

    def path(self, tov, option='depth'):
        table = self.dfstable if option=='depth' else self.bfstable
        l = list()
        l.append(tov)
        fromv = table[tov][GraphSearcher.TO]
        while fromv != tov:
            l.append(fromv)
            tov=fromv
            fromv = table[tov][GraphSearcher.TO]
        print '->'.join(map(str, l))
        return l

    def check_cycle(self, v, w):
        return True if v in self.path(w) else False

    def get_groupid(self, v):
        return self.dfstable[v][GraphSearcher.GROUP]

class MST(object):
    def __init__(self, graph):
        self.graph = graph

    def search(self):
        g = Graph()
        pq = PriorityQueue()
        l = list()
        for e in self.graph.edges:
            pq.put(e)
        n_verteces = len(self.graph.verteces)

        while not pq.empty() and len(l)<n_verteces-1:
            e = pq.get()
            print e.weight
            startv, tov = e.startv, e.tov
            gs = GraphSearcher(g)
            gs.depth(startv)
            if not gs.check_cycle(startv,tov):
                g.add_vertex_edge(startv, tov)
                l.append(e)
        print g.adj


def test_convert():
    s = ['0-7 0.16','2-3 0.17','1-7 0.19','0-2 0.26','5-7 0.28','1-3 0.29','1-5 0.32','2-7 0.34','4-5 0.35','1-2 0.36','4-7 0.37','0-4 0.38','6-2 0.40','3-6 0.52','6-0 0.58']

    GU = GraphUtil()
    g = Graph(s)
    print g
    GU.convert_matrix(g)
    ss = g.adj.copy()
    print ss
    GU.convert_link(g)
    print g.adj
    print '----------'
    s1 =['0-7','2-3','1-7','0-2','5-7','1-3','1-5','2-7','4-5','1-2','4-7','0-4','6-2','3-6','6-0',]
    g = Graph(s1)
    print g
    GU.convert_matrix(g)
    ss = g.adj.copy()
    print ss
    GU.convert_link(g)
    print g.adj

def test_bigraph():
    s=['0-5','4-3','0-1','9-12','6-4','5-4','0-2','11-12','9-10','0-6','7-8','9-11','5-3']
    g = Graph(s, bi=True)
    print g
    GS = GraphSearcher(g)
    GS.depth(0)
    GS.path(6)
    GS.breadth(0)
    GS.path(4, option='breadth')
    GS.get_groupid(6)

def test_directgraph():
    s=['5-0','2-4','3-2','1-2','0-1','4-3','3-5','0-2']
    g = Graph(s)
    print g
    GS = GraphSearcher(g)
    GS.depth(0)
    GS.breadth(0)

def test_weightgraph():
    s = ['0-7 0.16','2-3 0.17','1-7 0.19','0-2 0.26','5-7 0.28','1-3 0.29','1-5 0.32','2-7 0.34','4-5 0.35','1-2 0.36','4-7 0.37','0-4 0.38','6-2 0.40','3-6 0.52','6-0 0.58']
    g = Graph(s)
    print g
    mst = MST(g)
    mst.search()


if __name__ == '__main__':
    #test_convert()
    #test_bigraph()
    #test_directgraph()
    test_weightgraph()
