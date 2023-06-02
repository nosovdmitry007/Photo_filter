import os
import cv2
import imutils
from .indeteficator_path import face_enc
from .indeteficator_face import Fase
import platform
face = Fase()
def face_inc(path_face, path_photo):
    face_enc(path_face)
    photo = os.listdir(path_photo)
    sistem = platform.system()
    if 'Win' in sistem:
        sleh = '\\'
    else:
        sleh = '/'
    if photo:
        for i in photo:
            frame = cv2.imread(f'{path_photo}{sleh}{i}')
            if frame.shape[0] < frame.shape[1]:
                frame = imutils.resize(frame, width=1280)
            else:
                frame = imutils.resize(frame, height=1280)
            person = face.face_indrtificator(frame, path_face)

            if person:
                s = '_'.join(sorted(person))
                if not os.path.isdir(f'{path_photo}/{s}'):
                    os.mkdir(f'{path_photo}{sleh}{s}')
                os.replace(f'{path_photo}{sleh}{i}',f'{path_photo}{sleh}{s}{sleh}{i}')
# face_inc('./Face_people','./face_test')
