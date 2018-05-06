## processSetImages - Dakota Madden-Fong

# Calculates SIFT features and converts all images in a dictionary of cv2 images
# to grayscale. 

# Returns dictionaries of keypoints, desciptions, and grayscale images keyed on
# mtgjson unique ids

import numpy as np
import cv2
import os

def processSetImages(imgdict):
    
    sift = cv2.xfeatures2d.SIFT_create()
    
    keypdict = dict()
    desdict = dict()
    imgdict2g = dict()
    
    for key in imgdict:
        img2g = cv2.cvtColor(imgdict[key], cv2.COLOR_BGR2GRAY)
        imgdict2g[key] = img2g
        (kp, des) = sift.detectAndCompute(img2g,None)
        keypdict[key] = kp
        desdict[key] = des
    
    return(keypdict, desdict, imgdict2g, sift)