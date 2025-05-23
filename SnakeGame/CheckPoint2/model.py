from pygame.math import Vector2
from utils import randomCoord

class Snake:
    color = (88, 99, 255)
    def __init__(self, cellSize=25, numCellsHigh=25, numCellsWide=20):
        self.startCoord = randomCoord(numCellsWide - 4, numCellsHigh)
        self.body = [Vector2(self.startCoord.x + 3 - i, self.startCoord.y) for i in range(4)]
        self.direction = 0 # we will set this later
        self.size = cellSize

class Apple:
    def __init__(self):
        self.color
        self.size
        self.coord