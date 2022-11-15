import platform

from mtcnn.mtcnn import MTCNN
import statistics
import os
import cv2
import numpy
# import keras
import imutils
import tensorflow as tf

from tensorflow import keras
# from tensorflow.keras.models import load_model
# Создание сети нахождения лиц
detector = MTCNN()

# Загрузка модели сети определения лиц
embedder = keras.models.load_model('model/keras/facenet_keras.h5', compile=False)
put = 'test/фото'
sistem = platform.system()
if 'Win' in sistem:
    sleh = '\\'
else:
    sleh = '/'
# Загрузка видео
capture = cv2.VideoCapture(put)

lica = os.walk('test/лица')
for i in lica:
    if not os.path.isdir(put + sleh+i):
        os.mkdir(put + sleh + i)
# Получить дистанцию лица
def get_distance(model, face):

    face = face.astype('float32')
    face = (face - face.mean()) / face.std()
    face = numpy.expand_dims(face, axis=0)
    return embedder.predict(face)[0]


# Созданием базы с размечеными лицами
base = {}
for dirname in lica:

    base[dirname] = []
    for file in os.listdir(lica +sleh + dirname):

        if file.endswith('.jpg'):

            # Загрузка изображения с лицом
            image = cv2.imread(lica + sleh +dirname + sleh + file)

            # Замена BGR на RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Получить размеры изображения
            image_size = numpy.asarray(image.shape)[0:2]

            # Получение списка лиц с координатами и значением уверенности
            faces_boxes = detector.detect_faces(image)

            # Работа с лицами
            if faces_boxes:

                # Координаты лица
                x, y, w, h = faces_boxes[0]['box']

                # Выравнивание лица
                d = h - w  # Разница между высотой и шириной
                w = w + d  # Делаем изображение квадратным
                x = numpy.maximum(x - round(d / 2), 0)
                x1 = numpy.maximum(x, 0)
                y1 = numpy.maximum(y, 0)
                x2 = numpy.minimum(x + w, image_size[1])
                y2 = numpy.minimum(y + h, image_size[0])

                # Получение картинки с лицом
                cropped = image[y1:y2, x1:x2, :]
                face_image = cv2.resize(cropped, (160, 160), interpolation=cv2.INTER_AREA)

                # Сохранение суммы евклидова пространства
                base[dirname].append(get_distance(embedder, image))

frame_id = 0  # Инициализация счётчика кадров


for i in put:
    print(i)
    image = cv2.imread(put + sleh + i)
    lic = []
    # Если есть кадр
    # if success:

    # Увеличение/уменьшение наименьшей стороны изображения до 1000 пикселей
    if image.shape[0] < image.shape[1]:
        image = imutils.resize(image, height=1000)
    else:
        image = imutils.resize(image, width=1000)

    # Получить размеры изображения
    image_size = numpy.asarray(image.shape)[0:2]

    # Получение списка лиц с координатами и значением уверенности
    faces_boxes = detector.detect_faces(image)

    # Копия изображения для рисования рамок на нём
    # image_detected = frame.copy()

    # Замена BGR на RGB (так находит в два раза больше лиц)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Цвет меток BGR
    # marked_color = (0, 255, 0, 1)

    # Работа с лицами
    if faces_boxes:

        for face_box in faces_boxes:

            # Координаты лица
            x, y, w, h = face_box['box']

            # Выравнивание лица
            d = h - w  # Разница между высотой и шириной
            w = w + d  # Делаем изображение квадратным
            x = numpy.maximum(x - round(d / 2), 0)
            x1 = numpy.maximum(x, 0)
            y1 = numpy.maximum(y, 0)
            x2 = numpy.minimum(x + w, image_size[1])
            y2 = numpy.minimum(y + h, image_size[0])

            # Получение картинки с лицом
            cropped = image[y1:y2, x1:x2, :]
            face_image = cv2.resize(cropped, (160, 160), interpolation=cv2.INTER_AREA)

            # Получение дистанции
            distance = get_distance(embedder, face_image)

            # Координаты лица
            x, y, w, h = face_box['box']

            # # Отступы для увеличения рамки
            # d = h - w  # Разница между высотой и шириной
            # w = w + d  # Делаем изображение квадратным
            # x = numpy.maximum(x - round(d / 2), 0)
            # x1 = numpy.maximum(x - round(w / 4), 0)
            # y1 = numpy.maximum(y - round(h / 4), 0)
            # x2 = numpy.minimum(x + w + round(w / 4), image_size[1])
            # y2 = numpy.minimum(y + h + round(h / 4), image_size[0])

            # Отборка лиц {selected|rejected}
            if face_box['confidence'] > 0.99:  # 0.99 - уверенность сети в процентах что это лицо

                identity = None
                difference = None
                min_difference = 8
                median = None
                min_median = 8
                faces = {}

                # Сверка расстояний с известными лицами
                for name, base_distances in base.items():
                    faces[name] = []
                    for base_distance in base_distances:
                        difference = numpy.linalg.norm(base_distance - distance)
                        if difference < min_difference:
                            print('difference - ' + str(difference))
                            faces[name].append(difference)

                # Нахождение минимальной мидианы среди проголосовавших лиц
                if faces:
                    for name, items in faces.items():
                        # Идентификация только участвуют два и больше лиц
                        if items and len(items) >= 2:
                            print(name)
                            print(items)
                            median = statistics.median(items)
                            if median < min_median:
                                print('median - ' + str(median))
                                min_median = median
                                identity = name

                # Если лицо опознано
                if identity:
                    lic.append(identity)

        if len(lic) > 1:
            name = ''
            lic = lic.sort()
            for nam in lic:
                name= name+'_'+nam
            if not os.path.isdir(put + sleh + name):
                os.mkdir(put + sleh + name)
            os.replace(put + sleh + i, put + sleh + name + sleh + i)
        if len(lic) == 1:
            os.replace(put + sleh + i, put + sleh + lic[0] + sleh + i)