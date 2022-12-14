import os
import platform

import imageio
import rawpy
from mtcnn.mtcnn import MTCNN
import cv2
import numpy
import imutils
def face_filter(put):
    # photo = 'people.jpg'
    # Создание сети нахождения лиц
    sistem = platform.system()
    if 'win' in sistem:
        sleh = '\\'
    else:
        sleh = '/'
    detector = MTCNN()
    ph = os.listdir(put)

    # Загрузка изображения с лицами
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

            # Увеличение/уменьшение наименьшей стороны изображения до 1000 пикселей
            if image.shape[0] < image.shape[1]:
                image = imutils.resize(image, height=1000)
            else:
                image = imutils.resize(image, width=1000)

            # Получение списка лиц с координатами и значением уверенности
            faces_boxes = detector.detect_faces(image)
            if not os.path.isdir(put + sleh+'face'):
                os.mkdir(put + sleh+'face')
            if not os.path.isdir(put + sleh+'no_face'):
                os.mkdir(put + sleh+'no_face')
            # Работа с лицами
            if faces_boxes:
                os.replace(put+sleh+i, put + sleh+'face'+sleh+i)
            else:
                os.replace(put+sleh+i,put + sleh+'no_face'+sleh+i)