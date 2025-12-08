#---- 0: Library Importation ---- #
import pygame  # The game library - handles graphics, input, sound
import random  # For random numbers (to make obstacles unpredictable)
import sys  # For exiting the program cleanly
from collections import deque  # Helps us alternate obstacle patterns cleanly
from pygame import Vector2  # Vector2 stores x and y coordinates together

# ---- 0: Initialise Pygame ---- #
pygame.init() # Get pygame library to work

# ============================================================================
# STEP 1: SET UP THE GAME WINDOW
# ============================================================================
SCREEN_WIDTH = 1000  # How wide the window is (left to right)
SCREEN_HEIGHT = 600  # How tall the window is (top to bottom)
# Create the actual window that will show our game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Geometry Dash - Kids Edition")  # Title at top of window

# ============================================================================
# STEP 2: SET UP THE GAME CLOCK
# ============================================================================
clock = pygame.time.Clock() # Clock - control how fast the game runs
FPS = 60  # FPS = Frames Per Second (how many times we redraw the screen per second) -- same as our eyesight

# ============================================================================
# STEP 3: DEFINE COLORS
# ============================================================================
# Colors in pygame use RGB (Red, Green, Blue) values from 0-255
# Think of it like mixing paint: (255, 0, 0) = pure red, (0, 255, 0) = pure green
WHITE = (255, 255, 255)  # All colors at max = white
BLACK = (0, 0, 0)  # All colors at zero = black
SKY_BLUE = (20, 130, 200)  # A nice sky blue color
GROUND_COLOR = (50, 50, 50)  # Dark gray for the ground
PLAYER_COLOR = (255, 200, 50)  # Yellow/orange for the player
OBSTACLE_COLOR = (200, 50, 50)  # Red for obstacles
HITBOX_COLOR = (255, 0, 0)  # Bright red for hitboxes (collision boxes)

# ============================================================================
# STEP 4: OTHER GAME SETTING CONSTANTS
# ============================================================================
# Game constants
GROUND_Y = 450  # Where the ground starts (y coordinate - remember y goes down!)
GRAVITY = 3000  # How strong gravity is (bigger number = stronger gravity)
JUMP_VELOCITY = -1000  # How fast the player jumps up (negative = up, positive = down)
GAME_SPEED = 450.0 # How fast the obstacles shift
# Platform Constants
PLATFORM_HEIGHT = 20  # Thickness of each floating platform
PLATFORM_WIDTH_RANGE = (160, 240)  # Reasonable platform widths
# Obstacle Constants
SPIKE_WIDTH_RANGE = (45, 75)  # Ground spike width range
SPIKE_HEIGHT_RANGE = (60, 110)  # Ground spike height range
MIN_GAP_BETWEEN_OBSTACLES = 200  # Minimum spacing between any two spawns (pixels)

# ============================================================================
# STEP 5: LOAD IMAGES (OPTIONAL)
# ============================================================================
# Simply try to load the image and prevent an error if the image is not found
def try_load(path):
    try:
        surf = pygame.image.load(path).convert_alpha()  # convert_alpha makes transparent parts work
        return surf
    except IOError:
        return None # If something goes wrong (file doesn't exist), return None

PLAYER_IMG = try_load("player.png")
GROUND_IMG = try_load("ground.png")
TRIANGLE_IMG = try_load("triangle.png")

# ============================================================================
# STEP 6: UTILS FUNCTION
# ============================================================================
def draw_text(surf, text, x, y, size=24, color=WHITE):
    # Create a font object (the style of text)
    font = pygame.font.SysFont(None, size)
    # Render the text (turn it into an image we can draw)
    img = font.render(text, True, color)
    # Draw it on the screen (blit = "copy pixels onto screen")
    surf.blit(img, (x, y))

