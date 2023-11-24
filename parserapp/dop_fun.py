import imageio
import rawpy
import platform
import cv2_ext
import imutils
import time
import os
import psutil

def time_of_function(function):
    def wrapped(*args):
        start_time = time.time()
        res = function(*args)
        print(f'Function {function.__name__!r}', time.time() - start_time)
        return res
    return wrapped


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


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def profile(func):
    def wrapper(*args, **kwargs):
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        print("{}:consumed memory: {:,}".format(
            func.__name__,
            mem_before, mem_after, mem_after - mem_before))

        return result

    return wrapper
