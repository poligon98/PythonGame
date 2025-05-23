from pygame.math import Vector2

class Grids:
    def __init__(self,  cellSize=25, numCellsHigh=25, numCellsWide=20):
        self.coords = []
        for i in range(numCellsWide):
            self.coords.append([Grid(Vector2(i, j), cellSize=cellSize) for j in range(numCellsHigh)])
            
class Grid:
    def __init__(self, coord, cellSize=25):
        self.size = cellSize
        if ((coord.x % 2) and not (coord.y % 2)) or (not (coord.x % 2) and (coord.y % 2)):
            self.color = (144, 208, 144)
        else:
            self.color = (144, 238, 144)