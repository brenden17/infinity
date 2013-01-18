from pylab import imread, imshow, figure, show, subplot
from numpy import reshape, uint8, flipud
from scipy.cluster.vq import kmeans, vq

img = imread('diff.jpg')

pixel = reshape(img, (img.shape[0] * img.shape[1], 3))

centroids, _ = kmeans(pixel, 2)
print centroids
qnt, _ = vq(pixel, centroids)

centers_ids = reshape(qnt, (img.shape[0], img.shape[1]))
print centers_ids
print centers_ids.shape
clustered = centroids[centers_ids]

figure(1)
subplot(311)
imshow(flipud(img))
subplot(312)
imshow(flipud(clustered))
subplot(313)
imshow(flipud(centers_ids))
show()

