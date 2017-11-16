import sqlite3

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QTableWidget, QDialog, QPushButton, QVBoxLayout, QTableWidgetItem, QSizePolicy, \
    QAbstractItemView

from workers.data import DataWorker


class cardList(QDialog):
    def __init__(self):
        super(cardList,self).__init__()
        self.init_ui()
        self.populate()

    def init_ui(self):
        self.table = QTableWidget(self)
        #self.table.setDisabled(True)
        self.button =  QPushButton(self)
        self.button.setText('Fermer')
        self.vboxlayout = QVBoxLayout(self)

        self.vboxlayout.addWidget(self.table)
        self.vboxlayout.addWidget(self.button)

        self.setLayout(self.vboxlayout)
        self.setWindowTitle('Liste des cartes enregistrées')
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        self.threadpool = QThreadPool()

    def populate(self):
        worker = DataWorker('export',None)

        worker.signals.result.connect(self.bind)
        self.threadpool.start(worker)


    def bind(self,data):

        self.data = data
        self.table.setColumnCount(3)


        self.table.setRowCount(self.data.__len__())

        # print('Nombre: ',data.__len__())

        rowId = 0
        for row in self.data:
            self.table.setItem(rowId, 0, QTableWidgetItem(row[0]))
            self.table.setItem(rowId, 1, QTableWidgetItem(row[1]))
            self.table.setItem(rowId, 2, QTableWidgetItem(row[2]))
            rowId += 1

        # colonnes headers
        self.table.setHorizontalHeaderLabels(['Prénom', 'Nom', 'Identifiant'])

        # lecture seule
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)