# ============================================================================
# STEP 7: PLAYER CLASS
# ============================================================================
class Player:
    def __init__(self, x: int, y: int, size):
        # Store position as a Vector2 - this is like storing (x, y) together
        self.pos = Vector2(x, y)  # Current position of the player
        self.size = size # Store the size (we'll make a square player)

        # Create a rectangle for collision detection
        # pygame.Rect is like an invisible box we use to check if things touch
        self.rect = pygame.Rect(x, y, size, size)

        # ===== PHYSICS VARIABLES =====
        # 0 = not moving, negative = going up, positive = going down
        self.vel_y = 0.0  # Vertical velocity (how fast moving up/down)

        self.on_ground = True  # Are we touching the ground? (True = yes, False = no)

        # ===== IMAGE/SPRITE =====
        # If we have an image file, use it. Otherwise, we'll draw a rectangle
        if PLAYER_IMG:
            # Scale the image to match the player's size
            self.image = pygame.transform.scale(PLAYER_IMG, (size, size))
        else:
            self.image = None  # No image, so we'll draw a shape instead

    def jump(self):
        # Jump when the player is on the ground
        if self.on_ground:  # Only jump if we're touching the ground
            self.vel_y = JUMP_VELOCITY  # Set upward velocity (negative = up)
            self.on_ground = False  # We're now in the air

    def update(self, dt, game=None, platforms=None):
        # What we do to the player for every frame
        # ===== APPLY GRAVITY =====
        # Gravity pulls the player down, so we add it to velocity (it's a type of acceleration)
        if self.on_ground == False:
            self.vel_y += GRAVITY * dt # Apply gravity only if you are not on the ground

        # todo

        # ===== UPDATE POSITION =====
        # Move the player based on velocity
        # If vel_y is negative (going up), pos.y decreases (moves up)
        # If vel_y is positive (going down), pos.y increases (moves down)
        self.pos.y += self.vel_y * dt

        # ===== CHECK PLATFORM COLLISIONS =====
        # First check if we're landing on a platform
        self.on_ground = False  # Start by assuming we're in the air

        if platforms:
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                    self.vel_y = 0.0
                    self.pos.y = platform.rect.top - self.size + 1
                    self.on_ground = True
                    print("Collide!")
                    break

        # ===== CHECK IF HITTING THE GROUND =====
        # Only check ground if we're not on a platform
        if not self.on_ground:
            ground_top = GROUND_Y - self.size  # Top of ground minus player height

            if self.pos.y >= ground_top:  # If we've fallen through or hit the ground
                self.pos.y = ground_top
                self.on_ground = True
                self.vel_y = 0.0  # Stop falling

        # ===== UPDATE COLLISION RECTANGLE =====
        # Update the invisible collision box to match where the player actually is
        # We use int() because pygame needs whole numbers for rectangles
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def draw(self, surf):
        if self.image:
            # If we have an image, draw it
            surf.blit(self.image, self.rect.topleft)
        else:
            # No image, so draw a colored rectangle instead
            pygame.draw.rect(surf, OBSTACLE_COLOR, self.rect)

# ============================================================================
# STEP 8: GAME OBJECT CLASS (Parent Class)
# ============================================================================
class GameObject:
    speed = GAME_SPEED
    def __init__(self, pos: Vector2, size: Vector2, sprite):
        self.pos = pos
        self.size = size
        self.sprite = sprite

    def update(self, dt):
        """
                Move the obstacle left across the screen.
                dt = time since last frame (for smooth movement)
                """
        # Move left (subtract because x decreases as we go left)
        # Using dt ensures smooth movement at any framerate
        self.pos.x -= self.speed * dt
        # No rect hitbox to update; triangle points calculated on the fly

    def off_screen(self):
        return self.pos.x + self.size.x < 0  # If right edge is past left side of screen

    def draw(self, surf):
        draw_x = int(self.pos.x)  # Use actual position for responsive movement
        if type(self.sprite) == pygame.surface.Surface:
            # Draw the image if we have one
            surf.blit(self.sprite, (draw_x, int(self.pos.y)))
        else:
            color = self.sprite[2]
            # Draw the triangle
            if self.sprite[0] == "Polygon":
                pygame.draw.polygon(surf, color, (self.sprite[1]))
            elif self.sprite[0] == "Rectangle":
                rect = self.sprite[1]
                pygame.draw.rect(surf, color, rect)

