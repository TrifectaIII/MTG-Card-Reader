import numpy as np
import cv2
from compare2set import compare2set

cap = cv2.VideoCapture(0)
fin = False

compareset = compare2set('IMA')
while(not fin):
    # Capture frame-by-frame
    ret, frame = cap.read()

    cv2.imshow('frame',frame)
    inp = cv2.waitKey(1) & 0xFF
    if inp == ord('q'):
        fin = True
    if inp == ord('c'):
        #compare2set(frame,'IMA')
        compareset.compareimg(frame)
        
        
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
    # if cv2.waitKey(1) & 0xFF == ord('c'):
    #     compare2set(frame)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()