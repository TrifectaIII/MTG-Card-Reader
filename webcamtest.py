import numpy as np
import cv2
from compare2set import compare2set

cap = cv2.VideoCapture(0)
fin = False

setcode = '3ED'

compareset = compare2set(setcode)
while(not fin):
    ret, frame = cap.read()

    cv2.imshow('frame',frame)
    inp = cv2.waitKey(1) & 0xFF
    if inp == ord('q'):
        fin = True
    if inp == ord('c'):
        compareset.compareimg(frame)

cap.release()
cv2.destroyAllWindows()