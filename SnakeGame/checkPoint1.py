import pygame
from pygame.math import Vector2
import sys

pygame.init()

class SnakeGame:
    def __init__(self):
        # Creating Display
        self.cellSize = 25 # How wide will each square be
        self.numCellsHigh = 25 # How high the screen be (in number of cells)
        self.numCellsWide = 20 # How high the screen be (in number of cells)

        self.screenHeight = self.cellSize * self.numCellsHigh 
        self.screenWidth = self.cellSize * self.numCellsWide

        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screenColor = (175, 215, 70) 
        pygame.display.set_caption("Snake Game") # Name of the game

        self.clock = pygame.time.Clock()
        self.gameSpeed = 10 #in fps
    
    # Game Process
    def gameProcess(self):
        pass

    # Display on screen
    def displayScreen(self):
        pass

    # Game Loop
    def gameLoop(self):
        self.gameProcess()
        self.displayScreen()
        self.clock.tick(self.gameSpeed)

if __name__ == "__main__":
    game = SnakeGame()
    while True:
        game.gameLoop()

