from __future__ import print_function

import sqlite3,os


import sys


#classe de la fenêtre principale
from PyQt5.QtWidgets import QApplication

from components.gui import GUI


def detectDB(path):

    if os.path.isfile(path) and os.path.getsize(path) > 100:
        with open(path,'r',encoding= "ISO-8859-1") as f:
            header=f.read(100)
            if header.startswith('SQLite format 3'):
                return True
            else:
                return False
    else:
        return False

def createDB(path):
    db = sqlite3.connect('../mifare_cards.db')
    db.execute('CREATE TABLE IF NOT EXISTS users (fname TEXT, lname TEXT, cardid TEXT UNIQUE, modified DATETIME)')
    db.commit()
    db.close()



if __name__ == '__main__':
    if 'win32' == sys.platform:
        print('press Enter to continue')
        sys.stdin.read(1)

    if not detectDB('../mifare_cards.db'):
        print('DB do no exist: creation...')
        createDB('../mifare_cardss.db')


    app = QApplication(sys.argv)
    ex = GUI()
    sys.exit(app.exec_())



