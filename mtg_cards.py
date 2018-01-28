from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog

class Printings:
    def __init__(self, cardname):
        self.cards = Card.where(name=cardname).all()
        self.cards[:] = [card for card in self.cards if (cardname == card.name)]
        
        if (len(self.cards) == 0):
            raise NameError('No card found with that name')
        
        self.sets = []
        for card in self.cards:
            self.sets.append(card.set)
        
        self.imgurls = []
        for card in self.cards:
            self.imgurls.append(card.image_url)

 
## https://img.scryfall.com/cards/png/en/ set / number .png

