from sklearn.cross_validation import train_test_split, KFold
from sklearn import datasets

def load_by_train_test_split():
    iris = datasets.load_iris()
    print len(iris.data)
    train, test, v_train, v_test = train_test_split(iris.data, iris.target,
test_size=0.3, random_state=10)
    print 'train %d, test %d, v_train %d, test %d' % (len(train), len(test), len(v_train), len(v_test))

def load_by_kfold():
    iris = datasets.load_iris()
    number_split = 2
    kf = KFold(len(iris.data), number_split)
    for train_index, test_index in kf:
        print '---'
        print train_index, test_index

if __name__ == '__main__':
    #load_by_train_test_split()
    load_by_kfold()
