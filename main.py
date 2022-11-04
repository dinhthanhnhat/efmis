import cv2
import mediapipe as mp
import numpy as np
import math
import time
import sys
import os

# from ..paintKhktMat import main as mat
from paintKhktTay import main as tay
from paintKhktMat import main as mat

lang = ''

def main():
    global lang
    frameWidth = 1280
    frameHeight = 720
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    cTime = 0

    sm = 3
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    constHd = 35
    wScr, hScr = 1920, 1080

    #set color
    black = (0, 0, 0)
    penSize = 20

    langPre = False
    langNow = False

    def getPoint(hand, index):
        x = hand.landmark[index].x
        y = hand.landmark[index].y
        x = int(x * 1280)
        y = int(y * 720)
        cv2.circle(recognize, (x, y), radius=10, color=black, thickness=-1)
        h, w, c = img.shape
        wCam = 16 * constHd
        hCam = 9 * constHd
        lx = int(np.interp(x - (1280 - wCam) // 2, (0, wCam), (0, wScr)))
        ly = int(np.interp(y - (720 - hCam) // 2, (0, hCam), (0, hScr)))
        return lx, ly


    def paintPoint(lx, ly, color, radius):
        cv2.circle(img, (lx, ly), radius=radius, color=color, thickness=1)

    def distance_cal(x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))

    showWindow = True
    with mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.9) as hands:
        while cap.isOpened():
            img = cv2.imread(f'./homePage{lang}.png')
            if showWindow == False:
                cv2.destroyAllWindow()
                showWindow = True
                time.sleep(2)
            success, recognize = cap.read()
            if not success:
                continue
            recognize = cv2.flip(recognize, 1)
            imgRGB = cv2.cvtColor(recognize, cv2.COLOR_BGR2RGB)

            # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    x8, y8 = getPoint(handLms, 8)
                    x4, y4 = getPoint(handLms, 4)
                    xPoint = (x8 + x4) // 2
                    yPoint = (y8 + y4) // 2
                    xPoint = clocX = plocX + (xPoint - plocX) // sm
                    yPoint = clocY = plocY + (yPoint - plocY) // sm
                    plocX, plocY = clocX, clocY
                    paintPoint(xPoint, yPoint, black, round(penSize / 2))

                    range8_4 = distance_cal(x8, y8, x4, y4)

                    x5, y5 = getPoint(handLms, 5)
                    x0, y0 = getPoint(handLms, 0)
                    range0_5 = distance_cal(x0, y0, x5, y5)

                    ratio = range0_5 * 0.32
                    status = False
                    if ratio > range8_4:
                        status = True

                    print(xPoint, yPoint)
                    langPre = langNow
                    if status == True:
                        if 338 <= xPoint <= 777 and 267 <= yPoint <= 706:
                            cv2.destroyAllWindows()
                            tay.tay(lang)
                            return
                        if 1097 <= xPoint <= 1536 and 267 <= yPoint <= 706:
                            cv2.destroyAllWindows()
                            mat.mat(lang)
                            return
                        if 1795 <= xPoint <= 1869 and 57 <= yPoint <= 131:
                            cv2.destroyAllWindows()
                            exit()
                        if 72 <= xPoint <= 394 and 889 <= yPoint <= 1025:
                            langNow = True
                            if (langNow == True and langPre != langNow):
                                if (lang == ''):
                                    lang = 'ENG'
                                else:
                                    lang = '';
                        else:
                            langNow = False
            # Write frame rate
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, "FPS= " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)

            # if showWindow == True:
            cv2.imshow(f'./homePage{lang}.png', img)
            # if status == True:
            #     cv2.destroyallwindows()
            if cv2.waitKey(1) == 27:
                break
while True:
    main()

