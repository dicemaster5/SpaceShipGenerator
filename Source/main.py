import sys
from Generator import ShipGenerator
from PyQt5 import QtGui, uic, QtWidgets

# ========================= PYQT WINDOW CODE ====================== #

# Get UI file and load as window.
qtCreatorFile = "mainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

randShip = ShipGenerator()

# PyQT application.
class QtWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.RandoButton.clicked.connect(lambda: self.GenerateShipButton())
        self.SeedInput.returnPressed.connect(lambda: self.GenerateShipWithSeed())

    def GenerateShipButton(self):
        randShip.randomSeed()
        randShip.generateSpaceShip(randShip.shipSeed)
        self.SeedInput.setText(randShip.shipSeed)
        self.ShipName.setText(randShip.name)
        self.ShipView.setPixmap(QtGui.QPixmap("ShipParts/out.png"))
        #print(randShip.shipSeed)

    def GenerateShipWithSeed(self):
        randShip.shipSeed = self.SeedInput.text()
        print(randShip.shipSeed)

        randShip.generateSpaceShip(randShip.shipSeed)
        self.ShipView.setPixmap(QtGui.QPixmap("ShipParts/out.png"))
        self.ShipName.setText(randShip.name)






if __name__ == "__main__":
    if True:
        # Create qtApplication
        app = QtWidgets.QApplication(sys.argv)

        # Create and show qtWindow
        window = QtWindow()
        window.show()

        # Event loop
        sys.exit(app.exec_())