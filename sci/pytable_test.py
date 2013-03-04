import sys
import getopt

import scipy
from tables import openFile, IsDescription
from tables import StringCol, UInt16Col
import numpy as np

filename = 'testpytables2.h5'
dataset1 = [[1,2,3], [4,5,6], [7,8,9]]
dataset2 = [[1,2,3.1], [4,5,6], [7,8,9]]

def save():
    """write"""
    h5file = openFile(filename, mode='w', title='pytable test')
    root = h5file.createGroup(h5file.root, 'datasets', 'data set')
    datasets = h5file.createGroup(root, 'phase1', 'data set')

    d = np.array(dataset1)
    datasets = h5file.createArray(datasets, 'dataset1', d, 'dataset1')
    #d = np.array(dataset2)
    #datasets = h5file.createArray(datasets, 'dataset2', d, 'dataset2')
    h5file.close()

def load():
    """load"""
    h5file = openFile(filename, mode='r')
    dataset1obj = h5file.getNode('/datasets/phase1/', 'dataset1')
    #dataset2obj = h5file.getNode('/datasets/phase1/', 'dataset2')
    print repr(dataset1obj)
    #print repr(dataset2obj)

class NameItem(IsDescription):
    name = StringCol(16)
    year = UInt16Col()
    sex = StringCol(1)

H5_CLASS_FILENAME = 'h5-class.h5'
def save_class():
    h5file = openFile(H5_CLASS_FILENAME, mode='w', title='pytable class test')
    root = h5file.createGroup(h5file.root, 'datasets', 'data class set')
    datasets = h5file.createGroup(root, 'detector', 'info')
    table = h5file.createTable(datasets, 'readout', NameItem, 'name')
    ni = table.row
    for i in xrange(10):
        ni['name'] = 'Brenden Jeon'
        ni['year'] = 1976 + int(i)
        ni['sex'] = 'M'
        ni.append()
    h5file.close()

def load_class():
    h5file = openFile(H5_CLASS_FILENAME)
    nitable = h5file.root.datasets.detector.readout
    names = [x['year'] for x in nitable.iterrows() if x['year']==1976]
    for name in names:
        print name

    names = [x['year'] for x in nitable.where('year==1976')] 
    for name in names:
        print name

    h5file.close()

def get_table_info():
    h5file = openFile(H5_CLASS_FILENAME)
    nitable = h5file.root.datasets.detector.readout

    for name in nitable.colnames:
        print name

def append_class(table, data):
    row = table.row
    for d in data:
        for name in table.colnames:
            row[name] = d[name]
        row.append()
    table.flush()

def usage():
    pass

def main():
    args = sys.argv[1:]
    try:
        opts, args = getopt.getopt(args, 'ht:', ['help', 'test', ])
    except:
        pass

    for opt, val in opts:
        if opt in ('-t', '--test'):
            test_no = int(val)

    if test_no == 1:
        save()
    elif test_no == 2:
        load()
    elif test_no == 3:
        save_class()
    elif test_no == 4:
        load_class()
        get_table_info()
    else:
        pass

if __name__ == '__main__':
    main()
