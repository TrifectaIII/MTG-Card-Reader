## Manages the webcam feed in a thread so it doesn't impact main program performance.
#Dakota Madden-Fong May 2018
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
    
    sig = pyqtSignal()

            
    def WebCamMissing(self):
        # emit signal to trigger error message in MTGCardReader.py
        self.sig.emit()
        
    def __del__(self):
        self.wait()

    def __init__(self,imgwindow, parent = None):
        super(QWebcamThread,self).__init__(parent=parent)
        self.imgwindow = imgwindow
        self.done = False
        # on initialization, start reading from the webcam using OpenCV
        try:
            self.cap = cv2.VideoCapture(0)
            self.ret, self.cvframe = self.cap.read()
        except: 
            self.WebCamMissing()

    def getFrame(self):
        return self.cvframe
        
    def run(self):
        try:
            while not self.done:# update Webcam image every loop
                cvimg = self.cvframe
                height, width, _ = cvimg.shape
                while (width > 1000): #resize webcam images that are far too high resolution for the UI to handle
                    new_width = int(width/2)
                    new_height = int(height/2)
                    cvimg = cv2.resize(cvimg, (new_width,new_height) )#, fx=1, fy=1) 
                    height, width, _ = cvimg.shape
                cvimgRGB = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
                qpiximg = QPixmap(QImage(cvimgRGB, cvimgRGB.shape[1], cvimgRGB.shape[0], cvimgRGB.shape[1] * 3,QImage.Format_RGB888))
                self.imgwindow.setPixmap(qpiximg)
                self.imgwindow.update()
                self.ret, self.cvframe = self.cap.read()
        except:
            # if exception, signal for error message
            self.WebCamMissing()
        #QApplication.processEvents()