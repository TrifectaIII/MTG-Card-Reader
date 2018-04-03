## Compare2Set - Dakota Madden-Fong

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
    # User Provided Info
    #--------------------------------------------------------------------
        (self.imgdict, self.namedict) = fetchSetImages(setcode)
        (self.keypdict, self.desdict, self.imgdict2g) = processSetImages(self.imgdict)
        #--------------------------------------------------------------------
        
        ## Surf Setup
        self.sift = cv2.xfeatures2d.SIFT_create()
        #surf.setHessianThreshold(400)
        #surf.setExtended(True)
        
        ##Matcher Steup
        self.bf = cv2.BFMatcher()
        print(setcode,'Set loaded')
        
    def compareimg(self, imageinput):
        try:
            camimg = imageinput
            camimg2g = cv2.cvtColor(camimg, cv2.COLOR_BGR2GRAY)
        except:
            raise NameError('Cannot properly process input image')
            
        (kpr, desr) = self.sift.detectAndCompute(camimg2g,None)    
        
        printsimages = []
        printsimages2g = []
        printskp = []
        printsdes = []
        printsmatches = []
        printsmatcheslen = []
        printsnames = []
        
        
        for key in self.imgdict:
            printsimages.append(self.imgdict[key])
            printsimages2g.append(self.imgdict2g[key])
            kp = self.keypdict[key]
            des = self.desdict[key]
            printskp.append(kp)
            printsdes.append(des)
            printsnames.append(self.namedict[key])
            
            rawmatches = self.bf.knnMatch(desr,des, k=2)
            matches = []
            for m,n in rawmatches:
                if m.distance < 0.75*n.distance:
                    matches.append([m])
            printsmatches.append(matches)
            printsmatcheslen.append(len(matches))
            
        
        ## Find Three Best Matches and Display
        print("\n" * 100)
        #print(printsmatcheslen)
        for x in range(3):
            bestmatch = np.argmax(printsmatcheslen)
            print("Match",(x+1),',',printsnames[bestmatch],':','with',printsmatcheslen[bestmatch],'feature matches')
            if x == 0:
                bestmatchname = printsnames[bestmatch]
                bestmatchimg = printsimages[bestmatch]
            printsmatcheslen[bestmatch] = -math.inf
        # cv2.namedWindow("Best Match: "+bestmatchname)
        # cv2.imshow("Best Match: "+bestmatchname, bestmatchimg)
        # cv2.waitKey()
        # plt.imshow(test),plt.show()
        cv2.destroyAllWindows()
        return bestmatchname