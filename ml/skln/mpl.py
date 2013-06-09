def line_plots():
    import matplotlib as mpl
    from mpl_toolkits.mplot3d import Axes3D
    import numpy as np
    import matplotlib.pyplot as plt

    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    z = np.linspace(-2, 2, 100)
    r = z**2 + 1
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    ax.plot(x, y, z, label='parametric curve')
    ax.legend()
    plt.show()

def scatter_plots():
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    def randrange(n, vmin, vmax):
        return (vmax - vmin) * np.random.rand(n) + vmin

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    n = 100
    for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
        xs = randrange(n, 23, 32)
        ys = randrange(n, 0, 100)
        zs = randrange(n, zl, zh)
        ax.scatter(xs, ys, zs, c=c, marker=m)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()

def scatter_plots():
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt

    def randrange(n, vmin, vmax):
        return (vmax - vmin) * np.random.rand(n) + vmin

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    n = 100
    for c, m, zl, zh in [('r', 'o', -50, -25), ('b', '^', -30, -5)]:
        xs = randrange(n, 23, 32)
        ys = randrange(n, 0, 100)
        zs = randrange(n, zl, zh)
        ax.scatter(xs, ys, zs, c=c, marker=m)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()


def ff():
    import matplotlib.pyplot as plt
    plt.figure(1)
    plt.subplot(211)
    plt.plot([1,2,3])
    plt.subplot(212)
    plt.plot([4,5,6])

    plt.figure(2)
    plt.plot([4,5,6])

    plt.figure(1)
    plt.subplot(212)
    plt.title('easy')
    plt.show()

def wire():
    from mpl_toolkits.mplot3d import axes3d
    import matplotlib.pyplot as plt
    import numpy as np

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x, y, z = axes3d.get_test_data(0.05)
    x = np.linspace(1,10,100)
    y = np.linspace(4,10,100)
    z = np.linspace(8,10,100)
    ax.plot_wireframe(x, y, z, rstride=10, cstride=10)

    plt.show()

def a():
    from mpl_toolkits.mplot3d import axes3d
    import numpy as np
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    x = np.linspace(0, 1, 100)
    y = np.sin(x * 2 * np.pi) /2 + 0.5
    ax.plot(x, y, zs=0, zdir='z', label='zs=0, zdir=z')
    colors = ('r', 'g', 'b', 'k')
    for c in colors:
        x = np.random.sample(20)
        y = np.random.sample(20)
        ax.scatter(x, y, y, zdir='y', c=c)

    ax.legend()
    ax.set_xlim3d(0, 1)
    ax.set_ylim3d(0, 1)
    ax.set_zlim3d(0, 1)

    plt.show()

def iris():
    from mpl_toolkits.mplot3d import axes3d
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris
    iris = load_iris()
    data = iris.data
    target = iris.target
    fig = plt.figure(figsize=(10,7))
    ax = fig.gca(projection='3d')
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], c=target.astype(np.float))

    axismin = data.min(axis=0)
    axismax = data.max(axis=0)

    #ax.w_xaxis.set_ticklabels([axismin[0], axismax[0]])
    #ax.w_yaxis.set_ticklabels([axismin[1], axismax[1]])
    #ax.w_zaxis.set_ticklabels([axismin[2], axismax[2]])
    ax.legend()
    ax.set_xlabel('Patal width')
    ax.set_ylabel('Sepal length')
    ax.set_zlabel('Petal length')
    plt.show()


if __name__ == '__main__':
    #line_plots()
    #scatter_plots()
    #ff()
    #wire()
    #a()
    iris()
