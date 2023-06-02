import face_recognition
# import imutils
import pickle
import time
import cv2
import os
import platform

class Fase:
    def __init__(self):
        # найдите путь к xml-файлу, содержащему каскадный файл haar
        cascPathface = "./frontalFace/haarcascade_frontalface_alt2.xml"
        # print(cascPathface)
        # загрузите haarcascade в каскадный классификатор
        self.faceCascade = cv2.CascadeClassifier(cascPathface)
        # assert not faceCascade.empty()
        # Найдите путь к изображению, на котором вы хотите обнаружить лицо, и передайте его здесь
    def face_indrtificator(self, image,path_face):
        # print(put)
        sistem = platform.system()
        if 'Win' in sistem:
            sleh = '\\'
        else:
            sleh = '/'
        # загрузите известные грани и вложения, сохраненные в последнем файле
        data = pickle.loads(open(f'{path_face}{sleh}face_enc', "rb").read())
        # print(image)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # преобразовать изображение в оттенки серого для haarcascade
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # faces = self.faceCascade.detectMultiScale(gray,
        #                                      scaleFactor=1.1,
        #                                      minNeighbors=5,
        #                                      minSize=(60, 60),
        #                                      flags=cv2.CASCADE_SCALE_IMAGE)

        # встраивание лиц для face in input
        encodings = face_recognition.face_encodings(rgb)
        # print(encodings)
        names = []
        #  зациклитесь на лицевых вставках, чтобы
        # у нас есть несколько вложений для нескольких fcaes
        for encoding in encodings:
            # Сравнить кодировки с кодировками в данных["кодировки"]
            # Совпадения содержат массив с логическими значениями и значением True для вложений, которым он точно соответствует
            # и False для остальных
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            # # установить name =inknown, если кодировка не совпадает
            # print(matches)
            name = "Unknown"
            # проверьте, нашли ли мы совпадение
            if True in matches:
                # Найдите позиции, в которых мы получаем значение True, и сохраните их
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                # print(matchedIdxs)
                counts = {}
                # перебирать совпадающие индексы и вести подсчет для
                # каждое распознанное лицо - face
                for i in matchedIdxs:
                    # Проверьте имена в соответствующих индексах, которые мы сохранили в matchedIdxs
                    name = data["names"][i]
                    # увеличьте количество для полученного нами имени
                    counts[name] = counts.get(name, 0) + 1
                    # установите имя, которое имеет наибольшее количество значений
                    name = max(counts, key=counts.get)
                    # print(name)
                    # print(counts)
                #обновите список имен
                names.append(name)
                # print(names)
        return names