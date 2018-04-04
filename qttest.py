import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSlot
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
        
    
    
    ## Set Up Main UI
    def initUI(self):
        global compareset
        compareset = []
        
        def read_match(c2s,cvim):
            print('Reading and Matching')
            name_match_lab.setText('Matching...')
            img_match_lab.setText(' ')
            readbtn.setEnabled(False)
            setselect.setEnabled(False)
            QApplication.processEvents()
            (matchname,matchcvimage) = c2s.compareimg(cvim)
            matchimage = cvimg2qpixmap(matchcvimage)
            name_match_lab.setText(matchname)
            img_match_lab.setPixmap(matchimage)
            
            readbtn.setEnabled(True)
            setselect.setEnabled(True)
            QApplication.processEvents()
            
        def switchset(text):
            global compareset
            print('Switching to Set: ',text)
            name_match_lab.setText('Loading Set {}'.format(text))
            img_match_lab.setText(' ')
            readbtn.setEnabled(False)
            setselect.setEnabled(False)
            QApplication.processEvents()
            start = setselect.findText('None', Qt.MatchFixedString)
            if start != -1:
                setselect.removeItem(start)
            compareset = compare2set(text)
            name_match_lab.setText('Ready')
            readbtn.setEnabled(True)
            setselect.setEnabled(True)
            QApplication.processEvents()

        def cvimg2qpixmap(cvimg):
            cvimgRGB = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
            qpixmap = QPixmap(QImage(cvimgRGB, cvimgRGB.shape[1], cvimgRGB.shape[0], cvimgRGB.shape[1] * 3,QImage.Format_RGB888))
            # height, width, channel = cvimg.shape
            # bytesPerLine = 3 * width
            # qpixmap = QPixmap(QImage(cvimg.data, width, height, bytesPerLine, QImage.Format_RGB888))
            return qpixmap
            #Set Tooltip Font
            QToolTip.setFont(QFont('SansSerif', 10))
            
        def updateWC(cvimg):
            pixmapimg = cvimg2qpixmap(cvimg)
            imgwindow.setPixmap(pixmapimg)
            imgwindow.update()
            QApplication.processEvents()
        
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
        setselect.activated[str].connect(switchset)
        grid.addWidget(setselect, 1,2)
        
        #Quit Button
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        grid.addWidget(qbtn, 1,3)
        
        #Read Button
        readbtn = QPushButton('Read', self)
        readbtn.setToolTip('Press when your card is in the frame')
        readbtn.resize(readbtn.sizeHint())
        readbtn.clicked.connect(lambda:read_match(compareset,cvframe))
        readbtn.setEnabled(False)
        grid.addWidget(readbtn, 2,1)
        readbtn.setDefault(True)
        
        #Image Window
        imgwindow = QLabel(self)
        grid.addWidget(imgwindow, 2,2)
        
        cardinfov = QVBoxLayout()
        grid.addLayout(cardinfov, 2,3)
         
        #Name of Matched Card
        name_match_lab = QLabel(self)
        name_match_lab.setText('Select a Set Above')
        cardinfov.addWidget(name_match_lab)
        
        img_match_lab = QLabel(self)
        img_match_lab.setText(' ')
        cardinfov.addWidget(img_match_lab)
        
        
        #Begin Video Capture
        try:
            cap = cv2.VideoCapture(0)
            ret, cvframe = cap.read()
            updateWC(cvframe)
        except:
            raise IOError('Webcam or Image Error')
        #wc_height, wc_width, _ = cvframe.shape
        
        self.show()
        while ret:
            updateWC(cvframe)
            ret,cvframe=cap.read()
    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    cr = CardReader()
    sys.exit(app.exec_())