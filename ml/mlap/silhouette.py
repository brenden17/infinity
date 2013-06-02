import unittest

import numpy as np

from MLhelp import distance, shape

class Silhouette(object):
    def __init__(self):
        pass

    @classmethod
    def score(cls, ar):
        m, n = shape(ar)
        scoretable = np.zeros((m, 3))
        groupids = set(ar[:, -1])
        A, B, S = range(3)

        for i in range(m):
            item = ar[i, :]
            # get a(i)
            group = ar[np.where(ar[:, -1]==item[-1])]
            scoretable[i, A] = np.mean(distance(group[:, :-1], item[:-1]))

            # get b(i)
            scoretable[i, B] = np.min([np.min(distance(ar[np.where(ar[:, -1]==gid)][:, :-1], item[:-1])) for gid in groupids - {item[-1]}])

            # get s(i)
            scoretable[i, S] = (scoretable[i, B] - scoretable[i, A]) /\
                        float(max(scoretable[i, B], scoretable[i, A]))

        print (scoretable[:, S].mean()+1) * 50
        return scoretable[:, S].mean()


class Test(unittest.TestCase):
    def test_sihouette(self):
        n = np.array([[1,2,1], [1,3,1], [7,8,2], [7,9,2], [13,19,3]])
        print Silhouette.score(n)
        n = np.array([[1,2,1], [1,3,2], [7,8,2], [7,9,1], [13,19,3]])
        print Silhouette.score(n)

if __name__ == '__main__':
    unittest.main()
