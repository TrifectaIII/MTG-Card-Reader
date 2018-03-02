from tkinter import *
from tkinter import ttk

## Set Up Window
root = Tk()
root.title("MTG Card Reader")
root.iconbitmap('MTG Blue.ico')
root.mainloop()

mainframe = ttk.Frame(root, padding="12 12 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

## Tk Variables
cardname = StringVar()
cardset_enter = StringVar()
cardset = StringVar()

sets = ['MM3','IMA']

popupMenu = OptionMenu(mainframe, cardset_enter, *sets)
Label(mainframe, text="Choose a Set").grid(row = 1, column = 1)
popupMenu.grid(row = 2, column =1)
setname = cardset_enter.get()
Label(mainframe, text=setname).grid(row = 3, column = 1)
 
# on change dropdown value
def change_dropdown(*args):
    print( cardset_enter.get() )
 
# link function to change dropdown
cardset_enter.trace('w', change_dropdown)
 
root.mainloop()