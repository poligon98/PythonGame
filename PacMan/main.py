import pygame
import sys
import random
from pygame import Vector2

pygame.init()

TILE_SIZE = 24
ROWS, COLS = 27, 21
WIDTH, HEIGHT = COLS * TILE_SIZE, ROWS * TILE_SIZE

# Set up screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

clock = pygame.time.Clock()
FPS = 10

start_x = 10
start_y = 21

pac = pygame.Rect(start_x * 24, start_y * 24, 24, 24)
pacGrid = [start_x, start_y]
pacPosit = [pac.x, pac.y]
#####
pacCurrentDir = Vector2(1, 0) # start off right first
RED_GHOST_IMAGE = pygame.image.load('red_ghost.png').convert_alpha()
PINK_GHOST_IMAGE = pygame.image.load('pink_ghost.png').convert_alpha()
#####
# . - Dots
# # - Walls
# b - Gate
maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
    ["#", ".", "#", "#", "#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#", "#", "#", ".", "#"],
    ["#", ".", "#", " ", "#", ".", "#", " ", "#", ".", "#", ".", "#", " ", "#", ".", "#", " ", "#", ".", "#"],
    ["#", ".", "#", "#", "#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#", "#", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
    ["#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#"],
    ["#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", "#", ".", ".", ".", "#", ".", ".", ".", "#", ".", ".", ".", ".", ".", "#"],
    ["#", "#", "#", "#", "#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#", "#", "#", "#", "#"],
    [" ", " ", " ", " ", "#", ".", "#", " ", " ", " ", " ", " ", " ", " ", "#", ".", "#", " ", " ", " ", " "],
    [" ", " ", " ", " ", "#", ".", "#", " ", "#", "b", "b", "b", "#", " ", "#", ".", "#", " ", " ", " ", " "],
    ["#", "#", "#", "#", "#", ".", "#", " ", "#", " ", " ", " ", "#", " ", "#", ".", "#", "#", "#", "#", "#"],
    ["#", ".", ".", ".", ".", ".", " ", " ", "#", " ", " ", " ", "#", " ", " ", ".", ".", ".", ".", ".", "#"],
    ["#", "#", "#", "#", "#", ".", "#", " ", "#", " ", " ", " ", "#", " ", "#", ".", "#", "#", "#", "#", "#"],
    [" ", " ", " ", " ", "#", ".", "#", " ", "#", "#", "#", "#", "#", " ", "#", ".", "#", " ", " ", " ", " "],
    [" ", " ", " ", " ", "#", ".", "#", " ", " ", " ", " ", " ", " ", " ", "#", ".", "#", " ", " ", " ", " "],
    ["#", "#", "#", "#", "#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#", "#", "#", "#", "#"],
    ["#", ".", ".", ".", ".", ".", "#", ".", ".", ".", "#", ".", ".", ".", "#", ".", ".", ".", ".", ".", "#"],
    ["#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#"],
    ["#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
    ["#", ".", "#", "#", "#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#", "#", "#", ".", "#"],
    ["#", ".", "#", " ", "#", ".", "#", " ", "#", ".", "#", ".", "#", " ", "#", ".", "#", " ", "#", ".", "#"],
    ["#", ".", "#", "#", "#", ".", "#", "#", "#", ".", "#", ".", "#", "#", "#", ".", "#", "#", "#", ".", "#"],
    ["#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]


class pellet(pygame.sprite.Sprite):
    def __init__(self, col, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


pellets = pygame.sprite.Group()

class Ghost:
    ghosts = []

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    ]

    def __init__(self, sprite, x, y):
        self.sprite = pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
        self.x = x
        self.y = y
        self.grid = [x // TILE_SIZE, y // TILE_SIZE]  # grid coords
        self.dir = (1, 0)  # move right by default
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        Ghost.ghosts.append(self)  # append into instance class

    # Check which directions are available
    def available_moves(self, maze):
        moves = []
        for dx, dy in Ghost.directions:
            nx, ny = self.grid[0] + dx, self.grid[1] + dy

            if maze[ny][nx] != "#":
                moves.append((dx, dy))

        return moves

    # Choosing which moves using available_moves
    def choose_move(self, maze):
        moves = self.available_moves(maze)

        reverse = (-self.dir[0], -self.dir[1])
        if reverse in moves and len(moves) > 1:
            moves.remove(reverse)

        # Update direction
        self.dir = random.choice(moves)

    # Updating instance info to actually move
    def move(self):
        self.grid[0] += self.dir[0]
        self.grid[1] += self.dir[1]
        self.x = self.grid[0] * TILE_SIZE
        self.y = self.grid[1] * TILE_SIZE
        self.rect.topleft = (self.x, self.y)

#####
    def draw(self):
        screen.blit(self.sprite, (self.x, self.y), area=(0, 0, TILE_SIZE, TILE_SIZE))
#####

def DisplayMaze():
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            tile = maze[row][col]
            x, y = col * TILE_SIZE, row * TILE_SIZE
            if tile == '#':
                # wall
                pygame.draw.rect(screen, (52, 52, 255), (x, y, TILE_SIZE, TILE_SIZE))
            elif tile == '.':
                # pellet
                pel = pellet("white", x + (TILE_SIZE // 2), y + (TILE_SIZE // 2))
                pellets.add(pel)
                pellets.update(pac, maze)
                pellets.draw(screen)
            elif tile == 'b':
                # Gate
                pygame.draw.rect(screen, (52, 52, 255), (x, y + 7.5, TILE_SIZE, TILE_SIZE - 15))


# Game Loop
ghosts = [
    Ghost(RED_GHOST_IMAGE, 10 * TILE_SIZE, 10 * TILE_SIZE),
    Ghost(PINK_GHOST_IMAGE, 9 * TILE_SIZE, 12 * TILE_SIZE)
]
while True:
    screen.fill((0, 0, 0))
    for pel in pellets:
        pel.kill()
    DisplayMaze()

    for ghost in ghosts:
        if ghost.x % TILE_SIZE == 0 and ghost.y % TILE_SIZE == 0:
            ghost.choose_move(maze)

        ghost.move()

    for ghost in ghosts:
        ghost.draw()
        #pygame.draw.rect(screen, (255, 0, 0), (ghost.x, ghost.y, TILE_SIZE, TILE_SIZE))

######
    # Input
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_a:
                if maze[pacGrid[1]][pacGrid[0] - 1] != "#":
                    pacCurrentDir = Vector2(-1, 0)
            elif event.key == pygame.K_s:
                if maze[pacGrid[1] + 1][pacGrid[0]] != "#":
                    pacCurrentDir = Vector2(0, 1)
            elif event.key == pygame.K_w:
                if maze[pacGrid[1] - 1][pacGrid[0]] != "#":
                    pacCurrentDir = Vector2(0, -1)
            elif event.key == pygame.K_d:
                if maze[pacGrid[1]][pacGrid[0] + 1] != "#":
                    pacCurrentDir = Vector2(1, 0)
        elif event.type == pygame.QUIT:
            sys.exit()

    # player movement

    if maze[pacGrid[1] + int(pacCurrentDir.y)][pacGrid[0] + int(pacCurrentDir.x)] != "#":
        pacPosit[1] += int(24*pacCurrentDir.y)
        pacGrid[1] += int(pacCurrentDir.y)
        pacGrid[0] += int(pacCurrentDir.x)
        pacPosit[0] += int(24*pacCurrentDir.x)
#####

    pac.y = pacPosit[1]
    pac.x = pacPosit[0]

    if maze[pacGrid[1]][pacGrid[0]] == ".":
        maze[pacGrid[1]][pacGrid[0]] = " "

    for ghost in ghosts:
        if pac.colliderect(ghost.rect):
            print("GAME OVER")
            pygame.quit()
            sys.exit()

    # Other process
    # Display scene
    # Game over condition

    pygame.draw.rect(screen, (255, 255, 0), pac)
    pygame.display.flip()
    clock.tick(FPS)
