import sys
import time
import random
import numpy as np
from PIL import Image, ImageOps
from PyQt5 import QtCore, QtGui, uic, QtWidgets

# ========================= PYQT WINDOW CODE ====================== #

# Get UI file and load as window.
qtCreatorFile = "mainWindow.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# PyQT application.
class QtWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.RandoButton.clicked.connect(lambda: self.UpdateImageEvent())

    def UpdateImageEvent(self):
        generateSpaceShipImage()
        self.ShipView.setPixmap(QtGui.QPixmap("ShipParts/out.png"))

def generateSpaceShipImage():
    random.seed(time.time())
    square = 16

    cockPitSection = 0
    mainHaulSection = square * 3
    thrusterSection = square * 6
    wingSection = square * 9

    shipPartsImg = Image.open("ShipParts/ShipParts.png")

    cockPitSize = (square * 3, square * 2)
    mainHaulSize = (square * 3, square * 2)
    thrusterSize = (square * 3, square * 2)
    wingSize = (square * 2, square * 3)

    pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)
    # Areas to crop at -- NEEDS TO BE RANDOM! --
    newCockpit = shipPartsImg.crop((pointerPos, cockPitSection, pointerPos + cockPitSize[0], cockPitSection + cockPitSize[1]))

    random.seed()
    pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)
    newMainHull = shipPartsImg.crop((pointerPos, mainHaulSection, pointerPos + mainHaulSize[0], mainHaulSection + mainHaulSize[1]))
    random.seed()
    pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)
    newThruster = shipPartsImg.crop((pointerPos, thrusterSection, pointerPos + thrusterSize[0], thrusterSection + thrusterSize[1]))
    random.seed()
    pointerPos = (wingSize[0] + square) * random.randint(1, 4)
    newWing1 = shipPartsImg.crop((pointerPos, wingSection, pointerPos + wingSize[0], wingSection + wingSize[1]))
    newWing2 = ImageOps.mirror(newWing1)

    # Parts positions to put a ship together
    cockPitPos = (32, 0)
    mainHaulPos = (32, 32)
    thrusterPos = (32, 64)
    wingPos1 = (0, 16)
    wingPos2 = (64 + 16, 16)

    # Paste new parts to make ship
    newShip = Image.new('RGBA', (112, 112))
    newShip.paste(newCockpit, cockPitPos)
    newShip.paste(newMainHull, mainHaulPos)
    newShip.paste(newThruster, thrusterPos)
    newShip.paste(newWing1, wingPos1)
    newShip.paste(newWing2, wingPos2)

    newShip = newShip.resize((224, 224), Image.NEAREST)
    newShip.save("ShipParts/out.png")


    # CHANGE COLOUR
    im = Image.open("ShipParts/out.png")
    im = im.convert('RGBA')

    data = np.array(im)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    pink_areas = (red == 255) & (blue == 147) & (green == 20)
    random.seed()
    data[..., :-1][pink_areas.T] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Transpose back needed

    im2 = Image.fromarray(data)
    im2.save("ShipParts/out.png")

if __name__ == "__main__":
    if True:
        # Create qtApplication
        app = QtWidgets.QApplication(sys.argv)

        # Create and show qtWindow
        window = QtWindow()
        window.show()

        # main()
        #clientData.currentBackgroundThread = threading.Thread(target=backgroundThread, args=(clientData,))
        #clientData.currentBackgroundThread.start()

        # Event loop
        sys.exit(app.exec_())