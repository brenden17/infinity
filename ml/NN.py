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

def softmax(ar):
    normalise = np.sum(np.exp(ar), axis=1) * np.ones((1, shape(ar)[0]))
    return np.transpose(np.transpose(np.exp(ar))/normalise)

def normalise(ar):
    mean_ar = ar - ar.mean(axis=0)
    return mean_ar/ar.std(axis=0)

class Perception(object):
    """Perception"""
    def __init__(self, data, target, itercount=20, theta=0.25):
        self.dm, self.dn = shape(data)
        self.tm, self.tn = shape(target)
        assert self.dm == self.tm
        self.weight = np.random.rand(self.dn+1, self.tn)
        self.data = np.hstack((data, -np.ones((self.dm, 1))))
        #self.target = target.reshape(self.tm, 1)
        self.target = target
        self.itercount = itercount
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

            np.random.shuffle(change)
            self.data = self.data[change, :]
            self.target = self.target[change, :]

    def predict(self, test_data, func=threshhold):
        data = np.hstack((test_data, -np.ones(1)))
        return self._fwd(data)

def convert_target(target):
    m, n = shape(target)
    t = np.zeros((m, 3))
    t[np.where(target==0), 0] = 1
    t[np.where(target==1), 1] = 1
    t[np.where(target==2), 2] = 1
    print shape(t)
    return t

class MLP(object):
    """Multi Layer Perception"""
    def __init__(self, data, target, hidden_node=2, itercount=5, theta=0.45, outfunc=softmax):
        self.dm, self.dn = shape(data)
        self.tm, self.tn = shape(target)
        self.data = np.hstack((data, -np.ones((self.dm, 1))))
        self.target = target
        self.itercount = itercount
        self.theta = theta
        self.outfunc = outfunc

        self.weight1 = np.random.rand(self.dn+1, hidden_node)
        self.weight2 = np.random.rand(hidden_node+1, self.tn)

    def fwd(self, data):
        hidden_output = np.dot(data, self.weight1)
        #print hidden_output
        tmp_output = sigmod(hidden_output)
        self.hidden_output = np.hstack((tmp_output, -np.ones((shape(tmp_output)[0], 1))))
        output = np.dot(self.hidden_output, self.weight2)
        return self.outfunc(output)

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

            np.random.shuffle(change)
            self.data = self.data[change, :]
            self.target = self.target[change, :]

    def predict(self, test_input):
        data = np.hstack((test_input, -np.ones((shape(test_input)[0], 1))))
        output = threshhold(data):
        return output


class Test(unittest.TestCase):
    def a_test_perception1(self):
        print '-----test_perception1------'
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([0, 1, 1, 1])
        target = target[:, np.newaxis]
        pcn = Perception(data, target)
        pcn.train()
        self.assertEquals([0], pcn.predict(np.array([-1, -1])))

    def a_test_perception2(self):
        print '-----test_perception2------'
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([1, 2, 3, 4])
        target = target[:, np.newaxis]
        pcn = Perception(data, target)
        pcn.train()
        self.assertEquals([1], pcn.predict(np.array([-1, -1])))

    def a_test_mlp1(self):
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([1, 0, 0, 1])
        target = target[:, np.newaxis]
        mlp = MLP(data, target, itercount=100, outfunc=sigmod)
        mlp.train()
        print '======================'
        self.assertEquals([1], mlp.predict(np.array([[-1, -1]])))

    def a_test_mlp2(self):
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([0, 1, 1, 1])
        target = target[:, np.newaxis]
        mlp = MLP(data, target, itercount=1000, outfunc=sigmod)
        mlp.train()
        print '======================'
        self.assertEquals([1], mlp.predict(np.array([[-1, -1]])))

    def test_iris(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        normalise_data = normalise(data)
        target = convert_target(iris.target)
        print 'taget======================'
        mlp = MLP(normalise_data, target, itercount=1000)
        mlp.train()
        print mlp.predict(np.array([[5,5,5,2]]))
        self.assertEquals([[0, 0, 1]], mlp.predict(np.array([[5,5,5,2]])))

if __name__ == '__main__':
    unittest.main()
