import numpy as np

sample = np.matrix('-20,-8;-10,-1;0,0;10,1;20,8')
print sample
print np.cov(sample.T)
