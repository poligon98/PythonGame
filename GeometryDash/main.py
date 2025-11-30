"""
GEOMETRY DASH GAME - For Year 8-10 Students
===========================================


This is a simple side-scrolling game where you jump over obstacles.
Think of it like a simplified version of the popular Geometry Dash game!


WHAT IS PYGAME?
---------------
Pygame is a library (a collection of pre-made code) that helps us make games.
It handles things like drawing graphics, detecting keyboard presses, and managing time.


IMPORTANT CONCEPTS:
------------------
- CLASS: A blueprint for creating objects (like a cookie cutter)
- OBJECT: An instance of a class (like an actual cookie made from the cutter)
- METHOD: A function that belongs to a class
- VECTOR: A way to store x and y coordinates together (like a point on a graph)
- DELTA TIME (dt): How much time passed since the last frame (makes animations smooth)
"""

# ============================================================================
# STEP 1: IMPORT LIBRARIES
# ============================================================================
# These are tools we need to make our game work
import pygame  # The game library - handles graphics, input, sound
import random  # For random numbers (to make obstacles unpredictable)
import sys  # For exiting the program cleanly
from collections import deque  # Helps us alternate obstacle patterns cleanly
from pygame import Vector2  # Vector2 stores x and y coordinates together

# ============================================================================
# STEP 2: INITIALIZE PYGAME
# ============================================================================
# This "starts up" pygame - like turning on a game console
pygame.init()

# ============================================================================
# STEP 3: SET UP THE GAME WINDOW
# ============================================================================
# These numbers control how big our game window is (in pixels)
# Think of pixels like tiny dots on your screen - more pixels = bigger window
SCREEN_WIDTH = 1000  # How wide the window is (left to right)
SCREEN_HEIGHT = 600  # How tall the window is (top to bottom)

# Create the actual window that will show our game
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Geometry Dash - Kids Edition")  # Title at top of window

# ============================================================================
# STEP 4: SET UP THE GAME CLOCK
# ============================================================================
# The clock controls how fast our game runs
clock = pygame.time.Clock()
FPS = 60  # FPS = Frames Per Second (how many times we redraw the screen per second)
# 60 FPS means we update the game 60 times every second - this makes it smooth!


# ============================================================================
# STEP 5: DEFINE COLORS
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
# STEP 6: GAME WORLD SETTINGS
# ============================================================================
GROUND_Y = 450  # Where the ground starts (y coordinate - remember y goes down!)
GRAVITY = 3000  # How strong gravity is (bigger number = stronger gravity)
# This is in "pixels per second squared" - don't worry about the math!
JUMP_VELOCITY = -1000  # How fast the player jumps up (negative = up, positive = down)

# These extra constants make obstacle tuning easy to understand
PLATFORM_Y = GROUND_Y - 90  # Fixed platform height (high enough to jump to)
PLATFORM_HEIGHT = 20  # Thickness of each floating platform
PLATFORM_WIDTH_RANGE = (160, 240)  # Reasonable platform widths
SPIKE_WIDTH_RANGE = (45, 75)  # Ground spike width range
SPIKE_HEIGHT_RANGE = (60, 110)  # Ground spike height range
MIN_GAP_BETWEEN_OBSTACLES = 200  # Minimum spacing between any two spawns (pixels)


# ============================================================================
# STEP 7: LOAD IMAGES (OPTIONAL)
# ============================================================================
# This function tries to load an image file. If it can't find it, it returns None
# This way the game still works even without image files!
def try_load(path):
    """
    Try to load an image file.
    If it works, return the image. If it fails, return None (nothing).
    """
    try:
        # Try to load the image
        surf = pygame.image.load(path).convert_alpha()  # convert_alpha makes transparent parts work
        return surf
    except Exception:
        # If something goes wrong (file doesn't exist), return None
        return None


# Try to load images - if they don't exist, we'll draw shapes instead
PLAYER_IMG = try_load("player.png")
GROUND_IMG = try_load("ground.png")
TRIANGLE_IMG = try_load("triangle.png")


# ============================================================================
# STEP 8: HELPER FUNCTION FOR DRAWING TEXT
# ============================================================================
def draw_text(surf, text, x, y, size=24, color=WHITE):
    """
    Draw text on the screen.

    Parameters:
    - surf: The surface (screen) to draw on
    - text: The words to display (like "Score: 100")
    - x, y: Where to put the text (top-left corner)
    - size: How big the text is
    - color: What color the text is
    """
    # Create a font object (the style of text)
    font = pygame.font.SysFont(None, size)
    # Render the text (turn it into an image we can draw)
    img = font.render(text, True, color)
    # Draw it on the screen (blit = "copy pixels onto screen")
    surf.blit(img, (x, y))


