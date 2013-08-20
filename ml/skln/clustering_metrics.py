from sklearn.metrics.cluster import homogeneity_score
print(homogeneity_score([0, 0, 1, 1], [1, 1, 0, 0]))
print(homogeneity_score([0, 0, 0, 1, 1, 1], [3, 2, 2, 2, 3, 3]))

from sklearn.metrics.cluster import completeness_score
print(completeness_score([0, 0, 1, 1], [1, 1, 0, 0]))
print(completeness_score([0, 0, 0, 1, 1, 1], [3, 2, 2, 2, 3, 3]))
