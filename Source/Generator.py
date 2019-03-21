import time
import random
import numpy as np
from PIL import Image, ImageOps

class ShipGenerator:
    def __init__(self):
        self.name = "THE GREAT SHIP!"
        #self.rooms = {}
        self.shipSeed = ""

        self.shipPartsImg = Image.open("ShipParts/ShipParts.png")
        self.newShipOutput = "ShipParts/out.png"

        self.SpaceShipSize = (112, 112)
        self.newSpaceShipSize = (224, 224)

    def randomSeed(self):
        # Set a seed to do a radnom seed
        # Seedception
        random.seed(int(time.time() * 1000))
        self.shipSeed = str(random.randint(0, 99999999))
        #random.seed(self.shipSeed)


    # Creates a ship made of defined rooms
    def generateSpaceShip(self, seed):
        random.seed(seed)
        square = 16

        cockPitSection = 0
        mainHaulSection = square * 3
        thrusterSection = square * 6
        wingSection = square * 9

        cockPitSize = (square * 3, square * 2)
        mainHaulSize = (square * 3, square * 2)
        thrusterSize = (square * 3, square * 2)
        wingSize = (square * 2, square * 3)

        pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)

        newCockpit = self.shipPartsImg.crop(
            (pointerPos, cockPitSection, pointerPos + cockPitSize[0], cockPitSection + cockPitSize[1]))

        pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)
        newMainHull = self.shipPartsImg.crop(
            (pointerPos, mainHaulSection, pointerPos + mainHaulSize[0], mainHaulSection + mainHaulSize[1]))

        pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)
        newThruster = self.shipPartsImg.crop(
            (pointerPos, thrusterSection, pointerPos + thrusterSize[0], thrusterSection + thrusterSize[1]))

        pointerPos = (wingSize[0] + square) * random.randint(1, 4)
        newWing1 = self.shipPartsImg.crop((pointerPos, wingSection, pointerPos + wingSize[0], wingSection + wingSize[1]))
        newWing2 = ImageOps.mirror(newWing1)

        # Parts positions to put a ship together
        cockPitPos = (32, 0)
        mainHaulPos = (32, 32)
        thrusterPos = (32, 64)
        wingPos1 = (0, 16)
        wingPos2 = (64 + 16, 16)

        # Paste new parts to make ship
        newShip = Image.new('RGBA', self.SpaceShipSize)
        newShip.paste(newCockpit, cockPitPos)
        newShip.paste(newMainHull, mainHaulPos)
        newShip.paste(newThruster, thrusterPos)
        newShip.paste(newWing1, wingPos1)
        newShip.paste(newWing2, wingPos2)

        # CHANGE COLOUR
        data = np.array(newShip)  # "data" is a height x width x 4 numpy array
        red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability

        pink_areas = (red == 255) & (blue == 147) & (green == 20)
        # random.seed()
        data[..., :-1][pink_areas.T] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        newShip = Image.fromarray(data)
        newShip = newShip.resize(self.newSpaceShipSize, Image.NEAREST)
        newShip.save(self.newShipOutput)