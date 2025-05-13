import pygame

# Created by: Szemán László

# Initialize pygame
pygame.init()
pygame.display.set_caption("Úristen very big project *javított* beta 0.8.5")

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (124, 252, 0)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GRAY = (200, 200, 200)
PINK = (100, 72, 77)
DARK_GREEN = (0, 128, 0)

# Player positions
player1_x = 0
player1_y = 500
player2_x = 760
player2_y = 500

# Platform settings
platform_x = 200
platform_y = 350
platform_width = 400
platform_height = 40

# Health points
player1_health = 250
player2_health = 250

# Movement variables
player1_x_velocity = 0
player1_y_velocity = 0
player2_x_velocity = 0
player2_y_velocity = 0

# Bullet settings
bullet1_start_x = 135
bullet1_start_y = 110
bullet2_start_x = 600
bullet2_start_y = 110
bullet1_direction = 12
bullet2_direction = -12
bullet1_x = bullet1_start_x
bullet1_y = bullet1_start_y
bullet2_x = bullet2_start_x
bullet2_y = bullet2_start_y

# Axe settings
axe1_x = 200
axe1_y = 100
axe2_x = 650
axe2_y = 100
axe1_x_direction = 12
axe1_y_direction = 4
axe2_x_direction = -12
axe2_y_direction = 4
bullet_damage = 10
axe_damage = 10

# Special abilities
rasengan_x = 250
rasengan_y = 100
rasengan_speed = 15
player1_hits = 0

fireball_x = 700
fireball_y = 100
fireball_speed = 15
player2_hits = 0

game_over = 0

# State flags
bullet1_state = 0
bullet1_ready = 0
bullet1_active = 0

bullet2_state = 0
bullet2_ready = 0
bullet2_active = 0

axe1_state = 1
axe1_ready = 1
axe1_active = 1
axe1_direction_control = 1

axe2_state = 1
axe2_ready = 1
axe2_active = 1

rasengan_state = 0
rasengan_ready = 0
rasengan_active = 0

fireball_state = 0
fireball_ready = 0
fireball_active = 0

# Font settings
basic_font = pygame.font.SysFont('Times New Roman', 22)
large_font = pygame.font.SysFont('Times New Roman', 50)
huge_font = pygame.font.SysFont('Times New Roman', 100)

# Player names
player1_name = "Laci"
player2_name = "Patrik"
game_ended = False
draw_text = "Döntetlen"
winner_text = ""
fight_text = "FIGHT"

# Timer
start_ticks = pygame.time.get_ticks()

# Sound effects
shot_sound = pygame.mixer.Sound("hangok/gun.mp3")
shot_sound2 = pygame.mixer.Sound("hangok/gun2.mp3")
pygame.mixer.music.load('hangok/hatter_muzsika.mp3')
axe_hit_sound = pygame.mixer.Sound("hangok/fejsze.mp3")
rasengan_sound = pygame.mixer.Sound("hangok/rasengan.mp3")
fireball_sound = pygame.mixer.Sound("hangok/fireball.mp3")
pygame.mixer.music.play(-1)

