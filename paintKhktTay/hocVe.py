import math
import os
import time
import numpy as np
import cv2
import mediapipe as mp



def hocVe(lang):
    constHd = 45
    wScr, hScr = 16 * 125, 9 * 125
    xtemp = ytemp = 0
    disRatio = 1280 // 14

    def getPoint(hand, index):
        x = hand.landmark[index].x
        y = hand.landmark[index].y
        x = int(x * 1280)
        y = int(y * 720)
        cv2.circle(recognize, (x, y), radius=10, color=gray, thickness=-1)
        h, w, c = img.shape
        wCam = 16 * constHd
        hCam = 9 * constHd
        if index == 4:
            # print(disRatio)
            xSize = disRatio * 14
            ySize = disRatio * 8
            xtemp = x - xSize // 2
            ytemp = y - ySize // 2
            # print(xtemp, ytemp)
            cv2.rectangle(recognize, (xtemp, ytemp), (xSize + xtemp, ySize + ytemp), gray, thickness=20)
        lx = int(np.interp(x - (1280 - wCam) // 2, (0, wCam), (0, wScr)))
        ly = int(np.interp(y - (720 - hCam) // 2, (0, hCam), (0, hScr)))
        return lx, ly

    def paintPoint(lx, ly, color, radius):
        cv2.circle(img, (lx, ly), radius=radius, color=color, thickness=-1)

    def distance_cal(x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))

    def checkAccuracy(img, test):
        temp = 0
        checkTemp = 0
        for i in range(0, 1920):
            for j in range(201, 1080):
                if img[j][i][0] != 255 or img[j][i][1] != 255 or img[j][i][2] != 255:
                    checkTemp = checkTemp + 1
                    if test[j][i][0] == 0 and test[j][i][1] == 0 and test[j][i][2] == 0:
                        temp = temp + 1
        return 100 - temp / checkTemp * 100

    def generateTask(idx):
        if idx == 1:
            cv2.circle(img, (960, 652), radius=310, color=gray, thickness=10)
        elif idx == 2:
            cv2.rectangle(img, (652, 320), (1282, 950), gray, thickness=20)
        else:
            cv2.circle(img, (425, 354), radius=102, color=gray, thickness=10)
            cv2.rectangle(img, (881, 541), (1460, 970), gray, thickness=20)
            cv2.line(img, (748, 540), (1565, 540), gray, thickness=20)
            cv2.line(img, (1150, 263), (748, 540), gray, thickness=20)
            cv2.line(img, (1150, 263), (1565, 540), gray, thickness=20)
            cv2.rectangle(img, (1170, 767), (1289, 967), gray, thickness=20)
            cv2.rectangle(img, (967, 609), (1092, 731), gray, thickness=10)
            cv2.line(img, (1032, 608), (1032, 728), gray, thickness=10)
            cv2.line(img, (1032, 608), (1032, 728), gray, thickness=10)
            cv2.line(img, (972, 669), (1090, 669), gray, thickness=10)
            cv2.line(img, (572, 343), (772, 343), gray, thickness=10)
            cv2.line(img, (425, 507), (425, 507 + 772 - 572), gray, thickness=10)
            cv2.line(img, (542, 456), (648, 540), gray, thickness=10)



    def renderSizeBar(sizeBar):
        if sizeBar == 0:
            cv2.circle(img, (1778, 282), radius=penSize // 2, color=mainColor, thickness=-1)
        elif sizeBar == 1:
            cv2.circle(img, (1778, 456), radius=penSize // 2, color=mainColor, thickness=-1)
        elif sizeBar == 2:
            cv2.circle(img, (1778, 696), radius=penSize // 2, color=mainColor, thickness=-1)
        elif sizeBar == 3:
            cv2.circle(img, (1778, 979), radius=penSize // 2, color=mainColor, thickness=-1)

    folderPath = "./art/Sizebar"
    myList = os.listdir(folderPath)
    overlayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        overlayList.append(image)
    header = cv2.imread(f"./art/Header/1{lang}.png")
    taskBar = cv2.imread(f'./art/TaskBar{lang}.png')

    folderPath = "./art/Point"
    myList = [f'0{lang}.png', f'1{lang}.png', f'2{lang}.png', f'3{lang}.png', f'4{lang}.png', f'5{lang}.png', f'6{lang}.png', f'7{lang}.png', f'8{lang}.png', f'9{lang}.png', f'10{lang}.png']
    pointList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}')
        pointList.append(image)
    # print(len(pointList))

    # print(len(overlayList))

    # color discribtion
    red = (244, 56, 73)
    white = (248, 116, 74)
    black = (0, 0, 0)
    blue = (38, 149, 211)
    yellow = (255, 186, 49)
    green = (66, 178, 90)
    gray = (196, 196, 196)

    # set camera
    frameWidth = 1280
    frameHeight = 720
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)

    # set hand recognize
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    sm = 3
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    cTime = 0
    pTime = 0
    # set properties color
    penSize = 20
    mainColor = black
    mainHeader = 0
    finger = []
    statusTaskBar = False
    TaskManager = 0
    statusAccuracy = False
    checkStatusAccuracy = False
    percent = 0
    sizeBar = 5
    percent = 0
    pointCheck = False
    recordPaint = False
    recordIdx = 0
    image_canvas = np.zeros((1080, 1920, 3), np.uint8)
    background = cv2.imread('./art/background.png')
    checkBar = cv2.imread(f'./art/checkBar{lang}.png')

    statusTaskBarNow = False
    statusTaskBarPre = False

    with mpHands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.9) as hands:
        while cap.isOpened():
            success, recognize = cap.read()
            img = background
            # image_canvas = testBackGround

            if TaskManager != 0:
                generateTask(TaskManager)
            checkDiff1 = img
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            if sizeBar != -1:
                img[0:1080, 0:1920] = overlayList[5]
                renderSizeBar(sizeBar)
            if TaskManager != 0:
                generateTask(TaskManager)
            if recordPaint == True:
                if recordIdx >= len(finger) - 1:
                    recordPaint = False
                    recordIdx = 0
                for idx in range(0, recordIdx):
                    i = finger[idx]
                    y = finger[idx + 1]
                    if i[4] == True and y[4] == True:
                        cv2.line(image_canvas, (i[0], i[1]), (y[0], y[1]), i[2], i[3])
                recordIdx += 1
            else:
                for idx in range(0, len(finger) - 1):
                    i = finger[idx]
                    y = finger[idx + 1]
                    if i[4] == True and y[4] == True:
                        cv2.line(image_canvas, (i[0], i[1]), (y[0], y[1]), i[2], i[3])
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            image_canvas = cv2.cvtColor(image_canvas, cv2.COLOR_BGR2RGB)

            img_gray = cv2.cvtColor(image_canvas, cv2.COLOR_BGR2GRAY)
            _, imginv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)
            imginv = cv2.cvtColor(imginv, cv2.COLOR_GRAY2BGR)
            img = cv2.bitwise_and(img, imginv)
            img = cv2.bitwise_or(img, image_canvas)
            checkDiff2 = image_canvas
            img[0:1080, 0:258] = checkBar


            img[0:201, 0:1920] = header
            if statusTaskBar == True:
                img[0:1080, 0:298] = taskBar
            recognize = cv2.flip(recognize, 1)
            imgRGB = cv2.cvtColor(recognize, cv2.COLOR_BGR2RGB)
            if pointCheck == True and percent != 0:
                passPoint = pointList[int(percent) // 10 + 1]
                img[0:1080, 0:1920] = passPoint

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
                    paintPoint(xPoint, yPoint, mainColor, round(penSize / 2))
                    # img[0:126, 0:126] = paintBrush
                    range8_4 = distance_cal(x8, y8, x4, y4)

                    x5, y5 = getPoint(handLms, 5)
                    x0, y0 = getPoint(handLms, 0)
                    # paintPoint(x0, y0, mainColor, round(penSize / 2))
                    # paintPoint(x5, y5, mainColor, round(penSize / 2))

                    range0_5 = distance_cal(x0, y0, x5, y5)
                    # print(range0_5, range8_4)

                    ratio = range0_5 * 0.33
                    # print(range8_4)
                    disRatio = range8_4

                    status = False
                    if ratio > range8_4:
                        status = True
                    # # print(status, ratio, range8_4)
                    # print('long: ', range0_5)
                    # print('short', range8_4)

                    statusTaskBarPre = statusTaskBarNow

                    if status:
                        if 1490 <= xPoint <= 1617 and 48 <= yPoint <= 153:
                            mainColor = black
                        elif 1219 <= xPoint <= 1345 and 39 <= yPoint <= 163:
                            mainColor = blue
                        elif 1009 <= xPoint <= 1135 and 39 <= yPoint <= 163:
                            mainColor = green
                        elif 799 <= xPoint <= 925 and 39 <= yPoint <= 163:
                            mainColor = yellow
                        elif 589 <= xPoint <= 715 and 39 <= yPoint <= 163:
                            mainColor = red
                        elif 379 <= xPoint <= 505 and 39 <= yPoint <= 163:
                            mainColor = white
                        elif 1779 <= xPoint <= 1884 and 48 <= yPoint <= 153:
                            cv2.destroyAllWindows()
                            return
                        if sizeBar != -1:
                            if 1708 <= xPoint <= 1851 and 209 <= yPoint <= 209 + 1851 - 1708:
                                penSize = 20
                                sizeBar = 0
                            if 1708 <= xPoint <= 1851 and 381 <= yPoint <= 381 + 1851 - 1708:
                                penSize = 35
                                sizeBar = 1
                            if 1708 <= xPoint <= 1851 and 592 <= yPoint <= 592 + 1851 - 1708:
                                penSize = 55
                                sizeBar = 2
                            if 1708 <= xPoint <= 1851 and 907 <= yPoint <= 907 + 1851 - 1708:
                                penSize = 72
                                sizeBar = 3
                        if 739 <= xPoint <= 1180 and 814 <= yPoint <= 957 and pointCheck == True:
                            finger = []
                            image_canvas = np.zeros((1080, 1920, 3), np.uint8)
                            pointCheck = False
                            percent = 0
                    if yPoint > 200 and 258 <= xPoint <= 1658:
                        if finger and finger[-1][4] == False and status == False:
                            continue
                        finger.append((xPoint, yPoint, mainColor, penSize, status))
                    if status == True and  102 <= xPoint <= 255  and 26 <= yPoint <= 184:
                        statusTaskBarNow = True
                        print(statusTaskBarPre, statusTaskBarNow)
                        if (statusTaskBarNow == True and statusTaskBarNow != statusTaskBarPre):
                            if statusTaskBar == False:
                                statusTaskBar = True
                            else:
                                statusTaskBar = False
                    else:
                        statusTaskBarNow = False

                    if status == True and statusTaskBar == True:
                        if 32 <= xPoint <= 270 and 258 <= yPoint <= 447:
                            finger = []
                            image_canvas = np.zeros((1080, 1920, 3), np.uint8)
                            TaskManager = 1
                            statusTaskBar = False
                        if 32 <= xPoint <= 270 and 545 <= yPoint <= 734:
                            finger = []
                            image_canvas = np.zeros((1080, 1920, 3), np.uint8)
                            TaskManager = 2
                            statusTaskBar = False
                        if 32 <= xPoint <= 270 and 833 <= yPoint <= 1022:
                            finger = []
                            image_canvas = np.zeros((1080, 1920, 3), np.uint8)
                            TaskManager = 3
                            statusTaskBar = False
                    if statusTaskBar == False and status == True and pointCheck == False:
                        if 54 <= xPoint <= 196 and 242 <= yPoint <= 421:
                            recordPaint = True
                            image_canvas = np.zeros((1080, 1920, 3), np.uint8)
                        if 54 <= xPoint <= 204 and 462 <= yPoint <= 641:
                            finger = []
                            image_canvas = np.zeros((1080, 1920, 3), np.uint8)
                            TaskManager = 0
                        if 54 <= xPoint <= 196 and 680 <= yPoint <= 843:
                            finger = []
                            image_canvas = np.zeros((1080, 1920, 3), np.uint8)
                        if finger and 54 <= xPoint <= 179 and 889 <= yPoint <= 1021 and TaskManager != 0:
                            checkStatusAccuracy = True


            if statusAccuracy == True and len(finger) > 0:
                percent = checkAccuracy(checkDiff1, checkDiff2)
                pointCheck = True
                print(percent)
                statusAccuracy = False
                checkStatusAccuracy = 0

            if checkStatusAccuracy == True:
                statusAccuracy = True
                checkStatusAccuracy = False
                img = cv2.imread(f'./art/loading{lang}.png')

            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(img, "FPS= " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)
            cv2.imshow("Paint", img)
            # cv2.imshow("test", recognize)
            # cv2.imshow("hidden", image_canvas)
            if cv2.waitKey(1) == 27:
                break
# cv2.waitKey(100000000);
# hocVe()



