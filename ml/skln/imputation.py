import numpy as np

from sklearn.datasets import load_boston
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import Imputer
from sklearn.cross_validation import cross_val_score


dataset = load_boston()
x, y = dataset.data, dataset.target
n, m = x.shape

print('original data')
estimator = RandomForestRegressor(random_state=0, n_estimators=100)
score = cross_val_score(estimator, x, y)#.mean()
print(score, score.mean())

print('put missing data')
rng = np.random.RandomState(0)
missing_rate = 0.75
n_missing_samples = np.floor(n * missing_rate)
missing_samples = np.hstack((np.zeros(n-n_missing_samples, dtype=np.bool),
                            np.ones(n_missing_samples,dtype=np.bool)))
rng.shuffle(missing_samples)
missing_features = rng.randint(0, m, n_missing_samples)

filtered_x = x[~missing_samples, :]
filtered_y = y[~missing_samples, :]

estimator = RandomForestRegressor(random_state=0, n_estimators=100)
score = cross_val_score(estimator, filtered_x, filtered_y)#.mean()
print(score, score.mean())

print('after imputation')
missing_x = x.copy()
missing_x[np.where(missing_samples)[0], missing_features] = 0
missing_y = y.copy()
estimator = Pipeline([("imputer", Imputer(missing_values=0,
                                        strategy="mean",
                                        axis=0)),
                        ("forest", RandomForestRegressor(random_state=0,
                                        n_estimators=100))])
score = cross_val_score(estimator, missing_x, missing_y)
print(score, score.mean())
