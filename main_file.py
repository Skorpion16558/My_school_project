import subprocess
import tkinter as tk
import io, cv2
import base64 as bs
from PIL import Image as im
import numpy as np
cup = cv2.VideoCapture(0)
faces = cv2.CascadeClassifier("faces_blur.xml")

global image_str
while True:
    suc, img = cup.read()
    global roi
    result = faces.detectMultiScale(img, scaleFactor=1.5, minNeighbors=3)
    for (x, y, w, h) in result:
        roi = img[y:y + h + 30, x:x + w + 30]
    try:
        cv2.imshow('result', roi)
        if cv2.waitKey(1) & 0xFF == ord('w'):
            cv2.imwrite('image.png', img)
            cup.release()
            cv2.destroyAllWindows()
            break
    except NameError:
        print()
