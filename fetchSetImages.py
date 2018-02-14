import numpy as np
import cv2
from urllib import request as urlreq
import pickle
from mtg_cards import card_set_json as cardset
import os

def fetchSetImages(setcode):
    
    files = os.listdir('./SetFiles')
    
    set = cardset(setcode)
    setdict = dict()
    namedict = dict()
    
    if (setcode+'.dict') not in files:
        print(setcode+'.dict','file not found, generating from gatherer now')

        for i in range(len(set.uids)):
            url = set.imgurls[i]
            if (url != None):
                url_response = urlreq.urlopen(url)
                img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
                img = cv2.imdecode(img_array, -1)
                setdict[set.uids[i]] = img
                print(i)
                
        wfile = open(('SetFiles/'+setcode +'.dict'), 'wb')
        pickle.dump(setdict, wfile)
        wfile.close()
    
    if (setcode+'.names') not in files:
        print(setcode+'.dict','file not found, generating from gatherer now')

        for i in range(len(set.uids)):
            url = set.imgurls[i]
            if (url != None):
                namedict[set.uids[i]] = set.names[i]
                print(i)
                
        wfile = open(('SetFiles/'+setcode +'.names'), 'wb')
        pickle.dump(namedict, wfile)
        wfile.close()
        
    print(setcode +'.dict','file found')
    rfile = open(('SetFiles/'+ setcode + '.dict'), 'rb')
    setdictret = pickle.load(rfile)
    rfile.close()
    
    print(setcode +'.names','file found')
    rfile = open(('SetFiles/'+ setcode + '.names'), 'rb')
    namedictret = pickle.load(rfile)
    rfile.close()
    
    return(setdictret,namedictret)