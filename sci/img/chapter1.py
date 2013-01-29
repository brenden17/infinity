from PIL import Image
from pylab import *

"""
im = Image.open('empire.jpg').convert('L') #convert to grayscale

im.thumbnail((128, 128))
im.resize((128, 128))
im.rotate(45)
"""

im = array(Image.open('empire.jpg').convert('L'))
im2 = 255 - im
#imshow(im2)

axis('off')
axis('equal')
gray() #use gray() when you use convert

#contour(im, origin='image')
#figure()
#hist(im.flatten(), 128)
#invert_im = Image.fromarray(im2)
#invert_im.save('aa.jpg')

def histeq(im, nbr_bins=256):
    imhist, bins = histogram(im.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum()
    cdf = 255 * cdf / cdf[-1]
    im3 = interp(im.flatten(), bins[:-1], cdf)
    return im3.reshape(im.shape), cdf

im3, cdf = histeq(im)
imshow(im3)
#iii = Image.fromarray(im3)
#imshow(iii)
show()
