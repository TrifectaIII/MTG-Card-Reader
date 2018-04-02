from tkinter import *
from tkinter import ttk
import numpy as np
import cv2
from compare2set import compare2set
from PIL import Image, ImageTk

## Set Up Window
root = Tk()
root.title("MTG Card Reader")
root.iconbitmap('MTG Blue.ico')
root.mainloop()

mainframe = ttk.Frame(root, padding="200 200 200 200")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

## Tk Variables
cardname = StringVar(root)
cardset = StringVar(root)
compareset_name = StringVar(root)
sets = ['MM3','IMA']
compareset_name.set('')

chooselabel = Label(mainframe, text="Choose a Set")
chooselabel.grid(row = 1, column = 1)
setlabel = Label(mainframe, text='No Set Chosen')
setlabel.grid(row = 3, column = 1)
popupMenu = OptionMenu(mainframe, cardset, *sets)
popupMenu.grid(row = 2, column =1)
# on change dropdown value
def cardset_change_dropdown(*args):
    print( cardset.get() )
    setlabel.configure(text = 'Loading')
    
    if cardset.get() != compareset_name.get():
        compareset_name.set(cardset.get())
        compareset = compare2set(cardset.get())
        setlabel.configure(text = cardset.get())
 
# link function to change dropdown
cardset.trace('w', cardset_change_dropdown)
 
root.mainloop()