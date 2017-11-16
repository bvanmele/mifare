from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, pyqtSlot, QThread
from smartcard.Exceptions import NoCardException
from smartcard.System import readers
from smartcard.util import toHexString


class CardWorkerSignals(QObject):
    finished = pyqtSignal()

    error = pyqtSignal(tuple)

    result = pyqtSignal(object)

#Thread pour la lecture de carte
class CardWorker(QRunnable):
    def __init__(self):
        super(CardWorker,self).__init__()
        self.signals = CardWorkerSignals()


    @pyqtSlot()
    def run(self):
        found= False
        for reader in readers():
            try:
                connection = reader.createConnection()
                connection.connect()
                ATR = toHexString(connection.getATR())
                APDU = [0xFF,0xCA,0x00,0x00,0x00]
                data, sw1, sw2 = connection.transmit(APDU)
                UID= toHexString(data)
            except NoCardException:
                print(reader, 'no card inserted')

            except:
                self.signals.error.emit((reader, 'error !!'))

            else:
                found= True
                self.signals.result.emit(UID)

            finally:
                QThread.sleep(2)
        if(found):
            self.signals.finished.emit()
        else:
            self.signals.error.emit((reader,'aucune carte à proximité ou insérée !!!'))