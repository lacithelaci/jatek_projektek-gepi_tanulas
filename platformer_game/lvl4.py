# lvl4.py
import math
import pygame
import sys
from typing import List, Tuple
from karakterekFeliratok import (
    Player,
    display_fps,
    hp,
    win_or_lose,
    BossEnemy, JumpingEnemy, Tallnut, Peashooter, Spike
)


def lvl4() -> None:
    """A Level 4 játék logikája és fő ciklusa."""

    # Pygame és hangrendszer inicializálása
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

    # Színek definiálása
    blue: Tuple[int, int, int] = (0, 0, 255)
    gray: Tuple[int, int, int] = (100, 100, 100)

    # Zászló létrehozása és pozicionálása
    flag: pygame.Surface = pygame.image.load("kepek/flag.png").convert_alpha()
    flag = pygame.transform.scale(flag, (80, 160))
    flag_rect: pygame.Rect = flag.get_rect()
    flag_rect.topleft = (30, 420)

    # Szív létrehozása HP kijelzéshez
    heart: pygame.Surface = pygame.image.load("kepek/heart.png").convert_alpha()
    heart = pygame.transform.scale(heart, (40, 40))
    hp_rect: pygame.Rect = heart.get_rect()
    hp_rect.topleft = (15, 420)

    # Játékos létrehozása és kezdő élet
    player: Player = Player(0, 50, 50, 50)
    lives: int = 100

    # Főboss létrehozása, mozgástartomány beállítása
    boss = BossEnemy(100, 400, 580)  # x_left=100, x_right=400, y=580

    # Platformok definiálása emeletek szerint
    platforms: List[pygame.Rect] = [
        pygame.Rect(0, 100, 750, 20),  # 1. emelet
        pygame.Rect(50, 250, 800, 20),  # 2. emelet
        pygame.Rect(0, 400, 750, 20),  # 3. emelet
        pygame.Rect(50, 580, 800, 20),  # 4. emelet (alsó)
    ]

    # Ugráló ellenfelek létrehozása
    enemies: List[JumpingEnemy] = [
        JumpingEnemy(100, 80, 30, 30),
        JumpingEnemy(250, 0, 30, 30),
        JumpingEnemy(400, 100, 30, 30),
        JumpingEnemy(550, -30, 30, 30),
        JumpingEnemy(700, 70, 30, 30),
    ]

    # Tallnutok létrehozása a pályára
    tallnuts: List[Tallnut] = [
        Tallnut(650, 210, 42, 42),
        Tallnut(500, 210, 42, 42),
        Tallnut(350, 210, 42, 42),
        Tallnut(200, 210, 42, 42),
    ]

    # Peashooterek létrehozása (upside_down paraméterrel a fejjel lefelé változathoz)
    peashooters: List[Peashooter] = [
        Peashooter(0, 120, 50, 50, bullet_speed=7, upside_down=True),
    ]

    # Mozgó tüskék létrehozása
    spikes: List[Spike] = [
        Spike(216, 380, 25, 25, 100, 750, 5),
        Spike(432, 380, 25, 25, 100, 750, 5),
        Spike(648, 380, 25, 25, 100, 750, 5),
    ]

    # Betűtípus és óra inicializálása
    font: pygame.font.Font = pygame.font.Font(None, 36)
    clock: pygame.time.Clock = pygame.time.Clock()
    succesfull: bool = False
    run: bool = True

    # Fő játékciklus
    while run:
        # Események kezelése (kilépés és Q gomb)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                run = False

        # Játékos mozgása és gravitáció
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()
        player.check_collision(platforms)

        # Képernyő törlése minden frame előtt
        screen.fill((135, 206, 235))

        # Platformok kirajzolása
        for p in platforms:
            pygame.draw.rect(screen, gray, p)

        # Főboss frissítése és kirajzolása
        boss.update()
        boss.draw(screen)

        # Lövedékek ütközésének kezelése, élet csökkentése, de a játék nem ér véget
        for fb in boss.fireballs:
            if fb.rect.colliderect(player.rect):
                fb.kill()  # Lövedék eltávolítása
                lives -= 1  # Élet csökkentése
                player: Player = Player(0, 50, 50, 50)  # Visszaállítás kezdőpozícióra
                burning.play()

        # Ugráló ellenfelek frissítése és ütközés
        for e in enemies:
            e.draw(screen)
            e.move(-80, 80)
            if player.rect.colliderect(e):
                player = Player(0, 50, 50, 50)
                lives -= 1
                punch.play()  # Hang lejátszása

        # Tallnutok frissítése és ütközés
        for tn in tallnuts:
            tn.draw(screen)
            if tn.check_collision(player):
                player = Player(0, 50, 50, 50)
                lives -= 1
                punch.play()

        # Peashooterek frissítése és ütközés
        for ps in peashooters:
            ps.draw(screen)
            ps.update(screen_width)
            if ps.check_collision(player):
                player = Player(0, 50, 50, 50)
                lives -= 1
                punch.play()

        # Tüskék frissítése és ütközés
        for s in spikes:
            s.draw(screen)
            s.update()
            if player.rect.colliderect(s):
                player = Player(0, 50, 50, 50)
                lives -= 1
                punch.play()

        # Játékos kirajzolása
        player.draw(screen, blue)

        # Zászló kirajzolása és elérése
        screen.blit(flag, flag_rect)
        if player.rect.colliderect(flag_rect):
            succesfull = True
            run = False  # Sikeres pálya teljesítés

        # Ha a boss hozzáér a játékoshoz
        if boss.rect.colliderect(player):
            lives -= 1
            player: Player = Player(0, 50, 50, 50)  # Visszaállítás kezdőpozícióra

        # HP megjelenítése
        screen.blit(heart, hp_rect)
        hp(screen, lives, (34, 438))

        # FPS megjelenítése
        display_fps(screen, clock, font)

        # Képernyő frissítése
        pygame.display.flip()
        clock.tick(60)

        # Ha az élet elfogyott, kilép a fő ciklusból
        if lives <= 0:
            run = False

    # Eredmény megjelenítése a játék végén
    if succesfull:
        win_or_lose(screen_width, screen_height, screen, (255, 255, 255), "YOU WIN!")
    else:
        win_or_lose(screen_width, screen_height, screen, (255, 255, 255), "YOU LOSE!")

    # Pygame bezárása
    pygame.quit()
    sys.exit()