# ============================================================================
# STEP 9: SPIKE CLASS
# ============================================================================
class Spike(GameObject):
    def __init__(self, x, width, height):
        if TRIANGLE_IMG:
            self.image = pygame.transform.scale(TRIANGLE_IMG, (width, height))
        else:
            # Draw a triangle using three points
            # Point 1: Top center (the spike point)
            p1 = (int(self.pos.x + self.size.x / 2), int(self.pos.y))
            # Point 2: Bottom left corner
            p2 = (int(self.pos.x), int(self.pos.y + self.size.y))
            # Point 3: Bottom right corner
            p3 = (int(self.pos.x + self.size.x), int(self.pos.y + self.size.y))
            self.image = ["Polygon", (p1, p2, p3), OBSTACLE_COLOR]
        super().__init__(Vector2(x, GROUND_Y - height), Vector2(width, height), self.image)

        # # ===== HITBOX =====
        # Triangle hitbox points for accurate collision
        self.get_p1 = lambda: (int(self.pos.x + self.size.x / 2), int(self.pos.y))  # top
        self.get_p2 = lambda: (int(self.pos.x), int(self.pos.y + self.size.y))  # bottom left
        self.get_p3 = lambda: (int(self.pos.x + self.size.x), int(self.pos.y + self.size.y))  # bottom right

# ============================================================================
# STEP 10: PLATFORM CLASS
# ============================================================================
class Platform(GameObject):
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(int(x), int(y), width, height) # Hitbox
        super().__init__(Vector2(x, y), Vector2(width, height), ["Rectangle", self.rect, GROUND_COLOR])

    def update(self, dt):
        super().update(dt) # don't override
        self.rect.x = int(self.pos.x)

# ============================================================================
# STEP 11: MANAGING GAME OBJECTS
# ============================================================================
class ObjectManager:
    def __init__(self):
        self.pattern = deque(["spike", "platform"])  # simple alternating pattern
        self.min_gap_time = MIN_GAP_BETWEEN_OBSTACLES / GAME_SPEED
        self.timer = 0.0  # spawn immediately when the game starts
        self.spawn_point_x = SCREEN_WIDTH + 50

    def update(self, dt, game):
        # --- Check whether the game has started --- #
        self.timer -= dt
        if self.timer > 0:
            return  # Greater than 0 so don't run the game
        # --- Alternate spikes and platform --- #
        next_type = self.pattern[0]
        self.pattern.rotate(-1)  # alternate spike -> platform -> spike ...
        if next_type == "spike":
            game.obstacles.append(self._spawn_spike())
        else:
            platform_obj, spike_obj = self._spawn_platform()
            game.platforms.append(platform_obj)
            game.obstacles.append(spike_obj)
        # --- Reset timer with a little randomness but never below the minimum gap --- #
        extra_time = random.uniform(0.1, 0.5) * self.min_gap_time
        self.timer = self.min_gap_time + extra_time

    def _spawn_spike(self, width=-1, height=-1):
        # Randomise the width and height of the spike if it is not under the platform using random.randint(number_range)
        width = random.randint(*SPIKE_WIDTH_RANGE) if width == -1 else width
        height = random.randint(*SPIKE_HEIGHT_RANGE) if height == -1 else height
        x = SCREEN_WIDTH + 50  # spawn just off the right edge
        return Spike(self.spawn_point_x, width, height)

    def _spawn_platform(self):
        width = random.randint(*PLATFORM_WIDTH_RANGE) # Randomise the width of the platform
        spike_width, spike_height = 50, 50 # Set the width and height of the spike
        spike_x = self.spawn_point_x + int(width * 0.45) # Set the spawn point of the spike underneath the platform
        return Platform(self.spawn_point_x, GROUND_Y - 90, width, PLATFORM_HEIGHT), Spike(spike_x, spike_width, spike_height)