# ============================================================================
# STEP 9: PLAYER CLASS
# ============================================================================
class Player:
    """
    The Player class represents our character in the game.

    Think of a class like a blueprint for making objects.
    This blueprint says "a player has a position, a size, and can jump"

    We use a class because we want to keep all the player's data together
    (like their position, speed, etc.) and all the things they can do
    (like jump, update, draw) in one place.
    """

    def __init__(self, x, y, size):
        """
        This is called when we create a new Player object.
        __init__ is short for "initialize" - it sets up the player when first created.

        Parameters:
        - x: Starting x position (left-right position)
        - y: Starting y position (up-down position)
        - size: How big the player is (width and height)
        """
        # Store position as a Vector2 - this is like storing (x, y) together
        # Vector2 makes it easier to do math with positions
        self.pos = Vector2(x, y)  # Current position of the player

        # Store the size (we'll make a square player)
        self.size = size

        # Create a rectangle for collision detection
        # pygame.Rect is like an invisible box we use to check if things touch
        # We convert to int because pygame needs whole numbers
        self.rect = pygame.Rect(int(x), int(y), size, size)

        # ===== PHYSICS VARIABLES =====
        self.vel_y = 0.0  # Vertical velocity (how fast moving up/down)
        # 0 = not moving, negative = going up, positive = going down
        self.on_ground = True  # Are we touching the ground? (True = yes, False = no)

        # ===== IMAGE/SPRITE =====
        # If we have an image file, use it. Otherwise, we'll draw a rectangle
        if PLAYER_IMG:
            # Scale the image to match the player's size
            self.image = pygame.transform.scale(PLAYER_IMG, (size, size))
        else:
            self.image = None  # No image, so we'll draw a shape instead

    def jump(self):
        """
        Make the player jump!
        This only works if the player is on the ground (no double jumping).
        """
        if self.on_ground:  # Only jump if we're touching the ground
            self.vel_y = JUMP_VELOCITY  # Set upward velocity (negative = up)
            self.on_ground = False  # We're now in the air

    def update(self, dt, game=None, platforms=None):
        """
        Update the player's position and physics every frame.

        dt = "delta time" = how many seconds passed since last frame
        We use dt so the game runs at the same speed on fast and slow computers!
        platforms = list of platforms to check collision with (optional)

        Example: If dt = 0.016, that means 0.016 seconds passed (about 1/60th of a second)
        """
        # ===== APPLY GRAVITY =====
        # Gravity pulls the player down, so we add it to velocity
        # Bigger dt = more time passed = more gravity applied
        #################################################################
        if self.on_ground == False:
            # Apply gravity only if you are not on the ground
            self.vel_y += GRAVITY * dt
        #################################################################

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
                #####################################################
                if self.rect.colliderect(platform.rect) and self.vel_y >= 0:
                    # if self.rect.bottom > platform.rect.top + 5 and self.rect.top < platform.rect.bottom:
                    #     game.running = False
                    # else:
                    self.vel_y = 0.0
                    self.pos.y = platform.rect.top - self.size + 1
                    self.on_ground = True
                    print("Collide!")
                    break
                # if x_overlap and not y_overlap:
                #     # Game Over
                #     pass
                # elif y_overlap:
                #     self.vel_y = 0.0
                #     self.on_ground = True

                # player_bottom = self.pos.y + self.size
                # platform_top = platform.pos.y
                # player_right = self.pos.x + self.size
                # player_left = self.pos.x
                # platform_right = platform.pos.x + platform.width
                # platform_left = platform.pos.x
                # # TOP collision → Land
                # if (self.vel_y >= 0 and
                #         player_left < platform_right and
                #         player_right > platform_left and
                #         player_bottom <= platform_top + self.size * 0.4):
                #     self.pos.y = platform_top - self.size
                #     self.vel_y = 0.0
                #     self.on_ground = True
                #     break

                #####################################################

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

    def draw(self, surf, show_hitbox=False):
        """
        Draw the player on the screen.
        surf = the surface (screen) to draw on
        """

        if self.image:
            # If we have an image, draw it
            surf.blit(self.image, self.rect.topleft)
        else:
            # No image, so draw a colored rectangle instead
            pygame.draw.rect(surf, OBSTACLE_COLOR, self.rect)

        ########################################
        if show_hitbox:
            pygame.draw.rect(surf, HITBOX_COLOR, self.rect, 2)  # 2 = outline only
        ########################################


