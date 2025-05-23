import pygame
from pygame import Vector2
import random

def randomCoord(maxX, maxY,notCoords=[]):
    while True:
        randomX = random.randrange(maxX)
        randomY = random.randrange(maxY)
        randomCoord = Vector2(randomX, randomY)
        if randomCoord not in notCoords:
            break
    return randomCoord

def draw(coord, screen, size, sprite):
    rect = pygame.Rect(coord.x*size, coord.y*size, size, size) # (startingX, startingY, lengthX, lengthY)
    pygame.draw.rect(screen, sprite, rect)