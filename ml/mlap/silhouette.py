from __future__ import division
import unittest
import numpy as np
from sklearn.metrics import silhouette_score

from MLhelp import distance, shape


class Silhouette(object):
    @staticmethod
    def score(ar):
        m, n = shape(ar)
        scoretable = np.zeros((m, 3))
        groupids = set(ar[:, -1])
        #groupids = np.unique(ar[:, -1])
        A, B, S = range(3)

        for i in range(m):
            item = ar[i, :]
            # get a(i)
            subgroup = ar[np.where(ar[:, -1]==item[-1])]
            scoretable[i, A] = np.mean(distance(subgroup[:, :-1], item[:-1]))

            # get b(i)
            scoretable[i, B] = np.min([np.min(distance(ar[np.where(ar[:, -1]==gid)][:, :-1], item[:-1])) for gid in groupids - {item[-1]}])

            # get s(i)
            scoretable[i, S] = (scoretable[i, B] - scoretable[i, A]) /\
                        max(scoretable[i, B], scoretable[i, A])
            #print(scoretable[i, :])

        return scoretable[:, S].mean()


class Test(unittest.TestCase):
    def test_sihouette(self):
        n1 = np.array([[1,2,1], [1,3,1], [7,8,2], [7,9,2], [13,19,3]])
        print(Silhouette.score(n1))
        print(silhouette_score(n1, n1[:,-1]))
        n2 = np.array([[1,2,1], [1,3,2], [7,8,2], [7,9,1], [13,19,3]])
        print(Silhouette.score(n2))
        print(silhouette_score(n2, n2[:,-1]))

if __name__ == '__main__':
    unittest.main()
