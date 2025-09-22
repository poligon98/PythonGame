import pygame
import sys

pygame.init()

TILE_SIZE = 24
ROWS, COLS = 27, 21
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE

# Set up screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()
FPS = 10

maze = [
    "#####################",
    "#.........#.........#",
    "#.###.###.#.###.###.#",
    "#.#i#.#i#.#.#i#.#i#.#",
    "#.###.###.#.###.###.#",
    "#...................#",
    "#.###.#.#####.#.###.#",
    "#.###.#.#####.#.###.#",
    "#.....#...#...#.....#",
    "#####.###.#.###.#####",
    "    #.#       #.#    ",
    "    #.# #bbb# #.#    ",
    "#####.# #   # #.#####",
    "......  #   #  ......",
    "#####.# #   # #.#####",
    "    #.# ##### #.#    ",
    "    #.#       #.#    ",
    "#####.###.#.###.#####",
    "#.....#...#...#.....#",
    "#.###.#.#####.#.###.#",
    "#.###.#.#####.#.###.#",
    "#...................#",
    "#.###.###.#.###.###.#",
    "#.# #.# #.#.# #.# #.#",
    "#.###.###.#.###.###.#",
    "#.........#.........#",
    "#####################"
]

def DisplayMaze():
    for row in range(ROWS):
        for col in range(COLS):
            tile = maze[row][col]
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if tile == '#':
                pygame.draw.rect(screen, (52, 52, 255), (x, y, TILE_SIZE, TILE_SIZE))
            elif tile == '.':
                # We put the white dots for the pac man to eat
                pygame.draw.circle(screen, (255, 255, 255), (x +(TILE_SIZE//2), y+(TILE_SIZE//2)), 3)
            elif tile == 'b':
                # Gate
                pygame.draw.rect(screen, (52, 52, 255), (x, y + 7.5, TILE_SIZE, TILE_SIZE - 15))

# Processing Functions

# Game Loop



while True:
    DisplayMaze()
    pygame.display.flip()
    # Input
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: sys.exit()
            elif event.key == pygame.K_a: pass
            elif event.key == pygame.K_s: pass
            elif event.key == pygame.K_w: pass
            elif event.key == pygame.K_d: pass
        elif event.type == pygame.QUIT: sys.exit()


    # Other process
    # Display scene
    # Game over condition

    clock.tick(FPS)
