from urllib import request as urlreq
import numpy as np
import cv2


url = 'http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid=413582&type=card'

url_response = urlreq.urlopen(url)

img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)

img = cv2.imdecode(img_array, -1)

cv2.imshow('URL Image', img)