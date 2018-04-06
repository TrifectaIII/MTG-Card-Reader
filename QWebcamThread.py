import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox,  QPlainTextEdit, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import numpy as np
import cv2
import time

from compare2set import compare2set
from mtg_json_get import getSets

class QWebcamThread(QThread):
    
    
    def __init__(self,imgwindow, parent = None):
        super(QWebcamThread,self).__init__(parent=parent)
        self.imgwindow = imgwindow
        self.cap = cv2.VideoCapture(0)
        self.ret, self.cvframe = self.cap.read()
        
    def __del__(self):
        self.wait()
        
    def getFrame(self):
        return self.cvframe
        
    def run(self):
        while self.ret:
            cvimg = cv2.resize(self.cvframe, (640,480))#, fx=1, fy=1) 
            cvimgRGB = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
            qpiximg = QPixmap(QImage(cvimgRGB, cvimgRGB.shape[1], cvimgRGB.shape[0], cvimgRGB.shape[1] * 3,QImage.Format_RGB888))
            self.imgwindow.setPixmap(qpiximg)
            self.imgwindow.update()
            self.ret, self.cvframe = self.cap.read()
            #QApplication.processEvents()
            