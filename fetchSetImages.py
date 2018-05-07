## fetchSetImages - Dakota Madden-Fong May 2018

# Looks for a .dict and .names file for the specified set, if none are available
# creates them by fetching image data based on urls provided by card_set_json

# .dict is a dictionary of cv2 image files keyed on mtgjson unique ids
# .names is a dictionary of card names keyed on mtgjson unique ids

# Returns the image dictionary and the name dictionary

import numpy as np
import cv2
from urllib import request as urlreq
import pickle
from mtg_json_get import card_set_json as cardset
import os

def fetchSetImages(setcode):
    
    files = os.listdir('./SetFiles')
    
    imgdict = dict()
    namedict = dict()
    
    if (setcode+'.images') not in files: # if .images file doesnt exist
        print(setcode +'.images','file not found, generating from gatherer now')
        set = cardset(setcode)# call card_set_json to get image URLs
        for i in range(len(set.uids)):# fetch all card images from URLs
            url = set.imgurls[i]
            if (url != None):
                url_response = urlreq.urlopen(url)
                img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
                img = cv2.imdecode(img_array, -1)
                imgdict[set.uids[i]] = img
                print(i)
                
        wfile = open(('SetFiles/'+setcode +'.images'), 'wb')#save images to local file
        pickle.dump(imgdict, wfile)
        wfile.close()
    
    if (setcode+'.names') not in files: # if .names file doesnt exist
        print(setcode +'.dict','file not found, generating from gatherer now')
        set = cardset(setcode)
        for i in range(len(set.uids)):
            url = set.imgurls[i]
            if (url != None):
                namedict[set.uids[i]] = set.names[i]
                print(i)
                
        wfile = open(('SetFiles/'+setcode +'.names'), 'wb')#save names to local file
        pickle.dump(namedict, wfile)
        wfile.close()
        
    print(setcode +'.images','file found')
    rfile = open(('SetFiles/'+ setcode + '.images'), 'rb')# read .images file from local disk
    imgdictret = pickle.load(rfile)
    rfile.close()
    
    print(setcode +'.names','file found')
    rfile = open(('SetFiles/'+ setcode + '.names'), 'rb')# read .names file from local disk
    namedictret = pickle.load(rfile)
    rfile.close()
    
    return(imgdictret,namedictret)