# Images
player1_img = pygame.image.load('kepek/kep1.png')
player2_img = pygame.image.load('kepek/kep2.jpg')
bullet1_img = pygame.image.load("kepek/bullet.jpg")
bullet2_img = pygame.image.load("kepek/bullet2.jpg")
axe1_img = pygame.image.load("kepek/balta.jpg")
axe2_img = pygame.image.load("kepek/balta2.jpg")
rasengan_img = pygame.image.load("kepek/rasengan.png")
fireball_img = pygame.image.load("kepek/fireball.png")
pygame.display.set_icon(player1_img)
pygame.display.set_icon(player2_img)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        # Player controls
        if event.type == pygame.KEYDOWN:
            # Player 1 movement
            if event.key == pygame.K_a:
                player1_x_velocity = -5
                if bullet1_active == 0:
                    bullet1_direction = -12
                if axe1_active == 1:
                    axe1_x_direction = -12
                if rasengan_active == 0:
                    rasengan_speed = -15
            if event.key == pygame.K_d:
                player1_x_velocity = 5
                if bullet1_active == 0:
                    bullet1_direction = 12
                if axe1_active == 1:
                    axe1_x_direction = 12
                if rasengan_active == 0:
                    rasengan_speed = 15
            # Player 2 movement
            if event.key == pygame.K_LEFT:
                player2_x_velocity = -5
                if bullet2_active == 0:
                    bullet2_direction = -12
                if fireball_active == 0:
                    fireball_speed = -15
            if event.key == pygame.K_RIGHT:
                player2_x_velocity = 5
                if bullet2_active == 0:
                    bullet2_direction = 12
                if fireball_active == 0:
                    fireball_speed = 15

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player1_x_velocity = 0
            if event.key == pygame.K_d:
                player1_x_velocity = 0
            if event.key == pygame.K_LEFT:
                player2_x_velocity = 0
            if event.key == pygame.K_RIGHT:
                player2_x_velocity = 0

        # Player 1 shooting
        if bullet1_ready == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    bullet1_x = player1_x + 40
                    bullet1_y = player1_y + 20
                    bullet1_active = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    bullet1_state = 1
                    bullet1_ready = 1
                    pygame.mixer.Sound.play(shot_sound)

        # Player 2 shooting
        if bullet2_ready == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    bullet2_x = player2_x - 20
                    bullet2_y = player2_y + 20
                    bullet2_active = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_i:
                    bullet2_state = 1
                    bullet2_ready = 1
                    pygame.mixer.Sound.play(shot_sound2)

        # Player 1 jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1_y_velocity = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player1_y_velocity = 5
                axe1_direction_control = 1
                if axe1_direction_control == 1:
                    axe1_y_direction = 4

        # Player 2 jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2_y_velocity = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player2_y_velocity = 5

        # Player 1 axe throw
        if axe1_ready == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    axe1_x = player1_x + 20
                    axe1_y = player1_y - 40
                    axe1_active = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_2:
                    axe1_state = 0
                    axe1_ready = 0

        # Axe direction control
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                axe1_direction_control = 0
                if axe1_direction_control == 0:
                    axe1_y_direction = -4

        # Player 2 axe throw
        if axe2_ready == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    axe2_x = player2_x - 20
                    axe2_y = player2_y - 40
                    axe2_active = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_o:
                    axe2_state = 0
                    axe2_ready = 0

        # Player 1 special ability (Rasengan)
        if player1_hits >= 3:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    rasengan_x = player1_x + 20
                    rasengan_y = player1_y
                    rasengan_active = 1
                    pygame.mixer.Sound.play(rasengan_sound)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_3:
                    rasengan_state = 1
                    rasengan_ready = 1

        # Player 2 special ability (Fireball)
        if player2_hits >= 3:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    fireball_x = player2_x - 20
                    fireball_y = player2_y
                    fireball_active = 1
                    pygame.mixer.Sound.play(fireball_sound)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    fireball_state = 1
                    fireball_ready = 1

    # Update positions
    player1_x += player1_x_velocity
    player1_y += player1_y_velocity
    player2_x += player2_x_velocity
    player2_y += player2_y_velocity

    # Update projectile positions
    if bullet1_state == 1:
        bullet1_x += bullet1_direction
    if bullet2_state == 1:
        bullet2_x += bullet2_direction
    if axe1_state == 0:
        axe1_x += axe1_x_direction
        axe1_y += axe1_y_direction
    if axe2_state == 0:
        axe2_x += axe2_x_direction
        axe2_y += axe2_y_direction
    if rasengan_state == 1:
        rasengan_x += rasengan_speed
        player1_hits = 0
    if fireball_state == 1:
        fireball_x += fireball_speed
        player2_hits = 0

    # Clear screen
    screen.fill(WHITE)

    # Set boundaries
    if player1_y > 500:
        player1_y = 500
    if player1_y < 130:
        player1_y = 130
    if player1_x < 0:
        player1_x = 0
    if player1_x > 760:
        player1_x = 760

    if player2_y > 500:
        player2_y = 500
    if player2_y < 130:
        player2_y = 130
    if player2_x < 0:
        player2_x = 0
    if player2_x > 760:
        player2_x = 760

    # Draw game elements
    # Ground
    pygame.draw.rect(screen, BROWN, (0, 540, 800, 60))
    pygame.draw.rect(screen, DARK_GREEN, (0, 540, 800, 30))

    # Players
    screen.blit(player1_img, (player1_x, player1_y))
    screen.blit(player2_img, (player2_x, player2_y))

    # Platform
    pygame.draw.rect(screen, BROWN, (platform_x, platform_y, platform_width, platform_height))
    pygame.draw.rect(screen, DARK_GREEN, (platform_x, platform_y, platform_width, 20))

    # Health bars
    pygame.draw.rect(screen, RED, (40, 20, player1_health, 20))
    pygame.draw.rect(screen, RED, (500, 20, player2_health, 20))

    # Timer circle
    pygame.draw.circle(screen, PINK, (385, 40), 30)

    # Projectiles
    screen.blit(bullet1_img, (bullet1_x, bullet1_y))
    screen.blit(bullet2_img, (bullet2_x, bullet2_y))

    # Axes
    screen.blit(axe1_img, (axe1_x, axe1_y))
    screen.blit(axe2_img, (axe2_x, axe2_y))

    # Special abilities
    screen.blit(rasengan_img, (rasengan_x, rasengan_y))
    screen.blit(fireball_img, (fireball_x, fireball_y))

    # Collision detection and reset for bullets
    if bullet1_x in range(player2_x, player2_x + 40) and bullet1_y in range(player2_y, player2_y + 40):
        player2_health -= bullet_damage
        bullet1_x = bullet1_start_x
        bullet1_y = bullet1_start_y
        bullet1_state = 0
        bullet1_ready = 0
        bullet1_active = 0
        player1_hits += 1

    if bullet1_x > 800 or bullet1_x < 0:
        bullet1_x = bullet1_start_x
        bullet1_y = bullet1_start_y
        bullet1_state = 0
        bullet1_ready = 0
        bullet1_active = 0

    if bullet2_x in range(player1_x, player1_x + 40) and bullet2_y in range(player1_y, player1_y + 40):
        player1_health -= bullet_damage
        bullet2_x = bullet2_start_x
        bullet2_y = bullet2_start_y
        bullet2_state = 0
        bullet2_ready = 0
        bullet2_active = 0
        player2_hits += 1

    if bullet2_x > 800 or bullet2_x < 0:
        bullet2_x = bullet2_start_x
        bullet2_y = bullet2_start_y
        bullet2_state = 0
        bullet2_ready = 0
        bullet2_active = 0

    # Collision detection and reset for axes
    if axe1_x > 800 or axe1_x < 0 or axe1_y < 0 or axe1_y > 600:
        axe1_x = 200
        axe1_y = 100
        axe1_state = 1
        axe1_ready = 1
        axe1_active = 1

    if axe1_x in range(player2_x - 40, player2_x + 40) and axe1_y in range(player2_y - 40, player2_y + 40):
        axe1_x = 200
        axe1_y = 100
        axe1_state = 1
        axe1_ready = 1
        axe1_active = 1
        player2_health -= axe_damage
        player1_hits += 1
        pygame.mixer.Sound.play(axe_hit_sound)

    if axe2_x > 800 or axe2_x < 0 or axe2_y < 0 or axe2_y > 600:
        axe2_x = 650
        axe2_y = 100
        axe2_state = 1
        axe2_ready = 1
        axe2_active = 1

    if axe2_x in range(player1_x - 40, player1_x + 40) and axe2_y in range(player1_y - 40, player1_y + 40):
        axe2_x = 650
        axe2_y = 100
        player1_health -= axe_damage
        axe2_state = 1
        axe2_ready = 1
        axe2_active = 1
        player2_hits += 1
        pygame.mixer.Sound.play(axe_hit_sound)

    # Collision detection for special abilities
    if rasengan_x in range(player2_x, player2_x + 40) and rasengan_y in range(player2_y, player2_y + 40):
        player2_health -= 50
        rasengan_x = 250
        rasengan_y = 100
        rasengan_state = 0
        rasengan_ready = 0
        rasengan_active = 0

    if rasengan_x > 800 or rasengan_x < 0:
        rasengan_x = 250
        rasengan_y = 100
        rasengan_state = 0
        rasengan_ready = 0
        rasengan_active = 0

    if fireball_x in range(player1_x, player1_x + 40) and fireball_y in range(player1_y, player1_y + 40):
        player1_health -= 50
        fireball_x = 700
        fireball_y = 100
        fireball_state = 0
        fireball_ready = 0
        fireball_active = 0

    if fireball_x > 800 or fireball_x < 0:
        fireball_x = 700
        fireball_y = 100
        fireball_state = 0
        fireball_ready = 0
        fireball_active = 0

    # Platform collision
    if player1_y == 360 and player1_x in range(platform_x - 40, platform_x + platform_width):
        player1_y = 400
    if player1_y == 310 and player1_x in range(platform_x - 40, platform_x + platform_width):
        player1_y = 305

    if player2_y == 360 and player2_x in range(platform_x - 40, platform_x + platform_width):
        player2_y = 400
    if player2_y == 310 and player2_x in range(platform_x - 40, platform_x + platform_width):
        player2_y = 305

    # Timer
    seconds = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = 180 - seconds

    # Health minimum
    if player1_health < 0:
        player1_health = 0
    if player2_health < 0:
        player2_health = 0

    # Draw text
    health_text = basic_font.render(f'HP:{player1_health}', False, RED)
    screen.blit(health_text, (180, 60))
    health_text = basic_font.render(f'HP:{player2_health}', False, RED)
    screen.blit(health_text, (660, 60))

    name_text = basic_font.render(f'Név: {player1_name}', False, GREEN)
    screen.blit(name_text, (40, 60))
    name_text = basic_font.render(f'Név: {player2_name}', False, BLUE)
    screen.blit(name_text, (500, 60))

    timer_text = basic_font.render(f'{time_left}', False, GRAY)
    screen.blit(timer_text, (370, 25))

    ammo_text = basic_font.render('p1 bullet: ', False, GRAY)
    screen.blit(ammo_text, (40, 100))
    ammo_text = basic_font.render('p2 bullet: ', False, GRAY)
    screen.blit(ammo_text, (500, 100))

    fight_text_display = large_font.render(f'{fight_text}', False, RED)
    screen.blit(fight_text_display, (270, 250))

    # Remove fight text after 3 seconds
    if time_left <= 177:
        fight_text = ""

    # Determine winner
    winner_text_display = large_font.render(f'{winner_text}', False, RED)
    screen.blit(winner_text_display, (270, 250))

    if player1_health == 0:
        winner_text = "A győztes a játékos 2"
        print(winner_text)
        game_over = 100

    if player2_health == 0:
        winner_text = "A győztes a játékos 1"
        print(winner_text)
        game_over = 100

    if time_left == 0:
        winner_text = "Döntetlen"
        print(winner_text)
        game_over = 100

    # End game after showing winner
    if game_over == 100:
        pygame.time.wait(2000)
        running = False

    # Increase damage at 60 seconds remaining
    if time_left == 60:
        bullet_damage = 20
        axe_damage = 20

    # Increase damage when health is low
    if player2_health in range(0, 121):
        axe_damage = 30
    if player1_health in range(0, 121):
        bullet_damage = 30

    pygame.display.flip()
    clock.tick(60)