# ============================================================================
# STEP 10: OBSTACLE CLASS
# ============================================================================
class Obstacle:
    """
    The Obstacle class represents the triangles/spikes the player must avoid.

    Each obstacle moves from right to left across the screen.
    If the player touches one, they die!
    """

    def __init__(self, x, width, height, speed):
        """
        Create a new obstacle.

        Parameters:
        - x: Starting x position (usually off the right side of screen)
        - width: How wide the obstacle is
        - height: How tall the obstacle is
        - speed: How fast it moves left (pixels per second)
        """
        # Position - bottom sits on the ground
        self.pos = Vector2(x, GROUND_Y - height)
        print(self.pos)

        # Size
        self.width = width
        self.height = height

        # Movement speed
        self.speed = speed  # Pixels per second moving left

        # ===== HITBOX =====
        # Triangle hitbox points for accurate collision
        self.get_p1 = lambda: (int(self.pos.x + self.width / 2), int(self.pos.y))  # top
        self.get_p2 = lambda: (int(self.pos.x), int(self.pos.y + self.height))  # bottom left
        self.get_p3 = lambda: (int(self.pos.x + self.width), int(self.pos.y + self.height))  # bottom right

        # ===== IMAGE =====
        # Try to use an image if available
        if TRIANGLE_IMG:
            self.image = pygame.transform.scale(TRIANGLE_IMG, (width, height))
        else:
            self.image = None

    def update(self, dt):
        """
        Move the obstacle left across the screen.
        dt = time since last frame (for smooth movement)
        """
        # Move left (subtract because x decreases as we go left)
        # Using dt ensures smooth movement at any framerate
        self.pos.x -= self.speed * dt
        # No rect hitbox to update; triangle points calculated on the fly

    def draw(self, surf, show_hitbox=False):
        """
        Draw the obstacle on the screen.

        Parameters:
        - surf: The surface to draw on
        - show_hitbox: If True, draw a red box showing the collision area (for debugging)
        """
        draw_x = int(self.pos.x)  # Use actual position for responsive movement

        ##################################################################
        color = HITBOX_COLOR if show_hitbox else OBSTACLE_COLOR
        if self.image and not show_hitbox:
            # Draw the image if we have one
            surf.blit(self.image, (draw_x, int(self.pos.y)))
        else:
            # Draw a triangle using three points
            # Point 1: Top center (the spike point)
            p1 = (int(draw_x + self.width / 2), int(self.pos.y))
            # Point 2: Bottom left corner
            p2 = (int(draw_x), int(self.pos.y + self.height))
            # Point 3: Bottom right corner
            p3 = (int(draw_x + self.width), int(self.pos.y + self.height))
            # Draw the triangle
            pygame.draw.polygon(surf, color, (p1, p2, p3))
        ##################################################################

    def off_screen(self):
        """
        Check if the obstacle has completely left the screen.
        Returns True if it's off the left edge, False if still visible.
        """
        return self.pos.x + self.width < 0  # If right edge is past left side of screen


