import rawpy
import imageio
import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import os #Работа с папками и файлами
import platform

def filterphoto(put,format):
#Создаём классы по которым будем класифицировать фотографии
    sistem = platform.system()
    if 'Win' in sistem:
        sleh = '\\'
    else:
        sleh = '/'
    className=['Fokus','Good_foto','Peresvet','Temniy']
    #Размер изображения для НС
    visota=50
    shirina=50
    sloi=3
    xTest = []

    puti = [_ for _ in os.listdir(put) if _.endswith(f'.{format}')]

    #обрабатываем каждый файл и добавляем в массив для распознания
    if len(puti) >= 1:
        for j in puti:
            if '.' in j:
                if format == 'raw':
                    with rawpy.imread(put + sleh + j) as raw:
                        thumb = raw.extract_thumb()
                    if thumb.format == rawpy.ThumbFormat.JPEG:
                        with open('thumb.jpeg', 'wb') as f:
                            f.write(thumb.data)
                    elif thumb.format == rawpy.ThumbFormat.BITMAP:
                        imageio.imsave('thumb.jpeg', thumb.data)
                    L = Image.open('thumb.jpeg')
                else:
                    L = Image.open(put + sleh +j)


                z = L.resize((visota, shirina))
                x = image.img_to_array(z)
                x = x.reshape(visota, shirina, sloi)
                x /= 255
                xTest.append(x)  # добавляем в обучающую выборку
        #преобразуем в нампай массив
        xTest = np.array(xTest)
        L.close()

        # data_file= open(,'r')
        model1 = load_model('./parserapp/best_model_87.3.h5', compile=False)
    #создаем папки по категориям
        for k in className:
            if not os.path.isdir(put + sleh + k):
                os.mkdir(put + sleh + k)
    #определяем категории фотографий
        prediction = model1.predict(xTest) #Классифицируем каждое изображение
    #раскидываем фотографии по папкам
        for i in range(len(puti)): #Проходим по картинкам
          #Вводим результаты на экран

            os.replace(put + sleh + puti[i], put + sleh + className[np.argmax(prediction[i])] + sleh + puti[i])
    #удаляем пустые папки с категориями
        for k in className:
            if len(os.listdir(put + sleh + k)) == 0:
                os.rmdir(put + sleh + k)
