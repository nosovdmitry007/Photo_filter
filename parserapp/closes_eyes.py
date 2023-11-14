import glob
import os
import cv2_ext
import numpy as np
import mediapipe as mp
from .dop_fun import read_raw, slesh, resize_img

mp_facemesh = mp.solutions.face_mesh
mp_drawing  = mp.solutions.drawing_utils
denormalize_coordinates = mp_drawing._normalized_to_pixel_coordinates

# The chosen 12 points:   P1,  P2,  P3,  P4,  P5,  P6
chosen_left_eye_idxs  = [362, 385, 387, 263, 373, 380]
chosen_right_eye_idxs = [33,  160, 158, 133, 153, 144]
def distance(point_1, point_2):
    """Calculate l2-norm between two points"""
    dist = sum([(i - j) ** 2 for i, j in zip(point_1, point_2)]) ** 0.5
    return dist
def get_ear(landmarks, refer_idxs, frame_width, frame_height):
    """
    Рассчитайте соотношение сторон глаз для одного глаза.

    Аргументы:
        ориентиры: (список) Список обнаруженных ориентиров
        refer_idxs: (список) Расположение индексов выбранных ориентиров
                            в порядке P1, P2, P3, P4, P5, P6
    frame_width: (int) Ширина захваченного кадра
        frame_height: (int) Высота захваченного кадра

    Возвращается:
        EAR: (плавает) Соотношение сторон глаз
    """
    try:
        # Compute the euclidean distance between the horizontal
        coords_points = []
        for i in refer_idxs:
            lm = landmarks[i]
            coord = denormalize_coordinates(lm.x, lm.y, frame_width, frame_height)
            coords_points.append(coord)

        # Eye landmark (x, y)-coordinates
        P2_P6 = distance(coords_points[1], coords_points[5])
        P3_P5 = distance(coords_points[2], coords_points[4])
        P1_P4 = distance(coords_points[0], coords_points[3])

        # Compute the eye aspect ratio
        ear = (P2_P6 + P3_P5) / (2.0 * P1_P4)

    except:
        ear = 0.0
        coords_points = None

    return ear, coords_points

def calculate_avg_ear(landmarks, left_eye_idxs, right_eye_idxs, image_w, image_h):
    # Calculate Eye aspect ratio
    left_ear,  _ = get_ear(landmarks, left_eye_idxs,  image_w, image_h)
    right_ear, _ = get_ear(landmarks, right_eye_idxs, image_w, image_h)

    Avg_EAR = (left_ear + right_ear) / 2
    return Avg_EAR

def closes_eyes(put, format):
    sleh = slesh()
    # Загрузка изображения с лицами
    ph = glob.glob(f'{put}/*.{format}')

    if len(ph) >= 1:
        for i in ph:
            i = i.split(sleh)[-1]
            if format == 'raw':
                image = read_raw(put + sleh + i)
            else:
                image = cv2_ext.imread(put + sleh + i)
            image = resize_img(image, 1000)
            image = np.ascontiguousarray(image)
            imgH, imgW, _ = image.shape

            # Running inference using static_image_mode
            with mp_facemesh.FaceMesh(refine_landmarks=True) as face_mesh:
                results = face_mesh.process(image)

                # If detections are available.
                if results.multi_face_landmarks:

                    # Iterate over detections of each face. Here, we have max_num_faces=1, so only one iteration is performed.
                    for face_id, face_landmarks in enumerate(results.multi_face_landmarks):
                        landmarks = face_landmarks.landmark
                        EAR = calculate_avg_ear(landmarks, chosen_left_eye_idxs, chosen_right_eye_idxs, imgW, imgH)

                    if not os.path.isdir(put + sleh+'open_eyes'):
                        os.mkdir(put + sleh+'open_eyes')
                    if not os.path.isdir(put + sleh+'closed_eyes'):
                        os.mkdir(put + sleh+'closed_eyes')
                    # Работа с лицами
                    if EAR >= 0.1:
                        os.replace(put+sleh+i, put + sleh+'open_eyes'+sleh+i)
                    else:
                        os.replace(put+sleh+i, put + sleh+'closed_eyes'+sleh+i)