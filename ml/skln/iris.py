from mpl_toolkits.mplot3d import axes3d
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris

def iris_scatter():
    iris = load_iris()
    data = iris.data
    target = iris.target
    fig = plt.figure(figsize=(10,7))
    ax = fig.gca(projection='3d')
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=target.astype(np.float))

    ax.set_title('IRIS')
    ax.set_xlabel('Patal width')
    ax.set_ylabel('Sepal length')
    ax.set_zlabel('Petal length')
    plt.show()

def iris_histogram():
    pass

if __name__ == '__main__':
    iris_scatter()
    iris_histogram()
