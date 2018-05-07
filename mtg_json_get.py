#extracts data from MTG-JSON file

import json

jsonsets = json.loads(open('AllSets-x.json',encoding="utf8").read())
    
def getSets():
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
    def __init__(self, setcode):
        try:
            self.cards = jsonsets[setcode]['cards']
        except:
            raise NameError('No set found with that setcode')
        
        self.names = []
        for card in self.cards:
            self.names.append(card['name'])
            
        self.uids = []
        for card in self.cards:
            self.uids.append(card['id'])
            
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
            
        
        
        self.imgurls = []
        for id in self.multiverse_ids:
            if (id == None):
                self.imgurls.append(None)
            else: 
                self.imgurls.append('http://gatherer.wizards.com/Handlers/Image.ashx?multiverseid='+str(id)+'&type=card')

# class card_printings:
#     def __init__(self, cardname):
#         self.cards = Card.where(name=cardname).all()
#         self.cards[:] = [card for card in self.cards if (cardname == card.name)]
#         
#         if (len(self.cards) == 0):
#             raise NameError('No card found with that name')
#         
#         self.sets = []
#         for card in self.cards:
#             self.sets.append(card.set)
#         
#         self.imgurls = []
#         for card in self.cards:
#             self.imgurls.append(card.image_url)
# 
# # scryfall large image urls:
# # https://img.scryfall.com/cards/png/en/ set / number .png
# 
# class card_set:
#     def __init__(self, setcode):
#         more = True
#         self.cards = []
#         pagenum = 1
#         while more:
#             newcards = Card.where(set=setcode).where(page=pagenum).all()
#             self.cards += Card.where(set=setcode).where(page=pagenum).all()
#             if (len(newcards)<100):
#                 more = False
#             else:
#                 pagenum += 1
#         
#         self.cards[:] = [card for card in self.cards if (setcode == card.set)]
#         
#         if (len(self.cards) == 0):
#             raise NameError('No card found with that set code')
#         
#         self.imgurls = []
#         for card in self.cards:
#             self.imgurls.append(card.image_url)
