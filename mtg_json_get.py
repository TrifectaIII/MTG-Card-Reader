#extracts data from MTG-JSON file
#Dakota Madden-Fong May 2018

import json

#read in json file
jsonsets = json.loads(open('AllSets-x.json',encoding="utf8").read())

def getSets():
    #return alphabetized list of all sets, removing sets for which no card images exist
    retsets = []
    for set in (list(jsonsets.keys())):
        cards = jsonsets[set]['cards']
        empties = False
        exists = False
        multiverse_ids = []
        for card in cards:
            try:
                multiverse_ids.append(card['multiverseid'])
                exists = True
            except:
                multiverse_ids.append(None)
                empties = True
        if (empties and (not exists)):
            pass
        elif (empties and exists):
            pass
        else:
            retsets.append(set)
    retsets = sorted(retsets)
    return retsets

class card_set_json:
    # gather info on a specified set
    
    def __init__(self, setcode):
        try:
            self.cards = jsonsets[setcode]['cards']
        except:
            raise NameError('No set found with that setcode')
        
        self.names = []
        for card in self.cards:
            self.names.append(card['name'])
        # self.names = list of all card names
        self.uids = []
        for card in self.cards:
            self.uids.append(card['id'])
        # self.uids = list of all card unique ids
            
        self.multiverse_ids = []
        
        empties = False
        exists = False
        for card in self.cards:
            try:
                self.multiverse_ids.append(card['multiverseid'])
                exists = True
            except:
                self.multiverse_ids.append(None)
                empties = True
        if (empties and (not exists)):
            print('No images accessible')
        elif (empties and exists):
            print('Some images not accessible')
        else:
            print('All images accessible')
            
        
        # self.imgurls = list of all URLs to gatherer card images
        self.imgurls = []
        for id in self.multiverse_ids:
            if (id == None):
                self.imgurls.append(None)
            else: 
                self.imgurls.append('http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+str(id)+'&type=card')