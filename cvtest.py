import numpy as np
import cv2
from matplotlib import pyplot as plt
import urllib

# vma = cv2.imread('vma.jpg')
# wth = cv2.imread('wth.jpg')
# real = cv2.imread('real.png')

# vma = cv2.imread('ms_ima.jpg')
# wth = cv2.imread('ms_wth.jpg')
# real = cv2.imread('ms_ima_c.jpg')

#vma = cv2.imread('rs_mm3.jpg')
vma = cv2.imread('rs_mm3_s.jpg')
wth = cv2.imread('rs_nme_s.jpg')
real = cv2.imread('rs_mm3_c.jpg')

vmag = cv2.cvtColor(vma, cv2.COLOR_BGR2GRAY)
wthg = cv2.cvtColor(wth, cv2.COLOR_BGR2GRAY)
realg = cv2.cvtColor(real, cv2.COLOR_BGR2GRAY)

surf = cv2.xfeatures2d.SURF_create()
surf.setHessianThreshold(5000)

## Real Points
(kpr, desr) = surf.detectAndCompute(realg,None)
realp = cv2.drawKeypoints(realg,kpr,None,(255,0,0),4)
# cv2.namedWindow( "Display window 1");
# cv2.imshow( "Display window 1", realp );

## VMA Points
(kpv, desv) = surf.detectAndCompute(vmag,None)
vmap = cv2.drawKeypoints(vmag,kpv,None,(255,0,0),4)
# cv2.namedWindow( "Display window 2");
# cv2.imshow( "Display window 2", vmap );

## WTH Points
(kpw, desw) = surf.detectAndCompute(wthg,None)
wthp = cv2.drawKeypoints(wthg,kpw,None,(255,0,0),4)
# cv2.namedWindow( "Display window 3");
# cv2.imshow( "Display window 3", wthp );

## Matching
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

matches = bf.match(desr,desv)
matches = sorted(matches, key = lambda x:x.distance)
print(len(matches))
test = realg
test = cv2.drawMatches(realg,kpr,vmag,kpv,matches[:30],test, flags=2)
plt.imshow(test),plt.show()
cv2.namedWindow( "Display window 1");
cv2.imshow( "Display window 1", test );



matches = bf.match(desr,desw)
matches = sorted(matches, key = lambda x:x.distance)
print(len(matches))
test2 = realg
test2 = cv2.drawMatches(realg,kpr,wthg,kpw,matches[:30],test2, flags=2)
# plt.imshow(test2),plt.show()
cv2.namedWindow( "Display window 2");
cv2.imshow( "Display window 2", test2 );