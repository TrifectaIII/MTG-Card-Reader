## fetchSetImages - Dakota Madden-Fong

# Looks for a .dict and .names file for the specified set, if none are available
# creates them by fetching image data based on urls provided by card_set_json

# .dict is a dictionary of cv2 image files keyed on mtgjson unique ids
# .names is a dictionary of card names keyed on mtgjson unique ids

# Returns the image dictionary and the name dictionary

import numpy as np
import cv2
from urllib import request as urlreq
import pickle
from mtg_cards import card_set_json as cardset
import os

def fetchSetImages(setcode):
    
    files = os.listdir('./SetFiles')
    
    imgdict = dict()
    namedict = dict()
    
    if (setcode+'.images') not in files:
        print(setcode +'.images','file not found, generating from gatherer now')
        set = cardset(setcode)
        for i in range(len(set.uids)):
            url = set.imgurls[i]
            if (url != None):
                url_response = urlreq.urlopen(url)
                img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
                img = cv2.imdecode(img_array, -1)
                imgdict[set.uids[i]] = img
                print(i)
                
        wfile = open(('SetFiles/'+setcode +'.images'), 'wb')
        pickle.dump(imgdict, wfile)
        wfile.close()
    
    if (setcode+'.names') not in files:
        print(setcode +'.dict','file not found, generating from gatherer now')
        set = cardset(setcode)
        for i in range(len(set.uids)):
            url = set.imgurls[i]
            if (url != None):
                namedict[set.uids[i]] = set.names[i]
                print(i)
                
        wfile = open(('SetFiles/'+setcode +'.names'), 'wb')
        pickle.dump(namedict, wfile)
        wfile.close()
        
    print(setcode +'.images','file found')
    rfile = open(('SetFiles/'+ setcode + '.images'), 'rb')
    imgdictret = pickle.load(rfile)
    rfile.close()
    
    print(setcode +'.names','file found')
    rfile = open(('SetFiles/'+ setcode + '.names'), 'rb')
    namedictret = pickle.load(rfile)
    rfile.close()
    
    return(imgdictret,namedictret)