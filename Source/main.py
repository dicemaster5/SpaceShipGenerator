import sys
from Generator import ShipGenerator
from PyQt5 import QtGui, uic, QtWidgets

# ========================= PYQT WINDOW CODE ====================== #

# Get UI file and load as window.
qtCreatorFile = "mainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Initialise the ShipGenerator class
randShip = ShipGenerator()

# PyQT application.
class QtWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # User Buttons that do stuff
        self.RandoButton.clicked.connect(lambda: self.GenerateShipButton())
        self.SeedInput.returnPressed.connect(lambda: self.GenerateShipWithSeed())

    # Function that generates a random ship based of a random seed
    def GenerateShipButton(self):
        try:
            randShip.randomSeed()
            randShip.generateSpaceShip(randShip.shipSeed)
            self.SeedInput.setText(randShip.shipSeed)
            self.ShipName.setText(randShip.name)
            self.ShipView.setPixmap(QtGui.QPixmap("ShipParts/out.png"))
        except Exception as err:
            print(err)

    # Function to generate a ship with a seed specified by the user
    def GenerateShipWithSeed(self):
        try:
            randShip.shipSeed = self.SeedInput.text()
            print(randShip.shipSeed)

            randShip.generateSpaceShip(randShip.shipSeed)
            self.ShipView.setPixmap(QtGui.QPixmap("ShipParts/out.png"))
            self.ShipName.setText(randShip.name)
        except Exception as err:
            print(err)

# MAIN
if __name__ == "__main__":
    if True:
        # Create qtApplication
        app = QtWidgets.QApplication(sys.argv)

        # Create and show qtWindow
        window = QtWindow()
        window.show()

        # Event loop
        sys.exit(app.exec_())