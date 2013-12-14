import numpy as np

def cal_confusion(m):
    return (float(np.trace(m)) / float(np.sum(m))) * 100.0

if __name__ == '__main__':
    m = np.array([[5, 3, 1], [2, 3, 1], [0, 2, 1]])
    print cal_confusion(m)
