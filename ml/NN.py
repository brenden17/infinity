import unittest

import numpy as np

from MLhelp import shape, threshold, sigmod, softmax, normalise

class Perceptron(object):
    """Perceptron"""
    def __init__(self, data, target, itercount=2120, theta=0.25):
        self.dm, self.dn = shape(data)
        self.tm, self.tn = shape(target)
        assert self.dm == self.tm
        self.weight = np.random.rand(self.dn+1, self.tn)
        self.data = np.hstack((data, -np.ones((self.dm, 1))))
        #self.target = target.reshape(self.tm, 1)
        self.target = target
        self.itercount = itercount
        self.theta = theta

    def _fwd(self, data, func=threshold):
        output = np.dot(data, self.weight)
        return func(output)

    def fwd(self, data=None, func=threshold):
        if data is not None:
            self.dm, self.dn = shape(data)
            self.data = np.hstack((data, -np.ones((self.dm, 1))))
        return self._fwd(self.data)

    def train(self, data=None, target=None):
        if data is not None:
            self.dm, self.dn = shape(data)
            self.data = np.hstack((data, -np.ones((self.dm, 1))))
        if target is not None:
            self.target = target

        change = range(self.dm)

        for n in range(self.itercount):
            error = 0.5 * sum((self.target - self.fwd()) ** 2)
            if n % 200 == 0:
                print '++++++++++++++++++'
                print "Iteration: ", n, "\tError: ", error
            self.weight += self.theta * np.dot(np.transpose(self.data), self.target - self.fwd())

            np.random.shuffle(change)
            self.data = self.data[change, :]
            self.target = self.target[change, :]

    def predict(self, test_data, func=threshold):
        #data = np.hstack((test_data, -np.ones(1)))
        data = np.hstack((test_data, -np.ones((shape(test_data)[0], 1))))
        print self._fwd(data)
        return self._fwd(data)

    def score(self, input_data, target):
        data = np.hstack((input_data, -np.ones((shape(input_data)[0], 1))))
        output = self._fwd(data)
        m = data.shape[0]
        s = np.sum([(output[i]==target[i]).all() for i in range(m)])
        return float(s) / float(m) * 100.0


def convert_target(target):
    m, n = shape(target)
    t = np.zeros((n, 3))
    t[np.where(target==0), 0] = 1
    t[np.where(target==1), 1] = 1
    t[np.where(target==2), 2] = 1
    return t

class MLP(object):
    """Multi Layer Perception"""
    def __init__(self, data,
                       target,
                       hidden_node=5,
                       itercount=1000,
                       theta=0.5,
                       beta=1,
                       momentum=0.2,
                       mode='logistic'):
        self.dm, self.dn = shape(data)
        self.tm, self.tn = shape(target)
        self.data = np.hstack((data, -np.ones((self.dm, 1))))
        self.target = target
        self.itercount = itercount
        self.theta = theta
        self.beta = beta
        self.momentum = momentum
        self.mode = mode

        self.weight1 = (np.random.rand(self.dn+1, hidden_node)-0.5)*2/np.sqrt(self.dn)
        self.weight2 = (np.random.rand(hidden_node+1, self.tn)-0.5)*2/np.sqrt(hidden_node)

    def fwd(self, data):
        hidden_output = np.dot(data, self.weight1)
        tmp_output = sigmod(hidden_output, self.beta)
        self.hidden_output = np.hstack((tmp_output, -np.ones((shape(tmp_output)[0], 1))))
        output = np.dot(self.hidden_output, self.weight2)
        if self.mode == 'linear':
            return output
        elif self.mode == 'logistic':
            return sigmod(output)
        elif self.mode == 'softmax':
            return softmax(output)
        else:
            return None

    def train(self):
        change = range(self.dm)
        updatew1 = np.zeros((shape(self.weight1)))
        updatew2 = np.zeros((shape(self.weight2)))

        for n in range(self.itercount):
            fwd_output = self.fwd(self.data)
            error = 0.5 * sum((self.target - fwd_output) ** 2)
            if n % 200 == 0:
                print '++++++++++++++++++'
                print "Iteration: ", n, "\tError: ", error

            if self.mode == 'linear':
                delta_o = (self.target - fwd_output) / self.dm
            elif self.mode == 'logistic':
                delta_o = (self.target - fwd_output) * fwd_output * (1 - fwd_output)
            elif self.mode == 'softmax':
                delta_o = (self.target - fwd_output) / self.dm
            else:
                delta_o = 0
            delta_h = self.hidden_output * \
                        (1.0 - self.hidden_output) *\
                        (np.dot(delta_o, np.transpose(self.weight2)))


            updaetw1 = self.theta * (np.dot(np.transpose(self.data), delta_h[:,:-1])) + self.momentum * updatew1
            updatew2 = self.theta * (np.dot(np.transpose(self.hidden_output), delta_o)) + self.momentum * updatew2

            self.weight1 = self.weight1 + updatew1
            self.weight2 = self.weight2 + updatew2

            np.random.shuffle(change)
            self.data = self.data[change, :]
            self.target = self.target[change, :]

    def predict(self, test_input):
        data = np.hstack((test_input, -np.ones((shape(test_input)[0], 1))))
        return threshold(self.fwd(data))

    def score(self, input_data, target):
        data = np.hstack((input_data, -np.ones((shape(input_data)[0], 1))))
        output = threshold(self.fwd(data))
        m = data.shape[0]
        s = np.sum([(output[i]==target[i]).all() for i in range(m)])
        return float(s) / float(m) * 100.0

class Test(unittest.TestCase):
    def test_perceptron(self):
        print '-----test_perceptron1------'
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([0, 1, 1, 1])
        target = target[:, np.newaxis]
        pcn = Perceptron(data, target)
        pcn.train()
        pcn.score(data, target)
        self.assertEquals([[0], [0]], pcn.predict(np.array([[-1, -1], [-1, 1]])))

    def a_test_perceptron2(self):
        print '-----test_perceptron2------'
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([1, 2, 3, 4])
        target = target[:, np.newaxis]
        pcn = Perceptron(data, target)
        pcn.train()
        self.assertEquals([1], pcn.predict(np.array([-1, -1])))

    def a_test_mlp1(self):
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([1, 0, 0, 1])
        target = target[:, np.newaxis]
        mlp = MLP(data, target, itercount=100)
        mlp.train()
        print '======================'
        self.assertEquals([1], mlp.predict(np.array([[-1, -1]])))

    def test_mlp2(self):
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([0, 1, 1, 1])
        target = target[:, np.newaxis]
        mlp = MLP(data, target, itercount=1000)
        mlp.train()
        print '======================'
        self.assertEquals([1], mlp.predict(np.array([[-1, -1]])))

    def test_iris(self):
        from sklearn.datasets import load_iris
        iris = load_iris()
        data = iris.data
        normalise_data = normalise(data)
        target = convert_target(iris.target)
        print '======================'
        mlp = MLP(normalise_data, target, hidden_node=17,
                    itercount=2005, theta=0.9, mode='softmax')
        mlp.train()
        self.assertEquals(100, mlp.score(normalise_data, target))
        self.assertEquals([[0, 0, 1]], mlp.predict(np.array([[5,5,5,2]])))

if __name__ == '__main__':
    unittest.main()
