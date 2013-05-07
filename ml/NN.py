import unittest
import numpy as np

def shape(a):
    #return a.shape if a.ndim>1 else a.shape[0], 1
    if a.ndim>1:
        return a.shape
    else:
        return a.shape[0], 1

def threshhold(ar, value=0.5, highbase=1, lowbase=0):
    return np.where(ar>value, highbase, lowbase)

def sigmod(z, beta=1):
    return 1.0 / (1.0 + np.exp(-beta * z))

class Perception(object):
    """Perception"""
    def __init__(self, data, target, itercount=20, theta=0.25):
        self.dm, self.dn = shape(data)
        self.tm, self.tn = shape(target)
        assert self.dm == self.tm
        self.weight = np.random.rand(self.dn+1, self.tn)
        self.data = np.hstack((data, -np.ones((self.dm, 1))))
        self.target = target
        self.itercount = itercount if itercount > 0 else self.dm
        self.theta = theta

    def _fwd(self, data, func=threshhold):
        output = np.dot(data, self.weight)
        if self.tn == 1:
            return func(output)
        else:
            return np.argmax(output), np.argmax(self.target)

    def fwd(self, func=threshhold):
        return self._fwd(self.data)

    def train(self):
        change = range(self.dm)
        for i in range(self.itercount):
            error = 0.5 * sum((self.target - self.fwd()) ** 2)
            print "Iteration: ", i, "\tError: ", error
            self.weight += self.theta * np.dot(np.transpose(self.data), self.target - self.fwd())
            print self.weight

            np.random.shuffle(change)
            self.data = self.data[change, :]
            self.target = self.target[change, :]

    def predict(self, test_data, func=threshhold):
        data = np.hstack((test_data, -np.ones(1)))
        return self._fwd(data)

class MLP(object):
    """Multi Layer Perception"""
    def __init__(self, data, target, hidden_layer=2, itercount=2554, theta=0.45):
        self.dm, self.dn = shape(data)
        self.tm, self.tn = shape(target)
        self.data = np.hstack((data, -np.ones((self.dm, 1))))
        self.target = target[:, np.newaxis]
        self.itercount = itercount
        self.theta = theta

        self.weight1 = np.random.rand(self.dn+1, hidden_layer)
        self.weight2 = np.random.rand(hidden_layer+1, self.tn)

    def fwd(self, data, func=sigmod):
        hidden_output = np.dot(data, self.weight1)
        tmp_output = func(hidden_output)
        o = -np.ones((1)) if tmp_output.ndim==1 else -np.ones((tmp_output.shape[0], 1))
        self.hidden_output = np.hstack((tmp_output, o))
        output = np.dot(self.hidden_output, self.weight2)
        return func(output)

    def train(self):
        change = range(self.dm)
        for n in range(self.itercount):
            fwd_output = self.fwd(self.data)
            error = 0.5 * sum((self.target - fwd_output) ** 2)
            print "Iteration: ", n, "\tError: ", error

            delta_o = (self.target - fwd_output) *\
                        fwd_output * (1 - fwd_output)
            delta_h = self.hidden_output * \
                         (1 - self.hidden_output) *\
                         np.dot(delta_o, np.transpose(self.weight2))

            self.weight2 = self.weight2 + \
                            self.theta * \
                            (np.dot(np.transpose(self.hidden_output), delta_o))
            self.weight1 = self.weight1 + \
                            self.theta * \
                            (np.dot(np.transpose(self.data), delta_h[:,:-1]))

            #np.random.shuffle(change)
            #self.data = self.data[change, :]
            #self.target = self.target[change, :]

    def predict(self, test_input):
        if test_input.ndim==1:
            o = -np.ones((1))
        else:
            o = -np.ones((test_input.shape[1], 1))
        data = np.hstack((test_input, o))
        return np.where(self.fwd(data)>0.5, 1, 0)

class Test(unittest.TestCase):
    def a_test_perception1(self):
        print '-----test_perception1------'
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([[0], [1], [1], [1]])
        pcn = Perception(data, target)
        pcn.train()
        self.assertEquals([0], pcn.predict(np.array([-1, -1])))

    def a_test_perception2(self):
        print '-----test_perception2------'
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        pcn = Perception(data, target)
        pcn.train()
        self.assertEquals(np.array([1, 1]), pcn.predict(np.array([2,2])))

    def a_test_perception3(self):
        print '-----test_perception3------'
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([[1], [2], [3], [4]])
        pcn = Perception(data, target)
        pcn.train()
        self.assertEquals(1, pcn.predict(np.array([-1, -1])))

    def test_mlp(self):
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([1, 0, 0, 1])
        mlp = MLP(data, target)
        mlp.train()
        print '======================'
        self.assertEquals([0], mlp.predict(np.array([-1, -1])))

    def test_mlp(self):
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([0, 1, 1, 1])
        mlp = MLP(data, target)
        mlp.train()
        print '======================'
        self.assertEquals([0], mlp.predict(np.array([-1, -1])))

if __name__ == '__main__':
    unittest.main()
