# lvl3.py
import math
import pygame
import sys
from typing import List, Tuple
from karakterekFeliratok import (
    Player,
    JumpingEnemy,
    Spike,
    Bombs,
    FireBall,
    display_fps,
    hp,
    win_or_lose,
    Peashooter,
    Tallnut
)


def lvl3() -> None:
    """A Level 3 játék logikája és fő ciklusa."""
    # Pygame inicializálása
    pygame.init()
    pygame.mixer.init()

    # Hangok betöltése
    punch: pygame.mixer.Sound = pygame.mixer.Sound("hangok/punch.mp3")
    burning: pygame.mixer.Sound = pygame.mixer.Sound("hangok/burn.wav")
    explosions: pygame.mixer.Sound = pygame.mixer.Sound("hangok/bomba_robbanas.wav")

    # Képernyő beállítása
    screen_width: int = 800
    screen_height: int = 600
    screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Lvl3 - Downfall Tower")

    # Színek
    blue: Tuple[int, int, int] = (0, 0, 255)
    gray: Tuple[int, int, int] = (100, 100, 100)

    # Zászló az alsó emeleten
    flag: pygame.Surface = pygame.image.load("kepek/flag.png").convert_alpha()
    flag = pygame.transform.scale(flag, (80, 160))
    flag_rect: pygame.Rect = flag.get_rect()
    flag_rect.topleft = (30, 420)

    # Szív a HP megjelenítéséhez
    heart: pygame.Surface = pygame.image.load("kepek/heart.png").convert_alpha()
    heart = pygame.transform.scale(heart, (40, 40))
    hp_rect: pygame.Rect = heart.get_rect()
    hp_rect.topleft = (15, 420)

    # Játékos létrehozása
    player: Player = Player(0, 50, 50, 50)
    lives: int = 100

    # Platformok definiálása emeletek szerint
    platforms: List[pygame.Rect] = [
        pygame.Rect(0, 100, 750, 20),  # 1. emelet
        pygame.Rect(50, 250, 800, 20),  # 2. emelet
        pygame.Rect(0, 400, 750, 20),  # 3. emelet
        pygame.Rect(50, 580, 800, 20),  # 4. emelet (alsó)
    ]

    # Mozgó tüskék létrehozása
    spikes: List[Spike] = [
        Spike(150, 75, 25, 25, 100, 350, 5),
        Spike(500, 75, 25, 25, 400, 600, 5),
        Spike(250, 75, 25, 25, 600, 750, 5),
    ]

    # Bombák létrehozása
    bombs: List[Bombs] = [
        Bombs(150, 0, 25, 25),
        Bombs(550, 0, 25, 25),
        Bombs(350, 0, 25, 25),
    ]

    # Ugráló ellenfelek létrehozása
    enemies: List[JumpingEnemy] = [
        JumpingEnemy(100, 280, 30, 30),
        JumpingEnemy(250, 280, 30, 30),
        JumpingEnemy(400, 280, 30, 30),
        JumpingEnemy(550, 280, 30, 30),
        JumpingEnemy(700, 280, 30, 30),
    ]

    # Forgó tűzgolyók létrehozása
    fireballs: List[FireBall] = [
        FireBall(25, 25, (100, 180), 50, 0.1, math.radians(0)),
        FireBall(25, 25, (300, 180), 50, 0.08, math.radians(190)),
        FireBall(25, 25, (500, 180), 50, 0.12, math.radians(65)),
        FireBall(25, 25, (700, 180), 50, 0.09, math.radians(250)),
    ]

    # Peashooterek létrehozása
    peashooters: List[Peashooter] = [
        Peashooter(100, 535, 50, 50, bullet_speed=7),
    ]

    # Tallnutok létrehozása
    tallnuts: List[Tallnut] = [
        Tallnut(250, 535, 50, 50),
        Tallnut(550, 535, 50, 50),
        Tallnut(400, 535, 50, 50)
    ]

    # Betűtípus és óra inicializálása
    font: pygame.font.Font = pygame.font.Font(None, 36)
    clock: pygame.time.Clock = pygame.time.Clock()
    succesfull: bool = False
    run: bool = True

    # Fő játékciklus
    while run:
        # Események kezelése
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                run = False

        # Játékos mozgása és gravitáció alkalmazása
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()
        player.check_collision(platforms)

        # Képernyő törlése
        screen.fill((135, 206, 235))

        # Platformok kirajzolása
        for p in platforms:
            pygame.draw.rect(screen, gray, p)

        # Tüskék frissítése és ütközés
        for s in spikes:
            s.draw(screen)
            s.update()
            if player.rect.colliderect(s):
                player = Player(0, 50, 50, 50)
                lives -= 1
                punch.play()

        # Bombák kirajzolása és ütközés
        for b in bombs:
            b.draw(screen)
            if b.rect.colliderect(player):
                player = Player(0, 50, 50, 50)
                lives -= 1
                explosions.play()

        # Ugráló ellenfelek mozgása és ütközés
        for e in enemies:
            e.draw(screen)
            e.move(260, 380)
            if player.rect.colliderect(e):
                player = Player(0, 50, 50, 50)
                lives -= 1
                punch.play()

        # Forgó tűzgolyók mozgatása és ütközés
        for f in fireballs:
            f.draw(screen)
            f.update()
            if f.collides_with(player):
                player = Player(0, 50, 50, 50)
                lives -= 1
                burning.play()

        # Peashooterek frissítése és ütközés
        for ps in peashooters:
            ps.draw(screen)
            ps.update(screen_width)
            if ps.check_collision(player):
                player = Player(0, 50, 50, 50)
                lives -= 1

        # Tallnutok rajzolása és ütközés
        for tn in tallnuts:
            tn.draw(screen)
            if tn.check_collision(player):
                player = Player(0, 50, 50, 50)
                lives -= 1

        # Játékos kirajzolása
        player.draw(screen, blue)

        # Zászló kirajzolása és elérése
        screen.blit(flag, flag_rect)
        if player.rect.colliderect(flag_rect):
            succesfull = True
            run = False

        # HP megjelenítése
        screen.blit(heart, hp_rect)
        hp(screen, lives, (34, 438))

        # FPS megjelenítése
        display_fps(screen, clock, font)

        # Képernyő frissítése
        pygame.display.flip()
        clock.tick(60)

        # Ha az élet elfogyott, kilépés
        if lives <= 0:
            run = False

    # Eredmény megjelenítése
    if succesfull:
        win_or_lose(screen_width, screen_height, screen, (255, 255, 255), "YOU WIN!")
    else:
        win_or_lose(screen_width, screen_height, screen, (255, 255, 255), "YOU LOSE!")

    # Pygame bezárása
    pygame.quit()
    sys.exit()
