from cStringIO import StringIO
import scipy as sp
import numpy as np
import pandas as pd
import pylab as pl
from common import loadzipdata

def processdata(rawdata, delimiter='\t'):
    data = np.genfromtxt(StringIO(rawdata), delimiter)
    data = data[data[:, 1]!=-1]
    return data[:, 0], data[:,1]

def get_data_by_pd(rawdata):
    df = pd.read_csv(StringIO(rawdata), header=None, delimiter='\t')
    df.columns = ['a', 'b']
    df = df.dropna()
    return df

def resolve():
    df = loadzipdata('01', 'web_traffic.tsv', get_data_by_pd)
    x = df['a']
    y = df['b']
    polyf = np.poly1d(np.polyfit(x, y, 10))
    df['c'] = polyf(x)
    df['b'].plot(style=['ro-'])
    df['c'].plot(style=['bs-'])
    print 'error rate {:,}'.format(np.sum((df['b'] - df['c'])**2))

    sampling_factor = 15
    sampling_df = df.ix[::sampling_factor]
    x = sampling_df['a']
    y = sampling_df['b']
    polyf = np.poly1d(np.polyfit(x, y, 10))
    sampling_df['c'] = polyf(x)
    sampling_df['b'].plot(style=['go-'])
    sampling_df['c'].plot(style=['ys-'])
    print 'error rate {:,}'.format(np.sum((sampling_df['b'] - sampling_df['c'])**2))

    pl.show()



if __name__ == '__main__':
    resolve()
