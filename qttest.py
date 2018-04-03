
import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage, QComboBox


import numpy as np
import cv2

from compare2set import compare2set

class CardReader(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def closeEvent(self, event):
        #Handles qutting when using the top-right X
        reply = QMessageBox.question(self, 'Quitting',
            "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  
        
    def center(self):
        #Function to center the window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    
    def cvimg2qpixmap(self, cvimg):
        qpixmap = QPixmap(QImage(cvimg, cvimg.shape[1], cvimg.shape[0], cvimg.shape[1] * 3,QImage.Format_RGB888))
        # height, width, channel = cvimg.shape
        # bytesPerLine = 3 * width
        # qpixmap = QPixmap(QImage(cvimg.data, width, height, bytesPerLine, QImage.Format_RGB888))
        return qpixmap
    
    ## Set Up Main UI
    def initUI(self):
        #Set Tooltip Font
        QToolTip.setFont(QFont('SansSerif', 10))
        
        #Main Window
        w_height = 800
        w_width  = 600
        w_margin = 50
        
        self.setGeometry(0, 0, w_height, w_width)
        self.center()
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('MTG Blue.ico'))
        
        #Read Button
        readbtn = QPushButton('Read!', self)
        readbtn.setToolTip('Press when your card is in the frame')
        readbtn.resize(readbtn.sizeHint())
        readbtn.move(50, 50)
        
        #Set Seclection Drop Down Menu
        setselect = QComboBox(self)
        sets = {'MM3','IMA','MM2'}
        for set in sets:
            setselect.addItem(set)
        
        setselect.activated[str].connect(self.style_choice)
        
        #Quit Button
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(w_height - w_margin, w_width - w_margin)   
        
        #Image Window
        imgwindow = QLabel(self)
        imgwindow.move(150,50)
        
        #Begin Video Capture
        cap = cv2.VideoCapture(0)
        ret, cvframe = cap.read()
        qpixframe = self.cvimg2qpixmap(cvframe)
        imgwindow.setPixmap(qpixframe)
        
        self.show()
        while ret:
            qpixframe=self.cvimg2qpixmap(cvframe)
            imgwindow.setPixmap(qpixframe)
            imgwindow.update()
            QApplication.processEvents()
            ret,cvframe=cap.read()
    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    cr = CardReader()
    sys.exit(app.exec_())