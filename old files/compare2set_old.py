## Compare2Set - Dakota Madden-Fong

from urllib import request as urlreq
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import os

def compare2set(imageinput):
# User Provided Info
#--------------------------------------------------------------------
    try:
        camimg = imageinput
        camimg2g = cv2.cvtColor(camimg, cv2.COLOR_BGR2GRAY)
    except:
        raise NameError('Cannot properly process input image')
    
    files = os.listdir('./Set2')
    files.remove('cropped')
    set_images = [];
    set_names = [];
    for name in files:
        set_images.append(cv2.imread('Set2/'+name))
        set_names.append(name[:-4])
    #--------------------------------------------------------------------
    
    ## Surf Setup
    surf = cv2.xfeatures2d.SIFT_create()
    #surf.setHessianThreshold(400)
    #surf.setExtended(True)
    (kpr, desr) = surf.detectAndCompute(camimg2g,None)
    ## Orb Setup
    #orb = cv2.ORB_create()
    #kpr = orb.detect(camimg2g,None)
    #kpr, desr = orb.compute(camimg2g, kpr)
    
    ##Matcher Steup
    # bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    
    bf = cv2.BFMatcher()
    
    printsimages = []
    printsimages2g = []
    printskp = []
    printsdes = []
    printsmatches = []
    printsmatcheslen = []
    
    ## Fetch Card Images and Match Features
    for img in set_images:
        printsimages.append(img)
        img2g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        printsimages2g.append(img2g)
        
        # Surf ---------------------------------------------------------------------
        (kp, des) = surf.detectAndCompute(img2g,None)
        
        # Orb ----------------------------------------------------------------------
        # kp = orb.detect(img2g,None)
        # kp, des = orb.compute(img2g, kp)
    
        printskp.append(kp)
        printsdes.append(des)
    
        # BF Only ------------------------------------------------------------------
        # matches = bf.match(desr,des)
        # matches = sorted(matches, key = lambda x:x.distance)
        # printsmatches.append(matches)
        # printsmatcheslen.append(len(matches))
        
        # Ratio Test ---------------------------------------------------------------
        rawmatches = bf.knnMatch(desr,des, k=2)
        matches = []
        for m,n in rawmatches:
            if m.distance < 0.75*n.distance:
                matches.append([m])
        printsmatches.append(matches)
        printsmatcheslen.append(len(matches))
        
    
    ## Find Three Best Matches and Display
    print("\n" * 100)
    print(printsmatcheslen)
    for x in range(3):
        bestmatch = np.argmax(printsmatcheslen)
        print("Match",(x+1),',',set_names[bestmatch],':','with',printsmatcheslen[bestmatch])
        test = camimg2g
        
        # test = cv2.drawMatches(camimg2g,kpr,printsimages2g[bestmatch],printskp[bestmatch],printsmatches[bestmatch][:30],test,flags=2)
        
        #test = cv2.drawMatchesKnn(camimg2g,kpr,printsimages2g[bestmatch],printskp[bestmatch],printsmatches[bestmatch][:30],test,flags=2)
        if x == 0:
            cv2.namedWindow(("Match "+str(x+1)))
            #cv2.imshow(("Match "+str(x+1)), test )
            cv2.imshow(("Match "+str(x+1)), printsimages[bestmatch] )
            cv2.waitKey()
    #    plt.imshow(test),plt.show()
        printsmatcheslen[bestmatch] = -math.inf
    
    cv2.destroyAllWindows()