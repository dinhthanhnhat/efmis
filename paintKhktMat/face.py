import math
import time
import cv2
import mediapipe as mp
import numpy as np
# import autopy
from pynput.mouse import Button, Controller
# import pyaudio
from win32api import GetSystemMetrics

def face():
    mp_drawing = mp.solutions.drawing_utils
    mp_face_mesh = mp.solutions.face_mesh

    ## For webcam input:
    drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
    prevTime = 0

    wCam, hCam = 256, 144
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)

    wScr, hScr = GetSystemMetrics(0), GetSystemMetrics(1)
    mouse = Controller()
    print(wScr, hScr)

    # SMOOTHING
    sm = 10
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    # ĐIỀU KIỆN RIGHCLICK
    t1 = 0
    t2 = 0
    check = True


    def distance_cal(x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))

    def getPoint(face, index):
        x = face.landmark[index].x
        y = face.landmark[index].y
        lx = int(x * shape[1])
        ly = int(y * shape[0])
        cv2.circle(image, (lx, ly), radius=1, color=(225, 0, 100), thickness=3)
        return lx, ly



    sx = 0
    sy = 0
    od = 1

    # while true:
    # nói: dùng mặt (phương thức) ->
    # dùng tay (phương thức) ->
    # nhập text ->
    # nhấn thả -> chọn phương thức dùng ->
    with mp_face_mesh.FaceMesh(
            max_num_faces=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as face_mesh:
        while cap.isOpened():
            success, image = cap.read()
            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = face_mesh.process(image)

            # Draw the face_and_app mesh annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_face_landmarks:
                cnt = 0
                for face in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)
                    shape = image.shape
                    l1x, l1y = getPoint(face, 11)
                    l2x, l2y = getPoint(face, 15)
                    ld = int(distance_cal(l1x, l1y, l2x, l2y))
                    nosex1, nosey1 = getPoint(face, 5)
                    l10x, l10y = getPoint(face, 10)
                    l152x, l152y = getPoint(face, 152)
                    ratioLength = int(distance_cal(l10x, l10y, l152x, l152y))
                    # print(f'mieng: {ld}')
                    # print(f'ti le {ratioLength}')
                    ratio = (ratioLength + 6) / 8.5
                    # print(f'ratio: {ratio}')
                    if ratio < ld:
                        print(True)
                    else:
                        print(False)
                    nosex2 = np.interp(nosex1 - 512, (0, wCam), (0, wScr))
                    nosey2 = np.interp(nosey1 - 288, (0, hCam), (0, hScr))
                    # print(nosex2,nosey2)
                    clocX = plocX + (nosex2 - plocX) / sm
                    clocY = plocY + (nosey2 - plocY) / sm
                    if nosex2 <= wScr and nosey2 <= hScr:
                        if clocX > sx + od or clocX < sx - od or clocY < sy - od or clocY > sy + od:
                            mouse.position = (clocX, clocY)
                    sx = clocX
                    sy = clocY
                    plocX, plocY = clocX, clocY
                    if ld > ratio:
                        if check == True:
                            t1 = time.time()
                            check = False
                    else:
                        t2 = time.time()
                        check = True
                    if t2 > t1 and t1 != 0:
                        if t2 - t1 > 5:
                            cv2.destroyAllWindows()
                            return
                        if t2 - t1 > 0.5:
                            mouse.click(Button.right)
                        else:
                            mouse.click(Button.left)
                        t2 = 0
                        t1 = 0
            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime
            cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
            cv2.imshow('Do you wanna be disabled?', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
# face()