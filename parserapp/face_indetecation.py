import os
import cv2_ext
from .indeteficator_path import face_enc
from .indeteficator_face import Fase
from .dop_fun import slesh, resize_img
face = Fase()
def face_inc(path_face, path_photo):
    face_enc(path_face)
    photo = os.listdir(path_photo)
    sleh = slesh()
    if photo:
        for i in photo:
            frame = resize_img(cv2_ext.imread(f'{path_photo}{sleh}{i}'), 1280)
            person = face.face_indrtificator(frame, path_face)

            if person:
                s = '_'.join(sorted(person))
                if not os.path.isdir(f'{path_photo}/{s}'):
                    os.mkdir(f'{path_photo}{sleh}{s}')
                os.replace(f'{path_photo}{sleh}{i}',f'{path_photo}{sleh}{s}{sleh}{i}')
# face_inc('./Face_people','./face_test')
