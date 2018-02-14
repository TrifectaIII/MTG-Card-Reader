from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog


x1 = Card.where(set_name='Eternal Masters').where(page=1).all()
x2 = Card.where(set_name='Eternal Masters').where(page=2).all()
x3 = Card.where(set_name='Eternal Masters').where(page=3).all()
x4 = Card.where(set_name='Eternal Masters').where(page=4).all()
x5 = Card.where(set_name='Eternal Masters').where(page=5).all()
x6 = Card.where(set_name='Eternal Masters').where(page=6).all()

x = []

for page in [x1,x2,x2,x4,x5,x6]:
    for card in page:
        x.append(card)
        
print(len(x))

for card in x:
    matches = 0
    for cardm in x:
        if (card.name == cardm.name):
            matches += 1
    if (matches > 1):
        print(card.name)
        print(matches)
        
x = []
looped = False
pagenum = 1
while not looped:
    page = Card.where(set_name='Eternal Masters').where(page=1).all()