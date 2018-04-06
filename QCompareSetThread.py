import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox,  QPlainTextEdit, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import numpy as np
import cv2
import time

from compare2set import compare2set
from mtg_json_get import getSets

class QComareSetThread(QThread):
            
    def __del__(self):
        self.wait()

    def __init__(self,name_match_lab, img_match_lab, statuslab,blank, parent = None):
        super(QCompareSetThread,self).__init__(parent=parent)
        self.name_match_lab = name_match_lab
        self.img_match_lab = img_match_lab
        self.statuslab = statuslab
        self.readbool = False
        self.set = ''

    def read_match(self):
        self.readbool = True
    def switchset(self,text):
        self.set = text
        
    def run(self):
        while True:
            ## read_match
            if self.readbool:
                print('Reading and Matching')
                self.name_match_lab.setText('Card: ')
                self.statuslab.setText('Reading Card...')
                self.img_match_lab.setPixmap(blank)
                QApplication.processEvents()
                (matchname,matchcvimage) = c2s.compareimg(cvim)
                matchimage = cvimg2qpixmap(matchcvimage)
                name_match_lab.setText('Card: '+matchname)
                img_match_lab.setPixmap(matchimage)
                self.statuslab.setText('Ready')
                QApplication.processEvents()
                self.readbool= False
            
            ## 
            
            if (self.set != ''):
                
                self.set = ''