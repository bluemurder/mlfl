import sys
from PyQt4 import QtGui, QtCore # importiamo i moduli necessari

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self) # da porre sempre all'inizio
        # inizializza alcuni metodi importanti come resize

        self.resize(350, 250) # ridimensiona la finestra
        self.setWindowTitle('MainWindow')

        self.statusBar().showMessage('Messaggio') # crea una veloce barra di stato

app = QtGui.QApplication(sys.argv)
main = MainWindow()
main.show()
sys.exit(app.exec_())
