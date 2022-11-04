import cv2
import mediapipe as mp
import time
import math
import numpy as np
import csv
import random
import cv2

def HocToan(lang):
    frameWidth = 1280
    frameHeight = 720
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    mpFaceMesh = mp.solutions.face_mesh
    mpDraw = mp.solutions.drawing_utils
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)

    pTime = 0
    cTime = 0

    #set color
    black = (0, 0, 0)
    orange = (232, 149, 9)
    green = (50, 194, 26)
    penSize = 20

    constHd = 35
    wScr, hScr = 1920, 1080

    sm = 3
    plocX, plocY = 0, 0
    clocX, clocY = 0, 0

    xPosButton = 124
    yPosButton = 661
    hButton = 85
    wButton = 85
    disButton = 66

    class Button():
        def __init__(self, pos, text, size = [85, 85]):
            self.pos = pos
            self.text = text
            self.size = size
            self.enabled = 1
            self.time = 0

    with open('./art/mathQuest.csv') as f:
        reader = csv.reader(f)
        tempQuestion = [row for row in reader]
    questions = tempQuestion

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

    def calcAns(quest):
        questNow = ''
        ansQuestNow = int(quest[0])
        for i in range(0, len(quest)):
            temp = quest[i]
            questNow += temp
            if temp == ' +':
                ansQuestNow += int(quest[i + 1])
            elif temp == ' x':
                ansQuestNow *= int(quest[i + 1])
            elif temp == ' -':
                ansQuestNow -= int(quest[i + 1])
            elif temp == ' /':
                ansQuestNow /= int(quest[i + 1])
        return  questNow, ansQuestNow


    def paintPoint(lx, ly, color, radius):
        cv2.circle(img, (lx, ly), radius=radius, color=color, thickness=1)

    def distance_cal(x1, y1, x2, y2):
        return int(math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2)))

    def swap_random(seq):
        idx = range(len(seq))
        i1, i2 = random.sample(idx, 2)
        seq[i1], seq[i2] = seq[i2], seq[i1]

    def clearSpace(s):
        pass

    def renderNumber():
        cQr = 0
        cQc = 1
        buttonNumber = []
        tempNumber = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        for idx in tempNumber:
            if idx == ' ':
                continue
            cQr += 1
            if cQr > 10:
                cQr = 1
                cQc = 2
            buttonNumber.append(Button([xPosButton + (cQr - 1) * (disButton + 85), yPosButton + (cQc - 1) * (49 + 85)], idx))
        return buttonNumber

    def renderQuest(str, y, fontScale, fontFitness):
        (textWidth, textHeight), baseline = cv2.getTextSize(str, cv2.FONT_HERSHEY_SIMPLEX, 3, 2)
        image = cv2.putText(img, str, [700 - textWidth, y], cv2.FONT_HERSHEY_SIMPLEX, 3, black, 2, cv2.LINE_AA)

    def calcAns(quest):
        questNow = ''
        ansQuestNow = int(quest[0])
        for i in range(0, len(quest)):
            temp = quest[i]
            questNow += temp
            print(temp)
            if temp == ' +':
                ansQuestNow += int(quest[i + 1])
                print(i, ansQuestNow)
            elif temp == ' x':
                ansQuestNow *= int(quest[i + 1])
                print(i, ansQuestNow)
            elif temp == ' -':
                ansQuestNow -= int(quest[i + 1])
                print(i, ansQuestNow)
            elif temp == ' /':
                ansQuestNow /= int(quest[i + 1])
                print(i, ansQuestNow)
        return  questNow, ansQuestNow

    buttonNumber = renderNumber()
    for i in questions:
        swap_random(questions)
    showWindow = True
    resString = ''
    questNumber = 0
    questNumberNow = 0
    score = 0
    pointOverlay = False
    popUpFalse = False
    popUpTrue = False
    background = cv2.imread(f'./art/HocToan{lang}.png')
    ansQuestNow = 0
    questNow = ''
    while cap.isOpened():
        img = background
        if showWindow == False:
            cv2.destroyAllWindow()
            showWindow = True
            time.sleep(2)
        success, recognize = cap.read()
        if not success:
            continue
        recognize = cv2.flip(recognize, 1)
        imgRGB = cv2.cvtColor(recognize, cv2.COLOR_BGR2RGB)
        if questNumber == questNumberNow:
            questNumber += 1
            questNow, ansQuestNow = calcAns(questions[questNumberNow])
            questNow = questNow.split();
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        for idx in buttonNumber:
            if idx != 0 and time.time() - idx.time > 1:
                idx.enabled = 1
        for idx in buttonNumber:
            if idx.enabled == 1:
                cv2.rectangle(img, idx.pos, [idx.pos[0] + wButton, idx.pos[1] + hButton], orange, 4)
            else:
                cv2.rectangle(img, idx.pos, [idx.pos[0] + wButton, idx.pos[1] + hButton], (50, 50, 50), -1)
            image = cv2.putText(img, idx.text, [idx.pos[0] + (wButton - 40) // 2, idx.pos[1] + (hButton + 30) // 2], cv2.FONT_HERSHEY_SIMPLEX, 2, black, 2, cv2.LINE_AA)


        # render quest
        print(questNow)

        renderQuest(questNow[0], 100, 3, 2)
        renderQuest(questNow[2], 220, 3, 2)
        renderQuest(resString, 365, 3, 2)
        image = cv2.putText(img, questNow[1], [560, 150], cv2.FONT_HERSHEY_SIMPLEX, 2, black, 2, cv2.LINE_AA)
        image = cv2.putText(img, str(score), [1655, 743], cv2.FONT_HERSHEY_SIMPLEX, 5, green, 7, cv2.LINE_AA)



        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if popUpTrue == True:
            img[42:228, 1107:1652] = cv2.imread(f'./art/trueAnswer{lang}.png')
        if popUpFalse == True:
            img[42:228, 1107:1652] = cv2.imread(f'./art/wrongAnswer{lang}.png')
        if pointOverlay == True:
            img = cv2.imread(f'./art/pointTiengViet{lang}.png')
            textsize = cv2.getTextSize(str(score), cv2.FONT_HERSHEY_SIMPLEX, 3, 5)[0]
            print(textsize[0])
            image = cv2.putText(img, str(score), [918 - textsize[0], 746], cv2.FONT_HERSHEY_SIMPLEX, 3, green, 5, cv2.LINE_AA)
        results = faceMesh.process(imgRGB)
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                x8, y8 = getPoint(face_landmarks, 0)
                x4, y4 = getPoint(face_landmarks, 16)
                xPoint = (x8 + x4) // 2
                yPoint = (y8 + y4) // 2
                xPoint = clocX = plocX + (xPoint - plocX) // sm
                yPoint = clocY = plocY + (yPoint - plocY) // sm
                plocX, plocY = clocX, clocY
                paintPoint(xPoint, yPoint, (0, 0, 0), round(penSize / 2))
                # img[0:126, 0:126] = paintBrush
                range8_4 = distance_cal(x8, y8, x4, y4)

                x5, y5 = getPoint(face_landmarks, 69)
                x0, y0 = getPoint(face_landmarks, 291)
                # paintPoint(x0, y0, mainColor, round(penSize / 2))
                # paintPoint(x5, y5, mainColor, round(penSize / 2))

                range0_5 = distance_cal(x0, y0, x5, y5)
                # print(range0_5, range8_4)

                status = False
                if range0_5 > 250:
                    ratio = math.sqrt((range0_5 - 250) / 0.012)
                    if ratio < range8_4:
                        # continue
                        status = True

                if status == True and pointOverlay == True:
                    if 739 <= xPoint <= 1180 and 814 <= yPoint <= 957:
                        pointOverlay = False
                        questNumberNow = 0
                        questNumber = 0
                        swap_random(questions)
                        score = 0
                        popUpFalse = False
                        popUpTrue = False

                if status == True and pointOverlay == False:
                    for idx in buttonNumber:
                        if idx.pos[0] <= xPoint <= idx.pos[0] + wButton and idx.pos[1] <= yPoint <= idx.pos[1] + hButton and idx.enabled == 1:
                            resString += idx.text
                            idx.enabled = 0
                            idx.time = time.time()
                            popUpFalse = False
                            popUpTrue = False
                    if 198 <= xPoint <= 484 and 402 <= yPoint <= 503:
                        resString = ''
                        for idx in buttonNumber:
                            idx.enabled = 1
                    if 577 <= xPoint <= 1028 and 402 <= yPoint <= 503 and len(resString) > 0:
                        if int(resString) == ansQuestNow:
                            score += 10
                            popUpTrue = True
                            popUpFalse = False
                        else:
                            popUpFalse = True
                            popUpTrue = False
                        questNumberNow += 1
                        if questNumberNow == len(questions):
                            pointOverlay = True
                            questNumberNow = 1
                            questNumber = 2
                        resString = ''

                    if 1741 <= xPoint <= 1846 and 113 <= yPoint <= 218:
                        cv2.destroyAllWindows()
                        return

        # Write frame rate
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, "FPS= " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 0), 1)


        # if showWindow == True:
        cv2.imshow('image', img)
        # if status == True:
        #     cv2.destroyallwindows()
        if cv2.waitKey(1) == 27:
            break

# HocToan()