# ============================================================================
# STEP 12: GROUND DRAWING
# ============================================================================
def draw_ground(surf):
    if GROUND_IMG:
        # --- Draw Repeating Tiles --- #
        # Scale the ground tile image
        tile = pygame.transform.scale(GROUND_IMG, (150, 150))
        tile_w = tile.get_width()  # How wide one tile is
        x = 0 # Set the spawn point
        # Draw repeating tiles
        while x < SCREEN_WIDTH:
            surf.blit(tile, (x, GROUND_Y))  # Draw one tile
            x += tile_w  # Move to next position
    else:
        # No image, so draw a solid rectangle
        pygame.draw.rect(surf, GROUND_COLOR,
                         (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))

# ============================================================================
# STEP 13: GAME CLASS
# ============================================================================
class Game:
    """
    The Game class manages everything in our game.

    It keeps track of:
    - The player
    - All the obstacles
    - The score
    - Whether the game is running or paused

    Think of it as the "manager" that coordinates everything.
    """
    def __init__(self):
        # Create the player at position (80, GROUND_Y - 60) with size 60
        self.player = Player(80, GROUND_Y - 60, 60)

        # Collections that store everything moving in the level
        self.obstacles = []  # ground spikes/triangles
        self.platforms = []  # floating bars the player can land on

        # Dedicated manager that keeps spawn spacing fair
        self.obstacle_manager = ObjectManager()

        # Game state
        self.running = True  # Is the game currently running? (False = player died)
        self.show_hitboxes = True  # Show collision boxes? (like practice mode in real Geometry Dash)

        # Scoring
        self.score = 0  # Current score (increases over time)
        self.best = 0  # Best score this session

    def reset(self):
        # --- Reset the game when 'r' is pressed --- #
        # Create a new player
        self.player = Player(80, GROUND_Y - 60, 60)
        # Clear all obstacles and platforms
        self.obstacles = []
        self.platforms = []
        # Reset score and spawn logic
        self.score = 0
        self.obstacle_manager = ObjectManager()

    def update(self, dt):
        # --- Update the game on every frame --- #
        # ===== UPDATE PLAYER =====
        # Update player's physics (gravity, movement, etc.)
        # Pass platforms so player can land on them
        self.player.update(dt, game=self, platforms=self.platforms)

        # ===== SPAWN LOGIC MANAGED IN ONE PLACE =====
        # The obstacle manager handles alternating spike / platform spawns
        self.obstacle_manager.update(dt, self)

        # ===== UPDATE ALL OBSTACLES =====
        # Move each obstacle left across the screen
        for ob in self.obstacles:
            ob.update(dt)

        # ===== UPDATE ALL PLATFORMS =====
        # Move each platform left across the screen (and update its spikes)
        for platform in self.platforms:
            platform.update(dt)

        # ===== REMOVE OFF-SCREEN OBJECTS =====
        # If an obstacle has left the screen, remove it from the list
        # This keeps our list small and prevents lag
        self.obstacles = [o for o in self.obstacles if not o.off_screen()]
        # Remove off-screen platforms too
        self.platforms = [p for p in self.platforms if not p.off_screen()]
        # This is a "list comprehension" - it's like a for loop that creates a new list
        # It keeps only obstacles/platforms that are still on screen

        # ===== CHECK COLLISIONS =====
        # Check if player hit any obstacle
        for ob in self.obstacles:
            px, py = self.player.rect.centerx, self.player.rect.bottom
            x1, y1 = ob.get_p1()
            x2, y2 = ob.get_p2()
            x3, y3 = ob.get_p3()
            # Reduce hitbox width for spikes (narrower detection)
            margin = (x3 - x2) * 0.15
            if (x2 + margin) <= px <= (x3 - margin):
                # Linear interpolation spike top line
                slope = (y3 - y1) / (x3 - x1)
                spike_top_y = slope * (px - x1) + y1
                # Make spike collision more forgiving (top 10% safe)
                if py > spike_top_y + (y2 - y1) * 0.15:
                    self.best = max(self.best, self.score)
                    self.running = False
                    return

        # ===== UPDATE SCORE =====
        # Score increases over time (survive longer = higher score)
        self.score += dt * 100  # Multiply by 100 to make numbers bigger

    def draw(self, surf):
        """
        Draw everything on the screen.

        Order matters! We draw in this order:
        1. Ground (back)
        2. Platforms (middle-back)
        3. Ground spikes/obstacles (middle-front)
        4. Player (front)
        5. UI text (very front)

        This way the player appears on top of everything.
        """
        # Draw ground first (it's in the background)
        draw_ground(surf)

        # Draw all platforms (platforms and their spikes)
        for platform in self.platforms:
            platform.draw(surf)

        # Draw all obstacles
        for ob in self.obstacles:
            ob.draw(surf)

        # Draw player last (so it appears on top)
        self.player.draw(surf)

        # ===== DRAW UI (User Interface) =====
        # Score display (top left)
        draw_text(surf, f"Score: {int(self.score)}", 12, 12, size=28)

        # Best score display
        draw_text(surf, f"Best: {int(self.best)}", 12, 44, size=20)

        # Instructions (bottom left)
        draw_text(surf, "Space to jump • R to restart after death • H to toggle hitboxes",
                  12, SCREEN_HEIGHT - 28, size=18)

