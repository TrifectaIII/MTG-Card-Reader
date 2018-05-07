## Additional methods to extend the QPlainTextEdit: allows all text options in the texta area of the program
#Dakota Madden-Fong May 2018

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget,  QPlainTextEdit, QFileDialog
from PyQt5.QtCore import Qt, pyqtSlot


class QMtgPlainTextEdit(QPlainTextEdit):
    
    def loadtext(self):
        # load text to box from file
        filepath,_ = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Text files (*.txt)")
        file = open(filepath,'r')
        filetext = file.read()
        file.close()
        self.setPlainText(filetext)
    def savetext(self):
        # save text from box to file
        curr_text = self.toPlainText()
        filepath,_ = QFileDialog.getSaveFileName(self, 'Open file', 'c:\\',"Text files (*.txt)")
        file = open(filepath,'w')
        file.write(curr_text)
        file.close()
    def copy_alltext(self):
        #copy all text
        self.selectAll()
        self.copy()
        self.cursor.clearSelection()
        self.setTextCursor(self.cursor)
        
    def start_sideboard(self):
        #add sideboard divider
        self.appendPlainText('\nSideboard:')
    def start_divider(self):
        #add alternate divider
        self.appendPlainText('\n==========\n')
        
    def addtotext(self,num, name_match_lab):
        # add or remove some number of a card from the text box
        if num >=0:
            print('Adding',num,'to textbox')
        else:
            print('Removing',abs(num),'from textbox')
        matchname = name_match_lab.text()[6:]
        matchname_words = matchname.split()
        curr_text = self.toPlainText()
        curr_lines = curr_text.splitlines()
        newcard = True
        sideboard = False
        newline = ''
        #loop up the lines of the text box
        for line in range((len(curr_lines))-1,-1,-1):
            line_words = curr_lines[line].split()
            
            # If you hit a divider, act as if nothing more exists
            if (((line_words or [' '])[0]).lower() == "sideboard:"):
                sideboard = True
            if (((line_words or [' '])[0]).lower() == "=========="):
                sideboard = True
            if ((matchname_words == line_words[1:]) and (newcard) and (not sideboard)):
                newnumber = num + int(line_words[0])
                if newnumber > 0:
                    line_words[0] = str(newnumber)
                    curr_lines[line] = ' '.join(line_words)
                else:
                    curr_lines[line] = '__delete__this__'
                newcard = False
        if (newcard and (num>0)):
            textline = str(num)+' '+matchname
            self.appendPlainText(textline)
        else:
            curr_lines[:] = [line for line in curr_lines if line != '__delete__this__']
            new_text = '\n'.join(curr_lines)
            self.setPlainText(new_text)
        QApplication.processEvents()
        
    def __init__(self,textedit, text='', parent=None):
        super(QMtgPlainTextEdit, self).__init__(parent=parent)
        self.cursor = self.textCursor()