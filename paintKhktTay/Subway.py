import time

import cv2
import mediapipe as mp
# from pynput.keyboard import Key, Controller
import math
import pyautogui
import webbrowser

def Subway():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose
    # keyboard = Controller()

    cap = cv2.VideoCapture(0)

    cap.set(3, 1280)

    cap.set(4, 720)
    #set thuoc tinh
    isRight = False
    isRightPre = False
    isLeft = False
    isLeftPre = False
    isDown = False
    isDownPre = False
    isUp = False
    isUpPre = False
    distance = 200
    webbrowser.open_new_tab("https://www.trochoi.net/tr%C3%B2+ch%C6%A1i/subway-surfers.html")

    def Convert(normalized_x, normalized_y, image_width, image_height):
        x_px = min(math.floor(normalized_x * image_width), image_width - 1)
        y_px = min(math.floor(normalized_y * image_height), image_height - 1)
        return x_px, y_px


    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)
            cv2.line(image, (300, 0), (300, 1024), (0, 0, 0), 3)
            cv2.line(image, (1280 - 300, 0), (1280 - 300, 1024), (0, 0, 0), 3)
            cv2.line(image, (0, 720 - 200), (1280, 720 - 200), (0, 0, 0), 3)
            cv2.line(image, (0, 300), (1280, 300), (0, 0, 0), 3)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
            image_rows, image_cols, _ = image.shape
            if results.pose_landmarks:
                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    if (idx == 22 and landmark.visibility > 0.7):
                        x,y = Convert(landmark.x, landmark.y, image_cols, image_rows)
                        isRightPre = isRight
                        if (x < 300): isRight = True
                        else: isRight = False
                        if (isRight and isRight != isRightPre):
                            print('Right');
                            # keyboard.press(Key.right)
                            pyautogui.press('right')
                            # pyautogui.drag(distance, 0, duration=0.2)
                            # pyautogui.moveTo(1920 / 3, 1080 / 2)
                    if (idx == 21):
                        x,y = Convert(landmark.x, landmark.y, image_cols, image_rows)
                        isLeftPre = isLeft
                        if (x > 1280 - 300): isLeft = True
                        else: isLeft = False
                        if (isLeft and isLeft != isLeftPre):
                            print('Left');
                            # keyboard.press(Key.left)
                            # time.sleep(0.2)
                            pyautogui.press('left')
                            # pyautogui.drag(-distance, 0, duration=0.2)
                            # pyautogui.moveTo(1920 / 3, 1080 / 2)
                    if (idx == 12):
                        x,y = Convert(landmark.x, landmark.y, image_cols, image_rows)
                        isDownPre = isDown
                        isUpPre = isUp
                        if (y > 720 - 200): isDown = True
                        else: isDown = False
                        if (isDown and isDown != isDownPre):
                            print('Down');
                            # keyboard.press(Key.down)
                            # time.sleep(0.2)
                            pyautogui.press('down')
                            # pyautogui.drag(0, distance, duration=0.2)
                            # pyautogui.moveTo(1920 / 3, 1080 / 2)
                        if (y < 230): isUp = True
                        else: isUp = False
                        if (isUp and isUp != isUpPre):
                            print('Up');
                            # keyboard.press(Key.up)
                            # time.sleep(0.2)
                            pyautogui.press('up')
                            isDown = False
                            # pyautogui.drag(0, -distance, duration=0.2)
                            # pyautogui.moveTo(1920 / 3, 1080 / 2)
            cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
