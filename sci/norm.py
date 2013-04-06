from scipy. stats import norm
from numpy import linspace
from pylab import plot, show, hist, figure, title

samples = norm.rvs(loc=0, scale=1, size=150)
param = norm.fit(samples)

x = linspace(-5, 5, 100)
pdf_fitted = norm.pdf(x, loc=param[0], scale=param[1])
pdf = norm.pdf(x)

title('Normal distribution')
plot(x, pdf_fitted, 'r-', x, pdf, 'b-')
hist(samples, normed=1, alpha=.3)
show()

