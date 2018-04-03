import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt
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
        
    def read_match(self):
        global matchname
        global setselect
        global cvframe
        global compareset
        print('Reading and Matching')
        matchname = compareset.compareimg(cvframe)
        
    def switchset(self, text):
        global matchname
        global setselect
        global cvframe
        global compareset
        print('Switching Set: ',text)
        start = setselect.findText('None', Qt.MatchFixedString)
        if start != -1:
            setselect.removeItem(start)
            matchname = 'Ready!'
        compareset = compare2set(text)
        matchname = 'Ready!'
        
    
    def cvimg2qpixmap(self, cvimg):
        cvimgRGB = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        qpixmap = QPixmap(QImage(cvimgRGB, cvimgRGB.shape[1], cvimgRGB.shape[0], cvimgRGB.shape[1] * 3,QImage.Format_RGB888))
        # height, width, channel = cvimg.shape
        # bytesPerLine = 3 * width
        # qpixmap = QPixmap(QImage(cvimg.data, width, height, bytesPerLine, QImage.Format_RGB888))
        return qpixmap
    
    ## Set Up Main UI
    def initUI(self):
        global matchname
        global setselect
        global cvframe
        global compareset
        setselect = []
        cvframe = []
        matchname = 'Select a Set Above'
        compareset = []
        
        #Set Tooltip Font
        QToolTip.setFont(QFont('SansSerif', 10))
        
        #Main Window
        grid = QGridLayout()
        self.setLayout(grid)
        self.center()
        self.setWindowTitle('MTG Card Reader')
        self.setWindowIcon(QIcon('MTG Blue.ico'))
        
        #Set Seclection Drop Down Menu
        setselectlab = QLabel(self)
        setselectlab.setText('Set:')
        grid.addWidget(setselectlab, 1,1)
        
        setselect = QComboBox(self)
        setselect.addItem('None')
        sets = {'MM3','IMA','MM2'}
        for set in sets:
            setselect.addItem(set)
        setselect.activated[str].connect(self.switchset)
        grid.addWidget(setselect, 1,2)
        
        #Quit Button
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        grid.addWidget(qbtn, 1,3)
        
        #Read Button
        readbtn = QPushButton('Read (R)', self)
        readbtn.setToolTip('Press when your card is in the frame')
        readbtn.resize(readbtn.sizeHint())
        readbtn.clicked.connect(self.read_match)
        grid.addWidget(readbtn, 2,1)
        readbtn.setDefault(True)
        
        #Image Window
        imgwindow = QLabel(self)
        grid.addWidget(imgwindow, 2,2)
        
        cardinfov = QVBoxLayout(self)
         
        #Name of Matched Card
        matchlab = QLabel(self)
        matchlab.setText('Read a Card!')
        cardinfov.addWidget(matchlab)
        
        grid.addLayout(cardinfov, 2,3)
        
        #Begin Video Capture
        try:
            cap = cv2.VideoCapture(0)
            ret, cvframe = cap.read()
            qpixframe = self.cvimg2qpixmap(cvframe)
        except:
            raise IOError('No Webcam Detected')
        imgwindow.setPixmap(qpixframe)
        wc_height, wc_width, _ = cvframe.shape
        readbtn.resize(wc_height, 100)
        
        
        self.show()
        while ret:
            qpixframe=self.cvimg2qpixmap(cvframe)
            imgwindow.setPixmap(qpixframe)
            imgwindow.update()
            matchlab.setText(matchname)
            QApplication.processEvents()
            ret,cvframe=cap.read()
    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    cr = CardReader()
    sys.exit(app.exec_())