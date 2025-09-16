import pygame, sys, math

pygame.init()

clock = pygame.time.Clock()

size = width, height = 1200, 600
screen = pygame.display.set_mode(size)

# creating function for displaying text
courier_new_50 = pygame.font.SysFont("Courier New", 50)

def draw_text(txt, font, txt_color, x, y):
    img = font.render(txt, True, txt_color)
    screen.blit(img, (x, y))


# Start and reset ball at centre
def reset_ball():
    global ball, speed
    ball.center = ((600, 300))
    dir_x = math.copysign(1, speed[0])
    dir_y = math.copysign(1, speed[1])
    speed = [4*dir_x, 4*dir_y]

# Increase speed everytime the player touch the ball
def speed_game():
    global speed, speed_multiplier
    speed = list(map(lambda x: x*speed_multiplier, speed))

def check_game_over(points):
    global game_over, win_condition
    # If blue wins
    if points[0] >= win_condition:
        screen.fill((0, 0, 0))
        draw_text(f"BLUE wins!", courier_new_50, (255, 255, 255), 450, 150)
        draw_text(f"Please press ESC to exit the game", courier_new_50, (255, 255, 255), 100, 250)
        draw_text(f"Or press R to restart the game", courier_new_50, (255, 255, 255), 120, 350)
        game_over = True # freeze the game
    # If red wins
    elif points[1] >= win_condition:
        screen.fill((0, 0, 0))
        draw_text(f"BLUE wins!", courier_new_50, (255, 255, 255), 450, 150)
        draw_text(f"Please press ESC to exit the game", courier_new_50, (255, 255, 255), 100, 250)
        draw_text(f"Or press R to restart the game", courier_new_50, (255, 255, 255), 120, 350)
        game_over = True
    else:
        reset_ball() # return the ball to original position

# Put it in the set up function so the game can be restarted
def set_up():
    global p1y_posit, p2y_posit, stuck, speed, p1_point, p2_point, game_over, win_condition, p1, p2, ball, speed_multiplier, last_touch
    p1y_posit = 300
    p2y_posit = 300
    stuck = 0
    speed = [4, 4]
    speed_multiplier = 1.1
    p1_point = 0
    p2_point = 0
    game_over = False
    win_condition = 10
    last_touch = "R"

    # creating players and ball
    p1 = pygame.Rect(50, 0, 50, 200)
    p2 = pygame.Rect(1100, 600, 50, 200)
    ball = pygame.Rect(600, 300, 50, 50)

set_up()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: sys.exit()
    if keys[pygame.K_r]: set_up()

    # only run the game if it is not game over
    if not game_over:
        # listen to key press and change y cor of player
        if keys[pygame.K_w] and p1.y > 0:
            p1y_posit -= 5
        if keys[pygame.K_s] and p1.y < 400:
            p1y_posit += 5
        if keys[pygame.K_UP] and p2.y > 0:
            p2y_posit -= 5
        if keys[pygame.K_DOWN] and p2.y < 400:
            p2y_posit += 5

        # update player position
        p1.y = p1y_posit
        p2.y = p2y_posit

        # make ball reflect against wall
        ball = ball.move(speed)
        if ball.y > 600 or ball.y < 0:
            speed[1] = speed[1] * -1

        # increase point for the other side when ball move past the player
        if ball.x > 1200:
            p1_point += 1
            check_game_over((p1_point, p2_point))
        if ball.x < 0:
            p2_point += 1
            check_game_over((p1_point, p2_point))

        # detect ball collision and inverse direction of ball
        if ball.colliderect(p1):
            speed[0] = speed[0] * -1
            # Make sure that the speed only multiplied once
            if last_touch != "R":
                speed_game()
            last_touch = "R"

        if ball.colliderect(p2):
            speed[0] = speed[0] * -1
            if last_touch != "B":
                speed_game()
            last_touch = "B"

        pygame.draw.rect(screen, (0, 0, 255), p2)
        pygame.draw.rect(screen, (255, 0, 0), p1)
        pygame.draw.rect(screen, (12, 243, 145), ball)

        # change to the bottom so the game over screen can be displayed when the score reaches the win condition
        text = f"{p1_point}:{p2_point}"
        draw_text(text, courier_new_50, (255, 255, 255), 565, 100)

        pygame.display.flip()
        screen.fill((0, 0, 0))

    clock.tick(120)
