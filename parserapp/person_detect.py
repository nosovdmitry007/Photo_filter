import glob
import os
import platform
import cv2
import cv2_ext
import imageio
import imutils
import numpy as np
import rawpy
import torch
import pandas as pd

def person_filter(put, format, cat):
    sistem = platform.system()
    if 'Win' in sistem:
        sleh = '\\'
    else:
        sleh = '/'
    ph = glob.glob(f'{put}/*.{format}')
    model_detect = torch.hub.load('./parserapp/yolov5_master', 'custom',
                                  path='./parserapp/model/yolov5m6.pt',
                                  source='local')
    for i in ph:
        i = i.split(sleh)[-1]
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
            image = cv2_ext.imread(put+sleh+i)

        if image.shape[0] < image.shape[1]:
            image = imutils.resize(image, height=1280)
        else:
            image = imutils.resize(image, width=1280)

        results = model_detect(image)
        df = results.pandas().xyxy[0]
        df = df.drop(np.where(df['confidence'] < 0.61)[0])

        if not os.path.isdir(put + sleh + cat):
            os.mkdir(put + sleh + cat)
        # Работа с лицами
        ob = pd.DataFrame()
        ob['class'] = df['name']
        oblasty = ob.values.tolist()
        oblasty = sum(oblasty, [])
        # print(oblasty)
        if cat in oblasty:
            os.replace(put + sleh + i, put + sleh + cat + sleh + i)