import glob
import os

import cv2
import imutils
import numpy as np
# import matplotlib.pyplot as plt
import mediapipe as mp
import imageio
import platform

import rawpy
from mtcnn.mtcnn import MTCNN


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
    Calculate Eye Aspect Ratio for one eye.

    Args:
        landmarks: (list) Detected landmarks list
        refer_idxs: (list) Index positions of the chosen landmarks
                            in order P1, P2, P3, P4, P5, P6
        frame_width: (int) Width of captured frame
        frame_height: (int) Height of captured frame

    Returns:
        ear: (float) Eye aspect ratio
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

# image_eyes_open = cv2.imread("closes_eyes/test-open-eyes.jpg")[:, :, ::-1]
# image_eyes_close = cv2.imread("closes_eyes/test-close-eyes.jpg")[:, :, ::-1]

def closes_eyes(put, format):
    sistem = platform.system()
    if 'Win' in sistem:
        sleh = '\\'
        ph = glob.glob(f'{put}/*.{format}')
    else:
        sleh = '/'
        ph = glob.glob(f'/{put}/*.{format}')
    # Загрузка изображения с лицами
    if len(ph) >= 1:
        for i in ph:
            if '.' in i:
                print(i)
                if format == 'raw':

                    with rawpy.imread(i) as raw:
                        thumb = raw.extract_thumb()
                    if thumb.format == rawpy.ThumbFormat.JPEG:
                        with open('thumb.jpeg', 'wb') as f:
                            f.write(thumb.data)
                    elif thumb.format == rawpy.ThumbFormat.BITMAP:
                        imageio.imsave('thumb.jpeg', thumb.data)
                    image = cv2.imread('thumb.jpeg')[:, :, ::-1]
                else:

                    image = cv2.imread(i)[:, :, ::-1]

                if image.shape[0] < image.shape[1]:
                    image = imutils.resize(image, height=1000)
                else:
                    image = imutils.resize(image, width=1000)

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

                            # print(EAR)

                if not os.path.isdir(put + sleh+'open_eyes'):
                    os.mkdir(put + sleh+'open_eyes')
                if not os.path.isdir(put + sleh+'closed_eyes'):
                    os.mkdir(put + sleh+'closed_eyes')
                # Работа с лицами
                ph_name = i.split(sleh)[-1]
                if EAR >= 0.15:
                    os.replace(put+sleh+ph_name, put + sleh+'open_eyes'+sleh+ph_name)
                else:
                    os.replace(put+sleh+ph_name, put + sleh+'closed_eyes'+sleh+ph_name)