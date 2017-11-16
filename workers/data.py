import sqlite3

from datetime import datetime
from PyQt5.QtCore import QRunnable, QObject, pyqtSignal, pyqtSlot


class DataWorkerSignals(QObject):
    finished = pyqtSignal()

    error = pyqtSignal(tuple)

    result = pyqtSignal(object)


class DataWorker(QRunnable):

    def __init__(self,mode,values):
        super(DataWorker,self).__init__()
        self.signals = DataWorkerSignals()
        self.values = values
        self.mode = mode


    @pyqtSlot()
    def run(self):
        db = sqlite3.connect('../mifare_cards.db')

        c= db.cursor()

        if self.mode == 'save':

            row= c.execute("SELECT * FROM users WHERE fname LIKE '{0}' AND lname LIKE '{1}'".format(self.values[0],self.values[1]))
            print (c.rowcount)
            if row:
                print ("There is already a record")



            c = db.cursor()
            c.execute("INSERT or REPLACE INTO users (fname, lname, cardid, modified) VALUES ('{0}','{1}','{2}','{3}')".format(self.values[0],self.values[1],self.values[2],datetime.now()))
            db.commit()

        elif self.mode == 'export':
            data = c.execute('select fname, lname, cardid, modified from users').fetchall()
            self.signals.result.emit(data)

        db.close()
        self.signals.finished.emit()