# ============================================================================
# STEP 11: PLATFORM CLASS
# ============================================================================
class Platform:
    """
    The Platform class represents platforms that the player can jump on.

    Platforms are like floating ground - the player can land on top of them
    and jump from them. They move from right to left like obstacles.
    """

    def __init__(self, x, y, width, height, speed):
        """
        Create a new platform.

        Parameters:
        - x: Starting x position (usually off the right side of screen)
        - y: Y position (how high the platform is - lower y = higher on screen)
        - width: How wide the platform is
        - height: How thick the platform is
        - speed: How fast it moves left (pixels per second)
        """
        # Position - top-left corner
        self.pos = Vector2(x, y)

        # Size
        self.width = width
        self.height = height

        # Movement speed
        self.speed = speed  # Pixels per second moving left

        # Create a rectangle for collision detection
        # The player lands on the TOP of the platform
        self.rect = pygame.Rect(int(x), int(y), width, height)

        #######################################################################
        # Add a spike in the middle of the platform (40%-60% range)
        # spike_width = max(30, int(self.width * 0.07))
        # spike_height = max(50, int(self.width * 0.12))
        # spike_x = self.pos.x + int(self.width * 0.45)
        # spike_y = self.pos.y - spike_height  # sits on platform
        #
        # self.spike = Obstacle(spike_x, spike_width, spike_height, speed)
        #####################################################################

    def update(self, dt):
        """
        Move the platform left across the screen.
        dt = time since last frame (for smooth movement)
        """
        # Move left (subtract because x decreases as we go left)
        self.pos.x -= self.speed * dt

        # Update the collision rectangle
        self.rect.x = int(self.pos.x)

        ###############################################################
        # # Update spike position to move with the platform
        # self.spike.pos.x = self.pos.x + int(self.width * 0.45)
        # self.spike.update(dt)
        ###############################################################

    def draw(self, surf, show_hitbox=False):
        """
        Draw the platform on the screen.

        Parameters:
        - surf: The surface to draw on
        - show_hitbox: If True, draw a red box showing the collision area
        """
        # Draw the platform as a gray rectangle
        platform_rect = pygame.Rect(int(self.pos.x), int(self.pos.y), self.width, self.height)
        pygame.draw.rect(surf, GROUND_COLOR, platform_rect)

        #######################################
        # # Draw spike on platform
        # self.spike.draw(surf, show_hitbox)
        #######################################

        # Optionally draw the hitbox
        if show_hitbox:
            pygame.draw.rect(surf, HITBOX_COLOR, self.rect, 2)  # 2 = outline only

    def off_screen(self):
        """
        Check if the platform has completely left the screen.
        Returns True if it's off the left edge, False if still visible.
        """
        return self.pos.x + self.width < 0


# ============================================================================
# STEP 12: OBSTACLE MANAGER (KEEPS SPAWNS FAIR)
# ============================================================================
class ObstacleManager:
    """
    Handles the logic for spawning spikes and platforms.
    Making a separate manager keeps the Game class easier to read.
    """

    def __init__(self, speed):
        self.speed = speed
        self.pattern = deque(["spike", "platform"])  # simple alternating pattern
        self.min_gap_time = MIN_GAP_BETWEEN_OBSTACLES / self.speed
        self.timer = 0.0  # spawn immediately when the game starts

    def update(self, dt, game):
        """
        Count down and spawn the next obstacle when the timer hits zero.
        The timer is based on speed, so spacing stays consistent.
        """
        self.timer -= dt
        if self.timer > 0:
            return

        next_type = self.pattern[0]
        self.pattern.rotate(-1)  # alternate spike -> platform -> spike ...

        if next_type == "spike":
            game.obstacles.append(self._spawn_spike())
        else:
            platform_obj, spike_obj = self._spawn_platform()
            game.platforms.append(platform_obj)
            game.obstacles.append(spike_obj)

        # Reset timer with a little randomness but never below the minimum gap
        extra_time = random.uniform(0.1, 0.5) * self.min_gap_time
        self.timer = self.min_gap_time + extra_time

    def _spawn_spike(self, width=-1, height=-1):
        """
        Create a ground spike (triangle) that sits on the ground like real Geometry Dash.
        """
        ###########################
        width = random.randint(*SPIKE_WIDTH_RANGE) if width == -1 else width
        height = random.randint(*SPIKE_HEIGHT_RANGE) if height == -1 else height
        ###########################
        x = SCREEN_WIDTH + 50  # spawn just off the right edge
        return Obstacle(x, width, height, self.speed)

    def _spawn_platform(self):
        """
        Create a floating platform at a consistent height.
        """
        width = random.randint(*PLATFORM_WIDTH_RANGE)
        x = SCREEN_WIDTH + 50
        ##############################
        spike_width = max(50, int((width + 50) * 0.07))
        spike_height = max(50, int((width + 50) * 0.07))
        spike_x = x + int(width * 0.45)
        return Platform(x, PLATFORM_Y, width, PLATFORM_HEIGHT, self.speed), Obstacle(spike_x, spike_width, spike_height, self.speed)
        ##############################


# ============================================================================
# STEP 13: GROUND DRAWING FUNCTION
# ============================================================================
def draw_ground(surf):
    """
    Draw the ground at the bottom of the screen.

    If we have a ground image, we tile it (repeat it) across the screen.
    Otherwise, we just draw a solid colored rectangle.
    """
    if GROUND_IMG:
        # Scale the ground tile image
        tile = pygame.transform.scale(GROUND_IMG, (150, 150))
        tile_w = tile.get_width()  # How wide one tile is

        # Draw tiles from left to right across the screen
        x = 0
        while x < SCREEN_WIDTH:
            surf.blit(tile, (x, GROUND_Y))  # Draw one tile
            x += tile_w  # Move to next position
    else:
        # No image, so draw a solid rectangle
        pygame.draw.rect(surf, GROUND_COLOR,
                         (0, GROUND_Y, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y))


