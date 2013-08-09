import os
from zipfile import ZipFile
from cStringIO import StringIO
import scipy as sp
import numpy as np
import pandas as pd

def loadzipdata(chapter, datafilename, processfn=None):
    sourcefile = '/media/sda3/data/source/bmlsp/1400OS_{c}_Codes.zip'.format(c=chapter)
    zf = ZipFile(sourcefile)
    for filename in zf.namelist():
        (dirname, extractedfilename) = os.path.split(filename)
        if extractedfilename == datafilename:
            rawdata = zf.read(filename)
            break
    return rawdata if not processfn else processfn(rawdata)

def processdata(rawdata, delimiter='\t'):
    data = np.genfromtxt(StringIO(rawdata), delimiter)
    data = data[data[:, 1]!=-1]
    return data[:, 0], data[:,1]

def get_data_by_pd(rawdata):
    df = pd.read_csv(StringIO(rawdata), header=None, delimiter='\t')#, dtype=object)
    df.columns = ['a', 'b']
    df = df.dropna()
    df.plot()
    return df

if __name__ == '__main__':
    #print loadzipdata('01', 'web_traffic.tsv')
    #print loadzipdata('01', 'web_traffic.tsv', processdata)
    df = loadzipdata('01', 'web_traffic.tsv', get_data_by_pd)
