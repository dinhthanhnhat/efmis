import math
import time
import cv2
import mediapipe as mp
import numpy as np
from pynput.mouse import Button, Controller
from win32api import GetSystemMetrics
from .handDetector import HandDetector

def hand():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    wCam, hCam = 16 * 30, 9 * 30
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)
    cap.set(4, 720)
    prevTime = 0

    wScr, hScr = GetSystemMetrics(0), GetSystemMetrics(1)
    mouse = Controller()
    print(wScr, hScr)

    # SMOOTHING
    sm = 10
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    # ĐIỀU KIỆN RIGHCLICK + MIDDLECLICK
    t1 = 0
    t2 = 0
    check = True

    # ĐIỀU KIỆN LEFTCLICK + PRESS/RELEASE
    t3 = 0
    t4 = 0
    check2 = True
    cnt = 0

    # ĐIều kiênk scroll
    toadoDau = 0
    toadoCuoi = 0

    # ĐIỀU KIỆN RETURN
    check0 = 0
    t0 = 0
    t = 0

    def distance_cal(x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))


    # def getstartpoint(lmList):
    #     x, y = 1280, 720
    #     for lm in lmList:
    #         x, y = min(lmList[lm].x, x), min(lmList[lm].y, y)
    #     return x, y
    #
    # def getendpoint(lmList):
    #     x, y = 0, 0
    #     for lm in lmList:
    #         x, y = max(lmList[lm].x, x), max(lmList[lm].y, y)
    #     return x, y

    sx = 0
    sy = 0
    od = 1

    ms = 0
    ds = 0

    handDetector = HandDetector(min_detection_confidence=0.7, max_num_hands=1)


    with mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            handcnt = 0
            handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
            count = 0
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    shape = image.shape
                    # # BBOX
                    # x, y = 1280, 720
                    # for i in range(0, 21):
                    #     x, y = min(hand_landmarks.landmark[i].x, x), min(hand_landmarks.landmark[i].y, y)
                    # x, y = int(x * shape[1]), int(y * shape[0])
                    # sP = [x, y]
                    # x, y = 0, 0
                    # for i in range(0, 21):
                    #     x, y = max(hand_landmarks.landmark[i].x, x), max(hand_landmarks.landmark[i].y, y)
                    # x, y = int(x * shape[1]), int(y * shape[0])
                    # eP = [x, y]
                    # # print(sP, eP)
                    # cv2.rectangle(image, sP, eP, (255, 0, 255), 3)

                    # VẼ
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    # TỌA ĐỘ
                    x, y = hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y
                    x8, y8 = int(x * shape[1]), int(y * shape[0])  # ngón trỏ

                    x, y = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y
                    x12, y12 = int(x * shape[1]), int(y * shape[0])  # ngón giữa

                    x, y = hand_landmarks.landmark[20].x, hand_landmarks.landmark[20].y
                    x20, y20 = int(x * shape[1]), int(y * shape[0])  # ngón út

                    x, y = hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y
                    x4, y4 = int(x * shape[1]), int(y * shape[0])  # ngón cái

                    x, y = hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y
                    x0, y0 = int(x * shape[1]), int(y * shape[1])  # diemgiua

                    x, y = hand_landmarks.landmark[5].x, hand_landmarks.landmark[5].y
                    x5, y5 = int(x * shape[1]), int(y * shape[1])  # diemgiua
                    if (len(handLandmarks) != 0):

                        if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:  # Right Thumb
                            count = count + 1
                        elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:  # Left Thumb
                            count = count + 1
                        if handLandmarks[8][2] < handLandmarks[6][2]:  # Index finger
                            count = count + 1
                        if handLandmarks[12][2] < handLandmarks[10][2]:  # Middle finger
                            count = count + 1
                        if handLandmarks[16][2] < handLandmarks[14][2]:  # Ring finger
                            count = count + 1
                        if handLandmarks[20][2] < handLandmarks[18][2]:  # Little finger
                            count = count + 1
                    # print(count)

                    # KHOẢNG CÁCH
                    # print(x4, y4, x8, y8)
                    d812 = distance_cal(x12, y12, x8, y8)
                    d48 = distance_cal(x4, y4, x8, y8)
                    d05 = distance_cal(x0, y0, x5, y5)
                    d412 = distance_cal(x4, y4, x12, y12)

                    # DI CHUYỂN
                    x2 = np.interp(x20 - (1280 - wCam) // 2, (0, wCam), (0, wScr))
                    y2 = np.interp(y20 - (720 - hCam) // 2, (0, hCam), (0, hScr))
                    clocX = plocX + (x2 - plocX) / sm
                    clocY = plocY + (y2 - plocY) / sm
                    if x2 <= wScr and 2 <= hScr:
                        if clocX > sx + od or clocX < sx - od or clocY < sy - od or clocY > sy + od:
                            mouse.position = (clocX, clocY)
                    sx = clocX
                    sy = clocY
                    plocX, plocY = clocX, clocY
                    # print('cai tro:', d48)
                    # print('giua cai:', d05)
                    # print('ti le: ', d05 / 9 / d48)

                    # THAO TÁC
                    if count == 0:
                        if check0 == True:
                            t3 = time.time()
                            check0 = False
                    t = time.time()
                    if count != 0:
                        check0 = True
                    if check0 == False and t - t3 >= 1 and len(handLandmarks) > 0:
                        cv2.destroyAllWindows()
                        return

                    if d48 != 0:
                        if d05 / 9 / d48 > 0.7:
                            if check2 == True:
                                t3 = time.time()
                                check2 = False
                            # if ms == 0:
                            #     mouse.press(Button.left)
                            #     ms = 1
                    t4 = time.time()
                    if d48 != 0:
                        if ms == 1 or cnt == 1:
                            if d05 / 9 / d48 <= 0.7:
                                check2 = True
                                mouse.release(Button.left)
                                ms = 0
                                cnt = 0
                    if check2 == True and t4 - t3 <= 0.2:
                        if cnt == 0:
                            cnt = 1
                            mouse.click(Button.left)
                    elif check2 == False and t4 - t3 > 0.2:
                        if ms == 0:
                            ms = 1
                            mouse.press(Button.left)

    #  d05 / 9 / d48 > 0.7:
    #   if check == True:
    #       t1 = time.time()
    #       check = False
    # se:
    #   t2 = time.time()
    #   check = True
    #  t2 > t1 and t1 != 0:
    #   if t2 - t1 > 5:
    #       cv2.destroyAllWindows()
    #       return
    #   elif t2 - t1 > 0.5:
    #       mouse.click(Button.right)
    #   else:
    #       mouse.click(Button.left)
    #   t2 = 0
    #   t1 = 0

                    # print(d812)
                    if d812 != 0 and d05 / 9 / d812 > 0.5:
                        if check == True:
                            t1 = time.time()
                            toadoDau = y8
                            toadoCuoi = 0

                            check = False
                    t2 = time.time()
                    if toadoCuoi != 0:
                        toadodau = toadoCuoi
                    toadoCuoi = y8

                    if d812 != 0 and d05 / 9 / d812 < 0.5 and check == False:
                        check = True
                    if t2 - t1 > 0.5 and check == False:
                        print(f'toa do dau {toadodau}')
                        print(f'toa do cuoi {toadoCuoi}')
                        mouse.scroll(0, (toadoDau - toadoCuoi) / 100)
                    if t2 - t1 <= 0.5 and check == True:
                        mouse.click(Button.right)
                        # check = True

            currTime = time.time()
            fps = 1 / (currTime - prevTime)
            prevTime = currTime
            cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 196, 255), 2)
            cv2.imshow('OK bruh bruh lmouse', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
# hand()