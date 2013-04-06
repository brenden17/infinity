from scipy.stats.kde import gaussian_kde
from scipy.stats import  norm
from numpy import linspace, hstack
from pylab import plot, show, hist


sample1 = norm.rvs(loc=-1.0, scale=1, size=300)
sample2 = norm.rvs(loc=2.0, scale=0.5, size=300)
sample = hstack([sample1, sample2])

pdf = gaussian_kde(sample)

x = linspace(-5, 5, 100)
plot(x, pdf(x), 'r')
hist(sample, normed=1, alpha=.3)
show()
