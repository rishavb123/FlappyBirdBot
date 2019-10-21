import pyautogui
import time
import numpy as np
import cv2
from PIL import ImageGrab

rect = pyautogui.locateOnScreen('./flappy_bird.png')
box = (rect[0], rect[1], rect[0] + rect[2], rect[1] + 2 * rect[3])

while True:
    img = ImageGrab.grab()
    # img = img.crop(box)
    img = np.array(img.getdata(), dtype='uint8').reshape((img.size[1], img.size[0],3))
    cv2.imshow('window', img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

