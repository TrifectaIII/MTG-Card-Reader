## Compare2Set - Dakota Madden-Fong May 2018
# Compares an image to a library of images from a set
from urllib import request as urlreq
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import os
from fetchSetImages import fetchSetImages
from processSetImages import processSetImages

class compare2set:
    def __init__(self, setcode):
    # User Provides the SetCode
        (self.imgdict, self.namedict) = fetchSetImages(setcode)# Get name dictionary and image dictionary from fetchSetImages
        (self.keypdict, self.desdict, self.imgdict2g, self.sift) = processSetImages(self.imgdict)# Get keypoints dictionaries and SIFT onject from processSetImages
    
        
        ##Matcher Steup
        # create OpenCV keypoint matcher object
        self.bf = cv2.BFMatcher()
        print(setcode,'Set loaded')
        
    # Compare an image to the card images and identify one as a match
    def compareimg(self, imageinput):
        #accepts the webcam image as input
        try:
            camimg = imageinput
            height, width, _ = camimg.shape
            while (width > 1000):
                new_width = int(width/2)
                new_height = int(height/2)
                camimg = cv2.resize(camimg, (new_width,new_height) )
                height, width, _ = camimg.shape
            camimg2g = cv2.cvtColor(camimg, cv2.COLOR_BGR2GRAY)
        except:
            raise IOError('Cannot properly process input image')
            
        # compute keypoints for the webcam image
        (kpr, desr) = self.sift.detectAndCompute(camimg2g,None)    
        
        printsimages = []
        printsimages2g = []
        printskp = []
        printsdes = []
        printsmatches = []
        printsmatcheslen = []
        printsnames = []
        
        #Loop through images to compare each one
        for key in self.imgdict:
            printsimages.append(self.imgdict[key])
            printsimages2g.append(self.imgdict2g[key])
            kp = self.keypdict[key]
            des = self.desdict[key]
            printskp.append(kp)
            printsdes.append(des)
            printsnames.append(self.namedict[key])
            
            rawmatches = self.bf.knnMatch(desr,des, k=2)# find 2 nearest negihbor keypoint matches
            matches = []
            for m,n in rawmatches:
                if m.distance < 0.75*n.distance:# use ratio test to determine if match is successful
                    matches.append([m])
            printsmatches.append(matches)
            printsmatcheslen.append(len(matches))
            
        
        ## Find Best Match and Display
        for x in range(3):
            bestmatch = np.argmax(printsmatcheslen)# identify correct card by number of successful matches
            print("Match",(x+1),',',printsnames[bestmatch],':','with',printsmatcheslen[bestmatch],'feature matches')
            if x == 0:
                bestmatchname = printsnames[bestmatch]
                bestmatchimg = printsimages[bestmatch]
            printsmatcheslen[bestmatch] = -math.inf
        #OpenCV GUI Code--------------------------------------------------------
        # cv2.namedWindow("Best Match: "+bestmatchname)
        # cv2.imshow("Best Match: "+bestmatchname, bestmatchimg)
        # cv2.waitKey()
        # plt.imshow(test),plt.show()
        #-----------------------------------------------------------------------
        cv2.destroyAllWindows()
        bestmatchimg = cv2.resize(bestmatchimg, (223,311))
        return (bestmatchname, bestmatchimg)# return the name and image of the identified card