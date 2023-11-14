import imageio
import rawpy
import platform
import cv2_ext
import imutils


def read_raw(img):
    with rawpy.imread(img) as raw:
        thumb = raw.extract_thumb()
    if thumb.format == rawpy.ThumbFormat.JPEG:
        with open('thumb.jpeg', 'wb') as f:
            f.write(thumb.data)
    elif thumb.format == rawpy.ThumbFormat.BITMAP:
        imageio.imsave('thumb.jpeg', thumb.data)
    return cv2_ext.imread('thumb.jpeg')


def slesh():
    sistem = platform.system()
    if 'Win' in sistem:
        sleh = '\\'
    else:
        sleh = '/'
    return sleh


def resize_img(image, size):
    if image.shape[0] > image.shape[1]:
        image = imutils.resize(image, height=size)
    else:
        image = imutils.resize(image, width=size)
    return image
