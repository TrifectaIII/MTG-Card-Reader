## processSetImages - Dakota Madden-Fong May 2018

# Calculates SIFT features and converts all images in a dictionary of cv2 images
# to grayscale. 

# Returns dictionaries of keypoints, desciptions, and grayscale images keyed on
# mtgjson unique ids, as well as the SIFT object itself

import numpy as np
import cv2
import os

def processSetImages(imgdict):
    
    # create SIFT object
    sift = cv2.xfeatures2d.SIFT_create()
    
    keypdict = dict()
    desdict = dict()
    imgdict2g = dict()
    
    for key in imgdict:# calculate keypoints for all card images in the set
        img2g = cv2.cvtColor(imgdict[key], cv2.COLOR_BGR2GRAY)
        imgdict2g[key] = img2g
        (kp, des) = sift.detectAndCompute(img2g,None)
        keypdict[key] = kp
        desdict[key] = des
    # pass along everything including the sift object
    return(keypdict, desdict, imgdict2g, sift)