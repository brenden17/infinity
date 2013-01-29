from PIL import Image
from pylab import *

def basic_pil():
    im = Image.open('./dataimg/empire.jpg').convert('L') #convert to grayscale
    im.thumbnail((128, 128))
    im.resize((128, 128))
    im.rotate(45)

def invert():
    im = array(Image.open('./dataimg/empire.jpg').convert('L'))
    im2 = 255 - im
    imshow(im2)

    axis('off')
    axis('equal')
    gray() #use gray() when you use convert

    contour(im, origin='image')
    figure()
    hist(im.flatten(), 128)
    invert_im = Image.fromarray(im2)
    invert_im.save('aa.jpg')
    show()

def histeq(im, nbr_bins=256):
    imhist, bins = histogram(im.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum()
    cdf = 255 * cdf / cdf[-1]
    im3 = interp(im.flatten(), bins[:-1], cdf)
    return im3.reshape(im.shape), cdf

def pca(X):
    num_data, dim, X.shape

    mean_X = X.mean(axis=0)
    X = X - mean_X

    if dim>num_data:
        M = dot(X, X.T)
        e, EV = linalg.eigh(M)
        tmp = dot(X.T, EV).T
        V = tmp[::-1]
        S = sqrt(e)[::-1]
        for i in range(V.shape[1]):
            V[:, i] /= S
    else:
        U, S, V = linalg.svd(X)
        V = V[:num_data]
    return V, S, mean_X

def main1():
    im, cdf = histeq(im)
    imshow(im3)
    show()

def filtering():
    from PIL import Image
    from numpy import array
    from scipy.ndimage import filters

    im = array(Image.open('./dataimg/empire.jpg').convert('L'))
    im2 = filters.gaussian_filter(im, 15)

    imshow(im2)
    gray() #use gray() when you use convert
    show()

if __name__ == '__main__':
   filtering() 




