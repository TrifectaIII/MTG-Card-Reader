import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox,  QPlainTextEdit, QSizePolicy, QFileDialog, QDialog
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSlot
import numpy as np
import cv2
import time

from compare2set import compare2set
from mtg_json_get import getSets

class QMtgPlainTextEdit(QPlainTextEdit):
    
    def loadtext(self):
        filepath,_ = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Text files (*.txt)")
        file = open(filepath,'r')
        filetext = file.read()
        file.close()
        self.setPlainText(filetext)
    def savetext(self):
        curr_text = self.toPlainText()
        filepath,_ = QFileDialog.getSaveFileName(self, 'Open file', 'c:\\',"Text files (*.txt)")
        file = open(filepath,'w')
        file.write(curr_text)
        file.close()
    def copy_alltext(self):
        self.selectAll()
        self.copy()
        self.cursor.clearSelection()
        self.setTextCursor(self.cursor)
    def start_sideboard(self):
        self.appendPlainText('\nSideboard:')
        
    def addtotext(self,num, name_match_lab):
        print('Adding to textbox')
        matchname = name_match_lab.text()[6:]
        matchname_words = matchname.split()
        curr_text = self.toPlainText()
        curr_lines = curr_text.splitlines()
        newcard = True
        sideboard = False
        newline = ''
        for line in range((len(curr_lines))-1,-1,-1):
            line_words = curr_lines[line].split()
            
            if (((line_words or [' '])[0]).lower() == "sideboard:"):
                sideboard = True
            if ((matchname_words == line_words[1:]) and (newcard) and (not sideboard)):
                #print(line_words)
                line_words[0] = str(num + int(line_words[0]))
                #print(line_words)
                #print(curr_lines[line])
                #print(' '.join(line_words))
                curr_lines[line] = ' '.join(line_words)
                newcard = False
        #print(curr_lines)
        #print('newcard',newcard)
        if newcard:
            textline = str(num)+' '+matchname
            self.appendPlainText(textline)
        else:
            new_text = '\n'.join(curr_lines)
            self.setPlainText(new_text)
        QApplication.processEvents()
        
    def __init__(self,textedit, text='', parent=None):
        super(QMtgPlainTextEdit, self).__init__(parent=parent)
        self.cursor = self.textCursor()