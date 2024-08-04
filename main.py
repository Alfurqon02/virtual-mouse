import cv2
import mediapipe as mp
import pyautogui
import time

cam = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_y = 0
ALT_TAB_THRESHOLD = 0.5
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            positions = {}
            for id, landmark in enumerate(landmarks):
                x= int(landmark.x*frame_width)+10
                y= int(landmark.y*frame_height)+10
                # ANCHOR MOVE MOUSE
                if id == 4:
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                    pyautogui.moveTo(index_x, index_y)
                if id == 8:
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    if abs(index_y - thumb_y) < 40: 
                        pyautogui.click()
                        pyautogui.sleep(1)
                # if id == 12:
                #     thumb_x = screen_width/frame_width*x
                #     thumb_y = screen_height/frame_height*y
                #     if abs(index_y - thumb_y) < 40: 
                #         pyautogui.keyDown('alt')
                #         print('press')
                #         pyautogui.sleep(1)
                #         if id == 16:
                #             thumb_x = screen_width/frame_width*x
                #             thumb_y = screen_height/frame_height*y
                #             if abs(index_y - thumb_y) < 40: 
                #                 pyautogui.press('tab') 
                #                 pyautogui.sleep(1)
                #     pyautogui.keyUp('alt')
                #     print('notPress')
                # ANCHOR ALT + TAB
                if id == 16 and index_x is not None and index_y is not None:
                    ring_x = screen_width / frame_width * x
                    ring_y = screen_height / frame_height * y
                    if abs(index_y - ring_y) < 40:
                        if alt_tab_start_time is None:
                            alt_tab_start_time = time.time()
                        elif time.time() - alt_tab_start_time > ALT_TAB_THRESHOLD:
                            pyautogui.keyDown('alt')
                            pyautogui.press('tab')
                            pyautogui.keyUp('alt')
                            alt_tab_start_time = None
                    else:
                        alt_tab_start_time = None
                # ANCHOR DOUBLE CLICK
                if id == 20:
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    if abs(index_y - thumb_y) < 40: 
                        pyautogui.click(clicks=2, interval=0.25)
                        pyautogui.sleep(1)
                        
    cv2.imshow('camera', frame)
    cv2.waitKey(1)