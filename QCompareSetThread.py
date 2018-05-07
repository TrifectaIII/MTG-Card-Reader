import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox,  QPlainTextEdit, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import numpy as np
import cv2
import time
## This file is not perational at the moment and is not hooked into the rest of the program.


from compare2set import compare2set
from mtg_json_get import getSets

class QCompareSetThread(QThread):
            
    def __del__(self):
        self.wait()

    def __init__(self,name_match_lab, img_match_lab, statuslab,setselect,blank,buttons, parent = None):
        super(QCompareSetThread,self).__init__(parent=parent)
        self.name_match_lab = name_match_lab
        self.img_match_lab = img_match_lab
        self.statuslab = statuslab
        self.blank = blank
        self.compareset = []
        self.oldset = 'None'
        self.setselect = setselect
        self.buttons = buttons
        self.readimg = []
        self.settext = ''
        
    def setButtons(self,state):
        for btn in self.buttons:
            btn.setEnabled(state)
        
    def read_match(self,cvimg):
        self.readimg = cvimg
    def switchset(self,text):
        self.settext = text
        
    def run(self):
        if self.settext != '':
            if not (self.settext == self.oldset):
                print('Switching to Set: ',text)
                self.name_match_lab.setText('Card: ')
                self.statuslab.setText('Loading {}...'.format(text))
                self.img_match_lab.setPixmap(self.blank)
                #self.setButtons(False)
                QApplication.processEvents()
                start = self.setselect.findText('None', Qt.MatchFixedString)
                if start != -1:
                    self.setselect.removeItem(start)
                self.compareset = compare2set(text)
                self.statuslab.setText('Ready')
                #---------------------------
                self.setButtons(True)
                self.buttons[0].setEnabled(False)
                self.buttons[1].setEnabled(False)
                self.buttons[2].setEnabled(False)
                #---------------------------
                QApplication.processEvents()
            self.oldset = text
            self.settext = ''
        
        if self.readimg != []:
            print('Reading and Matching')
            self.name_match_lab.setText('Card: ')
            self.statuslab.setText('Reading Card...')
            self.img_match_lab.setPixmap(self.blank)
            #self.setButtons(False)
            QApplication.processEvents()
            (matchname,matchcvimage) = self.compareset.compareimg(readimg)
            cvimgRGB = cv2.cvtColor(matchcvimage, cv2.COLOR_BGR2RGB)
            qpiximg = QPixmap(QImage(cvimgRGB, cvimgRGB.shape[1], cvimgRGB.shape[0], cvimgRGB.shape[1] * 3,QImage.Format_RGB888))
            self.name_match_lab.setText('Card: '+matchname)
            self.img_match_lab.setPixmap(qpiximg)
            self.statuslab.setText('Ready')
            self.setButtons(True)
            self.readimage = []