import numpy as np
import pylab as pl

from sklearn import linear_model, decomposition, datasets
from sklearn.pipeline import Pipeline

logistic = linear_model.LogisticRegression()

pca = decomposition.PCA()
pipe = Pipeline(steps=[('pca', pca), ('logistic', logistic)])

digits = datasets.load_digits()
X = digits.data
Y = digits.target

pca.fit(X)

pl.figure(1, figsize=(4, 3))
pl.clf()
pl.axes([.2, .2, .7, .7])
pl.plot(pca.explained_variance_, linewidth=2)
pl.axis('tight')
pl.xlabel('n_component')
pl.ylabel('explained_variance_')

from sklearn.grid_search import GridSearchCV
n_components = [20, 40, 64]
Cs = np.logspace(-4, 4, 3)

#Parameters of pipelines can be set using ‘__’ separated parameter names:
estimator = GridSearchCV(pipe, dict(pca__n_components=n_components, logistic__C=Cs))

estimator.fit(X, Y)
pl.axvline(estimator.best_estimator_.named_steps['pca'].n_components, linestyle=':', label='n_components chosen')
pl.legend(prop=dict(size=12))
pl.show()
