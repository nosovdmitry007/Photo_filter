import os
import platform

import cv2
import imageio
import numpy as np
import math

import rawpy
import torch
import pandas as pd


def person_filter(put):
    sistem = platform.system()
    if 'Win' in sistem:
        sleh = '\\'
    else:
        sleh = '/'
    model_detect = torch.hub.load('yolov5_master', 'custom', path='model/yolov5x.pt', source='local')
    ph = os.listdir(put)
    for i in ph:
        if '.' in i:
            if format == 'raw':

                with rawpy.imread(put + sleh + i) as raw:
                    thumb = raw.extract_thumb()
                if thumb.format == rawpy.ThumbFormat.JPEG:
                    with open('thumb.jpeg', 'wb') as f:
                        f.write(thumb.data)
                elif thumb.format == rawpy.ThumbFormat.BITMAP:
                    imageio.imsave('thumb.jpeg', thumb.data)
                image = cv2.imread('thumb.jpeg')
            else:
                image = cv2.imread(put+sleh+i)

            # img = '/home/dima/PycharmProjects/Photo_filter/python-facedars-master/demo/detection_image/input/face/people.jpg'
            results = model_detect(image)
            df = results.pandas().xyxy[0]
            df = df.drop(np.where(df['confidence'] < 0.7)[0])

            if not os.path.isdir(put + sleh + 'person'):
                os.mkdir(put + sleh + 'face')
            if not os.path.isdir(put + sleh + 'no_face'):
                os.mkdir(put + sleh + 'no_face')
            # Работа с лицами
            if 'person' in df['name']:
                os.replace(put + sleh + i, put + sleh + 'person' + sleh + i)
            else:
                os.replace(put + sleh + i, put + sleh + 'no_person' + sleh + i)