# ============================================================================
# STEP 14: MAIN GAME LOOP
# ============================================================================
def main():
    game = Game() # Create a new Game object
    # Delta time - tracks how much time passed since last frame
    dt = 0.0  # Start at 0

    # ===== THE GAME LOOP =====
    while True:
        # ===== STEP 1: HANDLE INPUTS =====
        # Events are things that happen - like pressing a key or closing the window
        for event in pygame.event.get():
            # Check what type of event it is
            if event.type == pygame.QUIT:
                # Player clicked the X button to close window
                pygame.quit()  # Shut down pygame
                sys.exit()  # Exit the program
            elif event.type == pygame.KEYDOWN:
                # Player pressed a key
                if event.key == pygame.K_ESCAPE:
                    # Escape key = quit game
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    # Space bar = jump!
                    game.player.jump()
                elif event.key == pygame.K_h:
                    # H key = toggle hitboxes (show/hide collision boxes)
                    game.show_hitboxes = not game.show_hitboxes
                elif event.key == pygame.K_r:
                    # R key = restart
                    game.reset()  # Reset everything
                    game.running = True  # Start the game again

        # ===== STEP 2: UPDATE GAME =====
        if game.running:
            # Game is running, so update everything
            # Calculate delta time (how many seconds since last frame)
            dt = clock.tick(FPS) / 1000.0  # tick() returns milliseconds, divide by 1000 for seconds
            game.update(dt)  # Update the game state
        else:
            # Game is paused (player died), but we still need to tick the clock
            # Otherwise things might break
            dt = clock.tick(FPS) / 1000.0

        # ===== STEP 3: DRAW EVERYTHING =====
        screen.fill(SKY_BLUE) # Clear old frame
        game.draw(screen) # Show everything on the frame

        # ===== STEP 4: GAME OVER MESSAGE =====
        if not game.running:
            draw_text(screen, "You Died! Press R to restart",
                      SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 20,
                      size=34, color=BLACK)

        pygame.display.flip()  # Update the frame

# STEP 15: START THE GAME
# This code only runs if we run this file directly (not if we import it)
if __name__ == "__main__":
    main()  # Start the game!
