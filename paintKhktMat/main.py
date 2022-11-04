import cv2
import mediapipe as mp
import time
from . import hocVe
import math
from . import hocViet
from . import vuaTiengViet
from . import hocToan
from . import face
from . import Subway
import numpy as np
# from pynput.keyboard import Key, Controller

# keyboard = Controller()

checkout = True

def main(lang):
    # with keyboard.pressed(Key.alt):
    #     keyboard.press(Key.tab)
    frameWidth = 16 * 80
    frameHeight = 9 * 80
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    mpFaceMesh = mp.solutions.face_mesh
    mpDraw = mp.solutions.drawing_utils
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)

    pTime = 0
    cTime = 0

    sm = 3
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    constHd = 35
    wScr, hScr = 16 * 130, 9 * 130

    #set color
    black = (0, 0, 0)
    penSize = 20

    def getPoint(hand, index):
        x = hand.landmark[index].x
        y = hand.landmark[index].y
        x = int(x * 1280)
        y = int(y * 720)
        cv2.circle(recognize, (x, y), radius=3, color=black, thickness=-1)
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
    global checkout
    checkout = True
    while True:
        img = cv2.imread(f'./art/homePage1{lang}.png')
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
        results = faceMesh.process(imgRGB)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                x0, y0 = getPoint(face_landmarks, 0)
                x17, y17 = getPoint(face_landmarks, 16)
                xPoint = x0
                yPoint = y0
                xPoint = clocX = plocX + (xPoint - plocX) // sm
                yPoint = clocY = plocY + (yPoint - plocY) // sm
                plocX, plocY = clocX, clocY
                paintPoint(xPoint, yPoint, black, round(penSize / 2))

                range8_4 = distance_cal(x0, y0, x17, y17)

                x96, y96 = getPoint(face_landmarks, 61)
                x235, y235 = getPoint(face_landmarks, 291)
                range0_5 = distance_cal(x235, y235, x96, y96)
                # paintPoint(x96, y96, black, round(penSize / 2))
                # paintPoint(x235, y235, black, round(penSize / 2))
                # keyboard.type(str(range8_4))
                # keyboard.press(Key.right)
                # keyboard.type(str(range0_5))
                # keyboard.press(Key.enter)
                # keyboard.press(Key.left)
                # time.sleep(0.1)
                # print(range8_4)
                # print(range0_5)
                status = False
                if range0_5 > 250:
                    ratio = math.sqrt((range0_5 - 250) / 0.005)
                    if ratio < range8_4:
                        # continue
                        status = True

                if status == True:
                    if 163 <= xPoint <= 507 and 251 <= yPoint <= 597:
                        cv2.destroyAllWindows()
                        hocVe.hocVe(lang)
                        return True
                    if 804 <= xPoint <= 1146 and 251 <= yPoint <= 597:
                        cv2.destroyAllWindows()
                        hocViet.hocViet(lang)
                        return True
                    if 1143 <= xPoint <= 1773 and 251 <= yPoint <= 597:
                        cv2.destroyAllWindows()
                        vuaTiengViet.VuaTiengViet(lang)
                        return True
                    if 163 <= xPoint <= 507 and 663 <= yPoint <= 1003:
                        cv2.destroyAllWindows()
                        hocToan.HocToan(lang);
                        return True
                    if 804 <= xPoint <= 1146 and 663 <= yPoint <= 1003:
                        cv2.destroyAllWindows()
                        Subway.Subway()
                        return True
                    if 1143 <= xPoint <= 1773 and 663 <= yPoint <= 1003:
                        cv2.destroyAllWindows()
                        face.face()
                        return True
                    if 1795 <= xPoint <= 1869 and 57 <= yPoint <= 131:
                        cv2.destroyAllWindows()
                        checkout = False
                        return False
        # Write frame rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "FPS= " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)

        # if showWindow == True:
        cv2.imshow('image', img)
        # cv2.imshow('test', recognize)
        # if status == True:
        #     cv2.destroyallwindows()
        if cv2.waitKey(1) == 27:
            break
def mat(lang):
    global checkout
    checkout = True
    while True:
        if checkout:
            main(lang)
        else:
            return