# ============================================================================
# STEP 14: GAME CLASS
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
        """
        Initialize the game - set up everything when the game starts.
        """
        # Create the player at position (80, GROUND_Y - 60) with size 60
        self.player = Player(80, GROUND_Y - 60, 60)

        # Collections that store everything moving in the level
        self.obstacles = []  # ground spikes/triangles
        self.platforms = []  # floating bars the player can land on

        # How fast obstacles and platforms move (pixels per second)
        self.obstacle_speed = 450.0

        # Dedicated manager that keeps spawn spacing fair
        self.obstacle_manager = ObstacleManager(self.obstacle_speed)

        # Game state
        self.running = True  # Is the game currently running? (False = player died)
        self.show_hitboxes = True  # Show collision boxes? (like practice mode in real Geometry Dash)

        # Scoring
        self.score = 0  # Current score (increases over time)
        self.best = 0  # Best score this session

    def reset(self):
        """
        Reset the game to start over after the player dies.
        """
        # Create a new player
        self.player = Player(80, GROUND_Y - 60, 60)

        # Clear all obstacles and platforms
        self.obstacles = []
        self.platforms = []

        # Reset score and spawn logic
        self.score = 0
        self.obstacle_manager = ObstacleManager(self.obstacle_speed)

    def update(self, dt):
        """
        Update everything in the game - called every frame.

        dt = delta time (seconds since last frame)
        """
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
            ###################################################################
            ###################################################################
            if (x2 + margin) <= px <= (x3 - margin):
                # Linear interpolation spike top line
                slope = (y3 - y1) / (x3 - x1)
                spike_top_y = slope * (px - x1) + y1
                # Make spike collision more forgiving (top 10% safe)
                if py > spike_top_y + (y2 - y1) * 0.15:
                    self.best = max(self.best, self.score)
                    self.running = False
                    return
            ###################################################################
            ###################################################################

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
            platform.draw(surf, show_hitbox=self.show_hitboxes)

        # Draw all obstacles
        for ob in self.obstacles:
            ob.draw(surf, show_hitbox=self.show_hitboxes)

        # Draw player last (so it appears on top)
        self.player.draw(surf, show_hitbox=self.show_hitboxes)

        # ===== DRAW UI (User Interface) =====
        # Score display (top left)
        draw_text(surf, f"Score: {int(self.score)}", 12, 12, size=28)

        # Best score display
        draw_text(surf, f"Best: {int(self.best)}", 12, 44, size=20)

        # Instructions (bottom left)
        draw_text(surf, "Space to jump • R to restart after death • H to toggle hitboxes",
                  12, SCREEN_HEIGHT - 28, size=18)


# ============================================================================
# STEP 15: MAIN GAME LOOP
# ============================================================================
def main():
    """
    The main function - this is where our game actually runs!

    The game loop is the heart of any game. It runs over and over, doing three things:
    1. Check for input (keyboard, mouse, etc.)
    2. Update game state (move things, check collisions, etc.)
    3. Draw everything on screen

    This loop runs 60 times per second (60 FPS) to create smooth animation.
    """
    # Create a new game
    game = Game()

    # Delta time - tracks how much time passed since last frame
    dt = 0.0  # Start at 0

    # ===== THE GAME LOOP =====
    # This runs forever until the player closes the window
    while True:
        # ===== STEP 1: HANDLE EVENTS =====
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
                    # R key = restart (only works when game is over)
                    if not game.running:
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
        # Fill the screen with sky blue (clear the old frame)
        screen.fill(SKY_BLUE)

        # Draw all game objects
        game.draw(screen)

        # If game is over, show "You Died!" message
        if not game.running:
            draw_text(screen, "You Died! Press R to restart",
                      SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 - 20,
                      size=34, color=BLACK)

        # Update the display (show everything we just drew)
        pygame.display.flip()  # "Flip" means swap the front and back buffers
        # This prevents flickering and makes animation smooth


# STEP 16: START THE GAME
# This code only runs if we run this file directly (not if we import it)
if __name__ == "__main__":
    main()  # Start the game!
