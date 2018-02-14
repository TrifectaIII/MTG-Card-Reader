import numpy as np
import cv2
from mtg_cards import card_set_json as cardset
import os

def processSetImages(setdict):
    
    sift = cv2.xfeatures2d.SIFT_create()
    
    keypdict = dict()
    desdict = dict()
    setdict2g = dict()
    
    for key in setdict:
        img2g = cv2.cvtColor(setdict[key], cv2.COLOR_BGR2GRAY)
        setdict2g[key] = img2g
        (kp, des) = sift.detectAndCompute(img2g,None)
        keypdict[key] = kp
        desdict[key] = des
    
    return(keypdict, desdict, setdict2g)