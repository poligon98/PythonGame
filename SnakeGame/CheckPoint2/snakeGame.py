import pygame
import sys
from pygame.math import Vector2
from model import Snake, Apple
from grid import Grids
from utils import draw

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

        # Load in the grid and the models
        self.snake = Snake()
        self.grids = Grids()

    
    # Input Handling
    def inputHandling(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                # 0 -- Quit
                if event.key == (pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # Click on the screen
                elif event.key == pygame.BUTTON_LEFT:
                    break
            elif (event.type == pygame.QUIT):
                pygame.quit()
                sys.exit()

    # Game Process
    def gameProcess(self):
        pass

    # Display on screen
    def displayScreen(self):
        for i, gridRow in enumerate(self.grids.coords):
            for j, grid in enumerate(gridRow):
                draw(Vector2(i, j), self.screen, grid.size, grid.color)
        for coord in self.snake.body:
            draw(coord, self.screen, self.snake.size, self.snake.color)
        pygame.display.update()

    # Game Loop
    def gameLoop(self):
        self.inputHandling()
        self.gameProcess()
        self.displayScreen()
        self.clock.tick(self.gameSpeed)

if __name__ == "__main__":
    game = SnakeGame()
    while True:
        game.gameLoop()

