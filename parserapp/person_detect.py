import glob
import multiprocessing
import os
from multiprocessing import Process
import cv2_ext
import numpy as np
import torch
from ultralytics import YOLO
from .dop_fun import slesh,resize_img, read_raw


class YOLO_filter:
    def __init__(self):
        self.device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
        self.model_detect = YOLO("./model/yolov8l.pt")

    def resiz(self, ph, proc, return_dict, format):
        phot = {}
        for i in ph:
            if format == 'raw':
                image = read_raw(i)
            else:
                image = cv2_ext.imread(i)
            image = resize_img(image,640)
            phot[i] = image
        return_dict[proc] = phot

    def sort_img(self, put, cat_nam, spis):
        sleh = slesh()
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
            results = self.model_detect(f, imgsz=640, device=self.device, classes=int(cat), stream=True, conf=0.5)
            spis_img_cat = []

            for nm, result in zip(n, results):
                if len(result.boxes.data.tolist()) > 0:
                    spis_img_cat.append(nm.split('/')[-1])
                    cat_nam = result.names[int(cat)]
            if len(spis_img_cat) > 0:
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
        if len(ph_sz) > 1:
            for i in range(1, col_proc):
                kart = {**kart, **ph_sz[i]}
        nam_img = list(kart.keys())
        img = list(kart.values())
        self.yol(nam_img, img, cat, put)