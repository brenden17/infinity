from PIL import Image
import numpy as np
from pylab import *
from scipy.ndimage import filters

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
    im = np.array(Image.open('./dataimg/empire.jpg').convert('L'))
    im2 = filters.gaussian_filter(im, 15)
    imx = np.zeros(im.shape)
    filters.sobel(im, 1, imx)

    imshow(imx)
    gray() #use gray() when you use convert
    show()

def compute_harris_response(im, sigma=3):
    imx = zeros(im.shape)
    filters.gaussian_filter(im, (sigma, sigma), (0, 1), imx)
    imy = zeros(im.shape)
    filters.gaussian_filter(im, (sigma, sigma), (1, 0), imy)

    Wxx = filters.gaussian_filter(imx * imx, sigma)
    Wxy = filters.gaussian_filter(imx * imy, sigma)
    Wyy = filters.gaussian_filter(imy * imy, sigma)

    Wdet = Wxx * Wyy - Wxy ** 2
    Wtr = Wxx + Wyy

    return Wdet / (Wtr * Wtr)

def get_harris_points(harrisim, min_dist=10, threshold=0.1):
    corner_threshold = harrisim.max() *  threshold
    harrisim_t = (harrisim > corner_threshold) * 1

    coords = array(harrisim_t.nonzero()).T

    candidate_values = [harrisim[c[0], c[1]] for c in coords]

    index = argsort(candidate_values)

    allowed_locations = zeros(harrisim.shape)
    allowed_locations[min_dist:-min_dist, min_dist:-min_dist] = 1

    filtered_coords = []
    for i in index:
        if allowed_locations[coords[i, 0], coords[i, 1]] == 1:
            filtered_coords.append(coords[i])
            allowed_locations[(coords[i,0]-min_dist):(coords[i,0]+min_dist),
                (coords[i,1]-min_dist):(coords[i,1]+min_dist)] = 0

    return filtered_coords

def plot_harris_points(image, filtered_coords):
    figure()
    gray()
    plot([p[1] for p in filtered_coords], [p[0] for p in filtered_coords], '*')
    axis('off')
    show()

def main_harris():
    im = np.array(Image.open('./dataimg/empire.jpg').convert('L'))
    hrs = compute_harris_response(im)
    filtered_coords = get_harris_points(hrs, 6)
    plot_harris_points(im, filtered_coords)

if __name__ == '__main__':
   #filtering() 
    main_harris()

