import numpy as np
import cv2
import time,os,sys
import pandas as pd

def color(filepath):
    image = cv2.imread(filepath)

    boundaries = {'yellow':( [0,102,102],[153,255,255]),
                  'green': ( [0,85,9], [45,252,65]),
                  'white':([225,228,255],[255,255,255]),
                  'purple':([130,0,75], [250,230,230]),
                  'pink':([133,21,199], [203,192,255])}

    for color, pair in boundaries.items():

        lower, upper = pair

        lower = np.array(lower, dtype='uint8')
        upper = np.array(upper, dtype='uint8')

        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask=mask)

        # cv2.imshow('test', mask)
        cv2.imshow(color, np.hstack([image, output]))
        cv2.waitKey(0)


color('test_image.PNG')
