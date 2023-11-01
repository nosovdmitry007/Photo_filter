import glob
import os
import platform
import cv2
import multiprocessing
import os
import platform
from multiprocessing import Process

import cv2_ext
import imageio
import imutils
import numpy as np
import rawpy
import torch
import pandas as pd
from ultralytics import YOLO
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor
class YOLO_filter:
    def __init__(self):
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        self.model_detect = YOLO("./model/yolov8l.pt")
    def sleh(self):
        sistem = platform.system()
        if 'Win' in sistem:
            sleh = '\\'
        else:
            sleh = '/'
        return sleh
    def resiz(self, ph, proc, return_dict, format):
        phot = {}
        for i in ph:
            if format == 'raw':
                with rawpy.imread(i) as raw:
                    thumb = raw.extract_thumb()
                if thumb.format == rawpy.ThumbFormat.JPEG:
                    with open('thumb.jpeg', 'wb') as f:
                        f.write(thumb.data)
                elif thumb.format == rawpy.ThumbFormat.BITMAP:
                    imageio.imsave('thumb.jpeg', thumb.data)
                image = cv2_ext.imread('thumb.jpeg')
            else:
                image = cv2_ext.imread(i)
            # print('2')
            if image.shape[0] < image.shape[1]:
                image = imutils.resize(image, height=640)
            else:
                image = imutils.resize(image, width=640)
            phot[i] = image
        return_dict[proc] = phot

    def sort_img(self, put, cat_nam, spis):
        sleh = self.sleh()
        if not os.path.isdir(put + sleh+ cat_nam):
            os.mkdir(put + sleh + cat_nam)
        # Работа с лицами
        for i in spis:
            os.replace(put + sleh + i, put + sleh + cat_nam + sleh + i)

    def yol(self, nam, phot, cat, put):
        n = 15
        if len(phot) > n:

            phot1 = [phot[i:i + n] for i in range(0, len(phot), n)]
            nam1 = [nam[i:i + n] for i in range(0, len(nam), n)]

        for n, f in zip(nam1, phot1):

            # results = self.model_detect(f, imgsz=640, device=self.device, classes=int(cat))
            results = self.model_detect(f, imgsz=640, device=self.device, classes=int(cat), stream=True, conf=0.5)
            print('675')
            # print(list(results))
            spis_img_cat = []
            for nm, result in zip(n, results):
                if len(result.boxes.data.tolist()) > 0:
                    spis_img_cat.append(nm.split('/')[-1])
                    cat_nam = result.names[int(cat)]
            self.sort_img(put, cat_nam, spis_img_cat)

    def person_filter(self, put, format, cat):

        ph = glob.glob(f'{put}/*.{format}')

        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        col_proc = multiprocessing.cpu_count() - 1
        splits = np.array_split(ph, col_proc)
        phot = []
        for array in splits:
            phot.append(list(array))

        processes = []
        z = 0
        for i in phot:
            z += 1
            p = Process(target=self.resiz, args=(i, z, return_dict, format))
            processes.append(p)
            p.start()
        for process in processes:
            process.join()

        ph_sz = return_dict.values()
        kart = ph_sz[0]
        print('0')
        if len(ph_sz) > 1:
            for i in range(1, col_proc):
                kart = {**kart, **ph_sz[i]}
        nam_img = list(kart.keys())
        img = list(kart.values())

        self.yol(nam_img, img, cat, put)



        # print(ph)
        # for i in ph:
        #     print(i)
        #     i = i.split(sleh)[-1]
        #     if form == 'raw':
        #
        #         with rawpy.imread(put + sleh + i) as raw:
        #             thumb = raw.extract_thumb()
        #         if thumb.format == rawpy.ThumbFormat.JPEG:
        #             with open('thumb.jpeg', 'wb') as f:
        #                 f.write(thumb.data)
        #         elif thumb.format == rawpy.ThumbFormat.BITMAP:
        #             imageio.imsave('thumb.jpeg', thumb.data)
        #         image = cv2_ext.imread('thumb.jpeg')
        #     else:
        #         image = cv2_ext.imread(put+sleh+i)
        #         print('2')
        #     if image.shape[0] < image.shape[1]:
        #         image = imutils.resize(image, height=640)
        #     else:
        #         image = imutils.resize(image, width=640)
        #     print('3')
        #     print(self.device)
            # print(image)
            # results = self.model_detect(image, imgsz=640, device=self.device, classes=int(cat))
            # # print(results)
            # for result in results:
            #     column = ['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class']
            #     df = pd.DataFrame(result.boxes.data.tolist(), columns=column)
            #     df['name'] = df['class'].apply(lambda x: result.names[x])
            #     cat_nam = result.names[int(cat)]
            # df = df.drop(np.where(df['confidence'] < 0.5)[0])

            # if not os.path.isdir(put + sleh + cat_nam):
            #     os.mkdir(put + sleh + cat_nam)
            # # Работа с лицами
            # ob = pd.DataFrame()
            # ob['class'] = df['name']
            # oblasty = ob.values.tolist()
            # oblasty = sum(oblasty, [])
            # if cat in oblasty:
            #     os.replace(put + sleh + i, put + sleh + cat_nam + sleh + i)