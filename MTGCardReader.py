import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QMessageBox, QPushButton, QApplication, QDesktopWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QComboBox,  QPlainTextEdit, QSizePolicy, QFileDialog
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import numpy as np
import cv2
import time

from compare2set import compare2set
from mtg_json_get import getSets
from QMtgPlainTextEdit import QMtgPlainTextEdit
from QWebcamThread import QWebcamThread
from QCompareSetThread import QCompareSetThread


class MTGCardReader(QWidget):
    
    # readsig = pyqtSignal()
    # setsig = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def closeEvent(self, event):
        #Handles qutting when using the top-right X
        reply = QMessageBox.question(self, 'Quitting?',
            "Do you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()  
            
    def keyPressEvent(self, event):
        key = event.key()
        print(key)
        
    def center(self):
        #Function to center the window
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
            
    
    ## Set Up Main UI
    
    def initUI(self):
        global oldset
        
        ##Functions
        
        def read_match(c2s,cvim):
            print('Reading and Matching')
            name_match_lab.setText('Card: ')
            statuslab.setText('Reading Card...')
            img_match_lab.setPixmap(blank)
            setButtons(False)
            textbox.setReadOnly(True)
            QApplication.processEvents()
            (matchname,matchcvimage) = c2s.compareimg(cvim)
            matchimage = cvimg2qpixmap(matchcvimage)
            name_match_lab.setText('Card: '+matchname)
            img_match_lab.setPixmap(matchimage)
            statuslab.setText('Ready')
            setButtons(True)
            textbox.setReadOnly(False)
            QApplication.processEvents()
        
        oldset = 'None'
        def switchset(text):
            global compareset
            global oldset
            if not (text == oldset):
                print('Switching to Set: ',text)
                name_match_lab.setText('Card: ')
                statuslab.setText('Loading {}...'.format(text))
                img_match_lab.setPixmap(blank)
                setButtons(False)
                textbox.setReadOnly(True)
                QApplication.processEvents()
                start = setselect.findText('None', Qt.MatchFixedString)
                if start != -1:
                    setselect.removeItem(start)
                compareset = compare2set(text)
                statuslab.setText('Ready')
                #---------------------------
                setButtons(True)
                add1btn.setEnabled(False)
                add4btn.setEnabled(False)
                add10btn.setEnabled(False)
                textbox.setReadOnly(False)
                #---------------------------
                QApplication.processEvents()
            oldset = text

        def cvimg2qpixmap(cvimg):
            cvimgRGB = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
            qpiximg = QPixmap(QImage(cvimgRGB, cvimgRGB.shape[1], cvimgRGB.shape[0], cvimgRGB.shape[1] * 3,QImage.Format_RGB888))
            return qpiximg
            
        def WebCamMissingDialog():
            reply = QMessageBox.question(self, 'Webcam Error',"Webcam Error:\n\nPlease ensure that your webcam is connected, then restart the program.", QMessageBox.Ok, QMessageBox.Ok)
        ##Widgets
        
        ##Left Side
        
        #Main Window
        grid = QGridLayout()
        self.setLayout(grid)
        self.setWindowTitle('MTG Card Reader')
        self.setWindowIcon(QIcon('Mana_U.png'))
        #Set Tooltip Font
        QToolTip.setFont(QFont('SansSerif', 10))
        
        setinfoh = QHBoxLayout()
        grid.addLayout(setinfoh, 1,1,1,2)
        
        #Credits
        creditlab = QLabel(self)
        creditlab.setText('Created By: Dakota Madden-Fong')
        setinfoh.addWidget(creditlab)
        
        #Set Seclection Drop Down Menu
        setselectlab = QLabel(self)
        setselectlab.setText('Set:')
        setselectlab.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        setinfoh.addWidget(setselectlab)
        
        setselect = QComboBox(self)
        setselect.addItem('None')
        sets = getSets()
        for set in sets:
            setselect.addItem(set)
        setinfoh.addWidget(setselect)
        
        #Status Indicator
        statuslab2 = QLabel(self)
        statuslab2.setText('Status:')
        statuslab2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        setinfoh.addWidget(statuslab2)
        
        statuslab = QLabel(self)
        statuslab.setText('Choose a Set')
        statuslab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        setinfoh.addWidget(statuslab)
        
        #Read Button
        readbtn = QPushButton('Read', self)
        readbtn.setToolTip('Press when your card is in the frame')
        readbtn.setEnabled(False)
        readbtn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        grid.addWidget(readbtn, 2,1,2,1)
        readbtn.setDefault(True)
        
        #Image Window
        imgwindow = QLabel(self)
        grid.addWidget(imgwindow, 2,2,2,1)
        
        
        ##Card Info Vert
        
        cardinfov = QVBoxLayout()
        grid.addLayout(cardinfov, 1,3,3,1)
         
        #Add 1 to Text Button
        add1btn = QPushButton('Add 1', self)
        add1btn.setToolTip('Press to add this card to the text box')
        add1btn.setEnabled(False)
        add1btn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        cardinfov.addWidget(add1btn)
        add1btn.setDefault(True)
        
        #Add 4 to Text Button
        add4btn = QPushButton('Add 4', self)
        add4btn.setToolTip('Press to add 4 of this card to the text box')
        add4btn.setEnabled(False)
        add4btn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        cardinfov.addWidget(add4btn)
        add4btn.setDefault(True)
        
        #Add 10 to Text Button
        add10btn = QPushButton('Add 10', self)
        add10btn.setToolTip('Press to add 10 of this card to the text box')
        add10btn.setEnabled(False)
        add10btn.setSizePolicy(QSizePolicy.MinimumExpanding,QSizePolicy.Preferred)
        cardinfov.addWidget(add10btn)
        add10btn.setDefault(True)
         
        #Name of Matched Card
        name_match_lab = QLabel(self)
        name_match_lab.setText('Card: ')
        cardinfov.addWidget(name_match_lab)
        
        #Image of Matched Card
        img_match_lab = QLabel(self)
        blankcv = cv2.imread('blank.png')
        blank = cvimg2qpixmap(blankcv)
        img_match_lab.setPixmap(blank)
        cardinfov.addWidget(img_match_lab)
        
        ##Text Vert
        
        textv = QVBoxLayout()
        grid.addLayout(textv, 1,4,3,1)
        
        #Text Area
        textbox = QMtgPlainTextEdit(self)
        
                ##File Options
        fileopth = QHBoxLayout()
        textv.addLayout(fileopth)
        
        #Load Button
        loadbtn = QPushButton('Load', self)
        loadbtn.setToolTip('load contents of a text file')
        fileopth.addWidget(loadbtn)
        loadbtn.setEnabled(True)
        loadbtn.setDefault(True)
        
        #Save Button
        savebtn = QPushButton('Save', self)
        savebtn.setToolTip('save contents to a text file')
        savebtn.setEnabled(True)
        fileopth.addWidget(savebtn)
        savebtn.setDefault(True)
        
        textv.addWidget(textbox)
        
                ##Text Options
        
        textopth = QHBoxLayout()
        textv.addLayout(textopth)
        
        #Copy Button
        copybtn = QPushButton('Copy All', self)
        copybtn.setToolTip('Copy contents of text box to clipboard')
        copybtn.setEnabled(True)
        textopth.addWidget(copybtn)
        copybtn.setDefault(True)
        #Paste Button
        pastebtn = QPushButton('Paste', self)
        pastebtn.setToolTip('Paste contents of clipboard to text box')
        pastebtn.setEnabled(True)
        textopth.addWidget(pastebtn)
        pastebtn.setDefault(True)
        #Clear Button
        clearbtn = QPushButton('Clear', self)
        clearbtn.setToolTip('clears contents of text box')
        clearbtn.setEnabled(True)
        textopth.addWidget(clearbtn)
        clearbtn.setDefault(True)
        
        divideropth = QHBoxLayout()
        textv.addLayout(divideropth)
        
        #Side Button
        sidebtn = QPushButton('Start Sideboard', self)
        sidebtn.setToolTip('Start a Sideboard')
        sidebtn.setEnabled(True)
        divideropth.addWidget(sidebtn)
        sidebtn.setDefault(True)
        
        #Divider Button
        dividebtn = QPushButton('Add Divider', self)
        dividebtn.setToolTip('Add a divider')
        dividebtn.setEnabled(True)
        divideropth.addWidget(dividebtn)
        dividebtn.setDefault(True)
        
        buttons = [add10btn,add4btn,add1btn,dividebtn,sidebtn,clearbtn,pastebtn,copybtn,savebtn,loadbtn,readbtn,setselect]
        
        #Webcam Thread
        camthread = QWebcamThread(imgwindow,self)
        #comparesetthread = QCompareSetThread(name_match_lab, img_match_lab, statuslab,setselect,blank,buttons,self)
        
        ##Signals
        
        setselect.activated[str].connect(switchset)
        readbtn.clicked.connect(lambda:read_match(compareset,camthread.getFrame()))
        
        # setselect.activated[str].connect(comparesetthread.switchset)
        # readbtn.clicked.connect(lambda:comparesetthread.read_match(camthread.getFrame()))
        
        add1btn.clicked.connect(lambda:textbox.addtotext(1,name_match_lab))
        add4btn.clicked.connect(lambda:textbox.addtotext(4,name_match_lab))
        add10btn.clicked.connect(lambda:textbox.addtotext(10,name_match_lab))
        loadbtn.clicked.connect(textbox.loadtext)
        savebtn.clicked.connect(textbox.savetext)
        copybtn.clicked.connect(textbox.copy_alltext)
        pastebtn.clicked.connect(textbox.paste)
        clearbtn.clicked.connect(textbox.clear)
        sidebtn.clicked.connect(textbox.start_sideboard)
        dividebtn.clicked.connect(textbox.start_divider)
        
        camthread.sig.connect(WebCamMissingDialog)
        
        def setButtons(state):
            for btn in buttons:
                btn.setEnabled(state)
        
        
        ##Main Camera Loop
        self.show()
        camthread.start()
        #comparesetthread.start()
        self.center()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    # font = app.font()
    # font.setPointSize(15)
    # font.setBold(True)
    # app.setFont(font)
    mtg_cr = MTGCardReader()
    sys.exit(app.exec_())