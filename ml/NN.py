"""
"""

import unittest
import numpy as np

class Perception(object):
    """Perception"""
    def __init__(self, data, target, n=4, theta=0.35):
        m, n = data.shape
        self.weight = np.random.rand(n+1)[:,np.newaxis]
        self.data = np.hstack((data, -np.ones((m, 1))))
        self.target = target[:, np.newaxis]
        self.n = n
        self.theta = theta

    def set_option(self):
        pass

    def fwd(self):
        r = np.dot(self.data, self.weight)
        return np.where(r>0.5, 1, 0)

    def train(self):
        for i in range(self.n):
            self.weight = self.weight - self.theta * np.dot(np.transpose(self.data), self.fwd())
            #self.weight = self.weight - self.theta * np.dot(np.transpose(self.data), self.fwd()) * 0.1 - 0.05

    def test(self, test_data):
        data = np.hstack((test_data, -np.ones(1)))
        return 1 if np.dot(data, self.weight)>0.5 else 0

def sigmod(output, beta=1):
    return 1.0 / (1.0 + np.exp(output))
    #return 1.0 / (1.0 + np.exp(beta * output))

class MLP(object):
    """Multi Layer Perception"""
    def __init__(self, data, target, hidden_layer=2, iter_count=4, theta=0.35):
        data_m = data.shape[0]
        data_n = 1 if data.ndim==1 else data.shape[1]
        target_n = 1 if target.ndim==1 else target.shape[1]
        self.data = np.hstack((data, -np.ones((data_m, 1))))
        self.target = target[:, np.newaxis]
        self.iter_count = iter_count
        self.theta = theta

        self.weight1 = np.random.rand(data_n+1, hidden_layer)
        self.weight2 = np.random.rand(hidden_layer+1, target_n)

    def set_option(self):
        pass
    
    def set_extra(self, m):
        return -np.ones((1)) if m.ndim==1 else -np.ones((m.shape[1], 1))

    def fwd(self, data, func=sigmod):
        hidden_output = np.dot(data, self.weight1)
        tmp_output = func(hidden_output)
        o = -np.ones((1)) if tmp_output.ndim==1 else -np.ones((tmp_output.shape[0], 1))
        self.hidden_output = np.hstack((tmp_output, o))
        output = np.dot(self.hidden_output, self.weight2)
        return func(output)

    def train(self):
        data = self.data
        for n in range(self.iter_count):
            fwd_output = self.fwd(data)

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

    def test(self, test_input):
        print test_input.shape
        print test_input.ndim
        if test_input.ndim==1:
            o = -np.ones((1))
        else:
            o = -np.ones((test_input.shape[1], 1))
            
        data = np.hstack((test_input, o))
        print data
        print '**************'
        return self.fwd(data)

class Test(unittest.TestCase):
    def perception(self):
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([0, 1, 1, 1])
        pcn = Perception(data, target, n=4)
        pcn.train()
        self.assertEquals(1, pcn.test(np.array([-1, -1])))

    def test_mlp(self):
        data = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
        target = np.array([1, 0, 0, 1])
        mlp = MLP(data, target) 
        mlp.train()
        print '======================'
        self.assertEquals(1, mlp.test(np.array([-1, -1])))

if __name__ == '__main__':
    unittest.main()
