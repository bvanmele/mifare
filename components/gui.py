import csv

from PyQt5.QtCore import QThreadPool
#from PyQt5.QtGui import QMovie
#from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import ( QWidget, QPushButton, QToolTip, QMessageBox, QDesktopWidget, QAction, qApp,
                             QMainWindow, QMenu, QLabel, QLineEdit, QGridLayout, QFileDialog)
from PyQt5.QtGui import (QIcon, QFont, QPixmap)

from components.table import cardList
from workers.card import CardWorker
from workers.data import DataWorker

import os


class GUI(QMainWindow):
    def __init__(self,parent=None):
        super(GUI, self).__init__(parent)
        self.threadpool = QThreadPool()
        self.form = FormUI(self)
        self.initUI()

    def initUI(self):

        #paramètres globaux
        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('Ceci est un programme pour <b>lire les cartes des employés</b> ')





        #contruction du menu
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(qApp.quit)

        ExpMenu = QMenu('Export', self)
        ExpAct = QAction('Export des utilisateurs', self)
        ExpAct.triggered.connect(self.exportCSV)
        ExpMenu.addAction(ExpAct)

        ListMenu = QMenu('Liste',self)
        ListAct = QAction('Liste des utilisateurs',self)
        ListAct.triggered.connect(self.showList)
        ListMenu.addAction(ListAct)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Fichier')
        fileMenu.addAction(exitAct)
        fileMenu.addMenu(ExpMenu)
        fileMenu.addMenu(ListMenu)

        #ajout d'une icone
        icon = QIcon()
        icon.addPixmap(QPixmap('../icon.png'),QIcon.Normal,QIcon.Off)
        self.setWindowIcon(icon)


        # definition des dimensions et positionement de la fenêtre
        self.setGeometry(300, 300, 300, 200)
        self.center()
        self.setWindowTitle('Lecture carte employé')
        self.setCentralWidget(self.form)

        #on affiche
        self.show()

    def exportCSV(self):
        worker = DataWorker('export',None)
        worker.signals.result.connect(self.writeCSV)
        self.threadpool.start(worker)


    def writeCSV(self,data):
        path = QFileDialog.getSaveFileName(self, 'Export CSV', os.getenv('HOME'),'CSV(*.csv)')
        if path[0] != '':
            with open(path[0], 'w') as csv_file:
                writer = csv.writer(csv_file, dialect='excel')
                for row in data:
                    writer.writerow(row)

    def showList(self):
        liste = cardList()
        liste.populate()
        liste.exec()



    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Êtes-vous certain de vouloir quitter ?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

#classe du formulaire
class FormUI(QWidget):
    def __init__(self, parent):
        super(FormUI,self).__init__(parent)

        self.genUI()

        self.threadpool = QThreadPool()

    def genUI(self):
        # labels

        self.fName = QLabel('Prénom')
        self.lName = QLabel('Nom')
        self.cardID = QLabel('ID carte')
        self.cardIDLbl = QLabel('Attente lecture')

        # champs textes

        self.fNameTxt = QLineEdit()
        self.lNameTxt = QLineEdit()

        # boutons principaux
        self.sBtn = QPushButton('Sauver')
        self.sBtn.clicked.connect(self.save)
        self.sBtn.setToolTip('Appuyer pour <b>quitter</b> le programme')
        self.sBtn.resize(self.sBtn.sizeHint())
        self.sBtn.setDisabled(True)

        self.gBtn = QPushButton('Lire')
        self.gBtn.clicked.connect(self.readCard)
        self.gBtn.setToolTip('Appuyer pour <b>lire la carte</b>')
        self.gBtn.resize(self.gBtn.sizeHint())

        # definir layout
        self.layout = QGridLayout(self)
        self.layout.setSpacing(10)

        self.layout.addWidget(self.fName, 1, 0)
        self.layout.addWidget(self.fNameTxt, 1, 1)

        self.layout.addWidget(self.lName, 2, 0)
        self.layout.addWidget(self.lNameTxt, 2, 1)

        self.layout.addWidget(self.cardID, 3, 0)
        self.layout.addWidget(self.cardIDLbl, 3, 1)

        self.layout.addWidget(self.gBtn,4,0)
        self.layout.addWidget(self.sBtn, 4, 1)

    def readCard(self):
        #movie = QMovie('loading.gif')
        #self.cardIDLbl.setMovie(movie)
        #movie.start()
        #self.cardIDLbl.setLayout(QHBoxLayout())
        #self.cardIDLbl.layout().addWidget(QLabel('Lecture...'))
        self.cardIDLbl.setText('lecture...')
        worker = CardWorker()
        worker.signals.result.connect(self.displayID)
        worker.signals.error.connect(self.displayError)
        self.threadpool.start(worker)

    def save(self):
        worker = DataWorker('save',(self.fNameTxt.text(),self.lNameTxt.text(),self.cardIDLbl.text()))
        self.threadpool.start(worker)
        worker.signals.finished.connect(self.dataSaved)

    def dataSaved(self):
        print ('Card saved !')

    def displayID(self,s):
        self.cardIDLbl.setStyleSheet("color: rgb(0, 0, 255);")
        self.cardIDLbl.setText(s)
        self.sBtn.setDisabled(False)

    def displayError(self,e):
        self.cardIDLbl.setStyleSheet("color: rgb(255, 0, 0);")
        self.cardIDLbl.setText(e[1])