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
from ultralytics import YOLO
class YOLO_filter:
    def  __init__(self):
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        self.model_detect = YOLO("./model/yolov8l.pt")
    def person_filter(self, put, format, cat):
        print(cat)
        sistem = platform.system()
        if 'Win' in sistem:
            sleh = '\\'
        else:
            sleh = '/'
        ph = glob.glob(f'{put}/*.{format}')

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
                image = imutils.resize(image, height=640)
            else:
                image = imutils.resize(image, width=640)

            results = self.model_detect(image, imgsz=640, device=self.device, classes=int(cat))
            for result in results:
                column = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class']
                df = pd.DataFrame(result.boxes.data.tolist(), columns=column)
                df['name'] = df['class'].apply(lambda x: result.names[x])
                cat_nam = result.names[int(cat)]
            df = df.drop(np.where(df['confidence'] < 0.5)[0])

            if not os.path.isdir(put + sleh + cat_nam):
                os.mkdir(put + sleh + cat_nam)
            # Работа с лицами
            ob = pd.DataFrame()
            ob['class'] = df['name']
            oblasty = ob.values.tolist()
            oblasty = sum(oblasty, [])
            if cat in oblasty:
                os.replace(put + sleh + i, put + sleh + cat_nam + sleh + i)