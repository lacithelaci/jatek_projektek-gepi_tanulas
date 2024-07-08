import math

import pygame
import sys
from karakterekFeliratok import Player, FireBall, JumpingEnemy, Spike, Bombs, display_fps, hp, win_or_lose


def lvl2() -> None:
    # Pygame inicializálása
    pygame.init()
    pygame.mixer.init()

    # hangok importálása
    explosions = pygame.mixer.Sound('hangok/bomba_robbanas.wav')
    punch = pygame.mixer.Sound('hangok/punch.mp3')
    teleporting = pygame.mixer.Sound('hangok/teleport.mp3')
    burning = pygame.mixer.Sound('hangok/burn.wav')

    # Képernyő beállítása
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Platformer Game Demo")

    # Színek
    blue = (0, 0, 255)
    brown = (150, 75, 0)

    # Zászló betöltése és átméretezése
    original_flag_image = pygame.image.load('kepek/flag.png').convert_alpha()
    new_flag_image = pygame.transform.scale(original_flag_image, (80, 160)).convert_alpha()
    new_flag_image = pygame.transform.flip(new_flag_image, True, False)
    flag_rect = new_flag_image.get_rect()
    flag_rect.topleft = (80, 160)

    # Teleportok betöltése, átméretezése
    original_tp_image = pygame.image.load('kepek/teleport.png').convert_alpha()
    new_tp_image = pygame.transform.scale(original_tp_image, (40, 120)).convert_alpha()
    tp_rect1 = new_tp_image.get_rect()
    tp_rect1.topleft = (750, 433)
    tp_rect2 = new_tp_image.get_rect()
    tp_rect2.topleft = (0, 22)

    # szív kirajzolása
    original_hp_image = pygame.image.load('kepek/heart.png').convert_alpha()
    new_hp_image = pygame.transform.scale(original_hp_image, (75, 75)).convert_alpha()
    hp_rect = new_hp_image.get_rect()
    hp_rect.topleft = (15, 200)

    # platformok kirajzolásaq
    platforms = [pygame.Rect(0, 550, 150, 50), pygame.Rect(300, 550, 150, 50), pygame.Rect(600, 550, 200, 50),
                 pygame.Rect(0, 320, 200, 25), pygame.Rect(330, 320, 200, 25), pygame.Rect(650, 320, 200, 25),
                 pygame.Rect(0, 140, 700, 25)]

    # tűzlabdák kirajzolása
    fireballs = [FireBall(25, 25, (225, 450), 80, 0.075, math.radians(0)),
                 FireBall(25, 25, (225, 450), 80, 0.075, math.radians(180)),
                 FireBall(25, 25, (525, 450), 80, 0.075, math.radians(0)),
                 FireBall(25, 25, (525, 450), 80, 0.075, math.radians(180))]

    # ellenfelek példányosítása és tárolása
    enemies = [JumpingEnemy(570, 250, 30, 30), JumpingEnemy(250, 300, 30, 30)]

    # tüskés ellenfél példányosítása
    spikes = [Spike(300, 295, 25, 25, 320, 530, 6),
              Spike(150, 115, 25, 25, 100, 700, 5),
              Spike(350, 115, 25, 25, 100, 700, 5),
              Spike(600, 115, 25, 25, 100, 700, 5), ]

    # bombák példányosítása és tárolása
    bombs = [Bombs(250, 0, 30, 30), Bombs(500, 0, 30, 30)]

    # Játékos példányosítása
    player = Player(0, 500, 50, 50)

    # élet
    lives = 50

    # Alapértelmezett betűtípus beállítása
    font = pygame.font.Font(None, 36)

    # sikeresen befejeződött-e a játék?
    succesfull = False

    # Játék ciklus
    clock = pygame.time.Clock()

    # A játék futása
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False

        # játékosmozgás
        keys = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()
        player.check_collision(platforms)

        # halálok
        if player.rect.y > 800:
            player = Player(0, 500, 50, 50)
            lives -= 1

        # Képernyő törlése
        screen.fill((135, 206, 235))

        # ellenfelek kirajzolása és mozgatása és ütközések kezelése
        for enemy in enemies:
            enemy.draw(screen)
            enemy.move(185, 350)

            # ütközés
            if player.rect.colliderect(enemy):
                pygame.time.wait(200)
                player = Player(0, 500, 50, 50)
                lives -= 1
                punch.play()

        # tüskés ellenfelek kirajzolása és mozgatása és ütközés
        for spike in spikes:
            spike.draw(screen)
            spike.update()
            if spike.rect.colliderect(player):
                player = Player(0, 500, 50, 50)
                lives -= 1
                punch.play()

        # bombák kirajzolása és ütközés
        for bomb in bombs:
            bomb.draw(screen)
            if bomb.rect.colliderect(player):
                player = Player(0, 500, 50, 50)
                lives -= 1
                explosions.play()

        # Játékos, platformok és fű kirajzolása
        player.draw(screen, blue)
        for platform in platforms:
            pygame.draw.rect(screen, brown, platform)

        # tűzlabdák kirajzolása és ütközés
        for fireball in fireballs:
            fireball.draw(screen)
            fireball.update()

            if fireball.collides_with(player):
                player = Player(0, 500, 50, 50)
                lives -= 1
                burning.play()

        # cél elérése és ahhoz kapcsolódó események
        if player.rect.colliderect(flag_rect):
            succesfull = True
            run = False

        # elveszített összes HP
        if lives < 0:
            run = False

        # teleportálások
        if player.rect.colliderect(tp_rect1):
            player = Player(50, 100, 50, 50)
            teleporting.play()

        if player.rect.colliderect(tp_rect2):
            player = Player(700, 400, 50, 50)
            teleporting.play()

        # tp-k kirajzolása
        screen.blit(new_tp_image, tp_rect1)
        screen.blit(new_tp_image, tp_rect2)

        # zászló kirajzolása
        screen.blit(new_flag_image, flag_rect)

        # HP megjelenítése
        screen.blit(new_hp_image, hp_rect)
        hp(screen, lives, (55, 230))

        # FPS megjelenítése
        display_fps(screen, clock, font)

        # Képernyő frissítése
        pygame.display.flip()

        # FPS beállítása
        clock.tick(60)

    if succesfull:
        win_or_lose(screen_width, screen_height, screen, (255, 255, 255), "You Win")
    else:
        win_or_lose(screen_width, screen_height, screen, (255, 255, 255), "You Lose")
    # Pygame bezárása
    pygame.quit()
    sys.exit()
