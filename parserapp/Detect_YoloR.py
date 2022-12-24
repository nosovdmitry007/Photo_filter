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
    # model_detect = torch.hub.load('yolor-main', 'custom', path='./parserapp/model/yolor_p6.pt',
    # #                               source='local')
    # model_detect = cv2.dnn.readNet("./model/yolor_p.weights", "./model/yolor_p6.cfg")
    #
    # with open("./yolor-main/data/coco.names","r") as f:
    #     classes = [line.strip() for line in f.readlines()]
    # layer_names = model_detect.getLayerNames()
    # output_layers = [layer_names[i - 1] for i in model_detect.getUnconnectedOutLayers()]
    # # Loading image
    # img = cv2.imread(put)



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
        img = put+sleh+i
        os.system("python yolor-main/detect.py --weights 'model/yolor_p6.pt' --source img --img-size 1280 --device 0 --project test --name 0 --exist-ok")
        # height, width, channels = image.shape
        #
        # blob = cv2.dnn.blobFromImage(image, 0.00392, (1280, 1280), (0, 0, 0), True, crop=False)
        # model_detect.setInput(blob)
        # outs = model_detect.forward(output_layers)
        #
        # # Showing informations on the screen
        # class_ids = []
        # confidences = []
        # boxes = []
        # for out in outs:
        #     for detection in out:
        #         scores = detection[5:]
        #         class_id = np.argmax(scores)
        #         confidence = scores[class_id]
        #         if confidence > 0.5:
        #             # Object detected
        #             center_x = int(detection[0] * width)
        #             center_y = int(detection[1] * height)
        #             w = int(detection[2] * width)
        #             h = int(detection[3] * height)
        #             # Rectangle coordinates
        #             x = int(center_x - w / 2)
        #             y = int(center_y - h / 2)
        #             boxes.append([x, y, w, h])
        #             confidences.append(float(confidence))
        #             class_ids.append(class_id)
        # indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        # d = []
        # z = []
        # for i in indexes:
        #     box = boxes[i]
        #     print(classes[class_ids[i]])
        #     # d.append(box)
        #     # d.append(confidences[i])
        #
        # if image.shape[0] < image.shape[1]:
        #     image = imutils.resize(image, height=1280)
        # else:
        #     image = imutils.resize(image, width=1280)

        # results = model_detect(image)
        # df = results.pandas().xyxy[0]
        # df = df.drop(np.where(df['confidence'] < 0.67)[0])
        #
        # if not os.path.isdir(put + sleh + cat):
        #     os.mkdir(put + sleh + cat)
        # # Работа с лицами
        # ob = pd.DataFrame()
        # ob['class'] = df['name']
        # oblasty = ob.values.tolist()
        # oblasty = sum(oblasty, [])
        # # print(oblasty)
        # if cat in oblasty:
        #     os.replace(put + sleh + i, put + sleh + cat + sleh + i)

person_filter('D:\\RAW\\2022.12.11\\Джек\\person','jpg','person')


# def convert(cfg='../models/yolov4-csp.cfg', weights='../runs/exp26_yolov4-csp-/weights/best_yolov4-csp-.pt', saveto='yolov4-csp-desk-800-100.weights'):
#     # Converts between PyTorch and Darknet format per extension (i.e. *.weights convert to *.pt and vice versa)
#     from models import *
#     convert('cfg/yolov3-spp.cfg', 'weights/yolov3-spp.weights')
