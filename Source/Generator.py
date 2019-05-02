import time
import random
import numpy as np
from PIL import Image, ImageOps

class ShipGenerator:
    def __init__(self):
        self.name = "!ERROR!-ShipNameNotFound"
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

    def randomShipName(self):
        shipNames = ["Bebop", "Daedalus", "Explorer", "X-71s", "Mayflower One", "Excelsior", "Anastasia",
                     "F-302 Mongoose", "Odyssey", "Scorpio E-X-1", "Zero-X", "Athena", "Avalon", "Axiom",
                     "Hyperion", "Nemesis", "Prometheus", "SDF-1 Macross", "Red Dwarf"]
        self.name = shipNames[random.randrange(0, shipNames.__len__())]

    # Picks a random colour scheme and applies it to the ship
    def changeTheColour(self, spaceShipImage):
        # Setup
        i = 0
        square = 16
        amountOfColours = 6
        amountOfSchemes = 5

        defaultScheme = (i * square, square * 13)
        randomColourScheme = random.randint(1, amountOfSchemes)
        partsImg = self.shipPartsImg.load()
        shipImg = spaceShipImage.load()

        colourPointerPos = defaultScheme
        currentColour = partsImg[colourPointerPos]

        colourPointerPos = (0, square * randomColourScheme + square * 13)
        newColour = partsImg[colourPointerPos]


        while i < amountOfColours:
            colourPointerPos = (i * square, square * 13)
            currentColour = partsImg[colourPointerPos]

            colourPointerPos = (i * square, square * randomColourScheme + square * 13)
            newColour = partsImg[colourPointerPos]

            # Change every pixel colour of the spaceShip Image
            for pixelX in range(spaceShipImage.size[0]):
                for pixelY in range(spaceShipImage.size[1]):
                    if shipImg[pixelX, pixelY] == currentColour:
                        if newColour == (0,0,0,255):
                            newColour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
                        else:
                            shipImg[pixelX, pixelY] = newColour
            i += 1

        # Return the new coloured spaceship
        return spaceShipImage

    # Creates a ship made of defined parts
    def generateSpaceShip(self, seed):
        random.seed(seed)
        square = 16
        self.randomShipName()

        # Sizes for each spaceship section
        cockPitSection = 0
        mainHaulSection = square * 3
        thrusterSection = square * 6
        wingSection = square * 9

        cockPitSize = (square * 3, square * 2)
        mainHaulSize = (square * 3, square * 2)
        thrusterSize = (square * 3, square * 2)
        wingSize = (square * 2, square * 3)

        # The pointer position on the canvas choosing a random part to be used
        pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)
        newCockpit = self.shipPartsImg.crop(
            (pointerPos, cockPitSection, pointerPos + cockPitSize[0], cockPitSection + cockPitSize[1]))

        pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)
        newMainHull = self.shipPartsImg.crop(
            (pointerPos, mainHaulSection, pointerPos + mainHaulSize[0], mainHaulSection + mainHaulSize[1]))

        pointerPos = (cockPitSize[0] + square) * random.randint(1, 3)
        newThruster = self.shipPartsImg.crop(
            (pointerPos, thrusterSection, pointerPos + thrusterSize[0], thrusterSection + thrusterSize[1]))

        pointerPos = (wingSize[0] + square) * random.randint(1, 5)
        newWing1 = self.shipPartsImg.crop(
            (pointerPos, wingSection, pointerPos + wingSize[0], wingSection + wingSize[1]))
        newWing2 = ImageOps.mirror(newWing1)

        # Parts positions to put a ship together
        cockPitPos = (32, 0)
        mainHaulPos = (32, 32)
        thrusterPos = (32, 64)
        wingPos1 = (0, 16)
        wingPos2 = (64 + 16, 16)

        # Paste new parts to make the new random ship
        newShip = Image.new('RGBA', self.SpaceShipSize)
        newShip.paste(newCockpit, cockPitPos)
        newShip.paste(newMainHull, mainHaulPos)
        newShip.paste(newThruster, thrusterPos)
        newShip.paste(newWing1, wingPos1)
        newShip.paste(newWing2, wingPos2)

        # Change the colour of the Ship
        newShip = self.changeTheColour(newShip)

        # Resize the ship
        newShip = newShip.resize(self.newSpaceShipSize, Image.NEAREST)

        # Save the ship
        newShip.save(self.newShipOutput)