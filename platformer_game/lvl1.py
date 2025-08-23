import pygame
import sys
from karakterekFeliratok import Player, JumpingEnemy, Bombs, hp, display_fps, win_or_lose
from lvl2 import lvl2


def lvl1() -> None:
    # Pygame inicializálása
    pygame.init()
    pygame.mixer.init()

    # hangok importálása
    explosions: pygame.mixer.Sound = pygame.mixer.Sound('hangok/bomba_robbanas.wav')
    punch: pygame.mixer.Sound = pygame.mixer.Sound('hangok/punch.mp3')
    teleporting: pygame.mixer.Sound = pygame.mixer.Sound('hangok/teleport.mp3')

    # Képernyő beállítása
    screen_width: int = 800
    screen_height: int = 600
    screen: pygame.Surface = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Platformer Game Demo")

    # Színek
    blue: tuple[int, int, int] = (0, 0, 255)
    brown: tuple[int, int, int] = (150, 75, 0)
    green: tuple[int, int, int] = (34, 139, 34)

    # Zászló betöltése és átméretezése
    original_flag_image: pygame.Surface = pygame.image.load('kepek/flag.png').convert_alpha()
    new_flag_image: pygame.Surface = pygame.transform.scale(original_flag_image, (80, 160)).convert_alpha()
    flag_rect: pygame.Rect = new_flag_image.get_rect()
    flag_rect.topleft = (70, 5)

    # Teleportok betöltése, átméretezése
    original_tp_image: pygame.Surface = pygame.image.load('kepek/teleport.png').convert_alpha()
    new_tp_image: pygame.Surface = pygame.transform.scale(original_tp_image, (40, 120)).convert_alpha()
    tp_rect1: pygame.Rect = new_tp_image.get_rect()
    tp_rect1.topleft = (750, 433)
    tp_rect2: pygame.Rect = new_tp_image.get_rect()
    tp_rect2.topleft = (0, 225)

    # szív kirajzolása
    original_hp_image: pygame.Surface = pygame.image.load('kepek/heart.png').convert_alpha()
    new_hp_image: pygame.Surface = pygame.transform.scale(original_hp_image, (75, 75)).convert_alpha()
    hp_rect: pygame.Rect = new_hp_image.get_rect()
    hp_rect.topleft = (15, 30)

    # Játékos példányosítása
    player: Player = Player(0, 500, 50, 50)

    # Élet
    lives: int = 20

    # Platformok
    platforms: list[pygame.Rect] = [
        pygame.Rect(0 + 0 * 150, 550, 50, 50), pygame.Rect(0 + 1 * 150, 550, 50, 50),
        pygame.Rect(0 + 2 * 150, 550, 50, 50), pygame.Rect(0 + 3 * 150, 550, 50, 50),
        pygame.Rect(0 + 4 * 150, 550, 50, 50), pygame.Rect(0 + 5 * 150, 550, 50, 50),
        pygame.Rect(0, 340, 200, 50), pygame.Rect(330, 340, 200, 50), pygame.Rect(650, 340, 200, 50),
        pygame.Rect(700, 290, 50, 50), pygame.Rect(750, 240, 50, 100),
        pygame.Rect(0, 160, 700, 25)
    ]

    # fű kirajzolása
    grasses: list[pygame.Rect] = [
        pygame.Rect(0 + 0 * 150, 550, 50, 25), pygame.Rect(0 + 1 * 150, 550, 50, 25),
        pygame.Rect(0 + 2 * 150, 550, 50, 25), pygame.Rect(0 + 3 * 150, 550, 50, 25),
        pygame.Rect(0 + 4 * 150, 550, 50, 25), pygame.Rect(0 + 5 * 150, 550, 50, 25),
        pygame.Rect(0, 340, 200, 25), pygame.Rect(330, 340, 200, 25), pygame.Rect(650, 340, 200, 25),
        pygame.Rect(700, 290, 50, 25), pygame.Rect(750, 240, 50, 25),
        pygame.Rect(0, 160, 700, 12.5)
    ]

    # ellenfelek példányosítása és tárolása
    enemies: list[JumpingEnemy] = [
        JumpingEnemy(100, 500, 30, 30), JumpingEnemy(250, 455, 30, 30), JumpingEnemy(400, 485, 30, 30),
        JumpingEnemy(550, 385, 30, 30), JumpingEnemy(700, 375, 30, 30),
        JumpingEnemy(570, 250, 30, 30), JumpingEnemy(250, 300, 30, 30)
    ]

    # bombák példányosítása és tárolása
    bombs: list[Bombs] = [
        Bombs(600, 130, 30, 30), Bombs(400, 130, 30, 30), Bombs(200, 130, 30, 30),
        Bombs(500, 130, 30, 30), Bombs(300, 130, 30, 30),
    ]

    # Játék ciklus
    clock: pygame.time.Clock = pygame.time.Clock()

    # sikeresen befejeződött_e a játék?
    successful: bool = False

    # Alapértelmezett betűtípus beállítása
    font: pygame.font.Font = pygame.font.Font(None, 36)

    # A játék futása
    run: bool = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False

        # játékosmozgás
        keys: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        player.move(keys, screen_width)
        player.apply_gravity()
        player.check_collision(platforms)

        # halálok
        if player.rect.y > 800:
            player = Player(0, 500, 50, 50)
            lives -= 1

        # Képernyő törlése
        screen.fill((135, 206, 235))

        # Játékos, platformok és fű kirajzolása
        player.draw(screen, blue)

        for platform in platforms:
            pygame.draw.rect(screen, brown, platform)

        for grass in grasses:
            pygame.draw.rect(screen, green, grass)

        # ellenfelek kirajzolása és mozgatása és

        # ellenfelek kirajzolása és mozgatása és ütközések kezelése
        for index, enemy in enumerate(enemies, 1):
            enemy.draw(screen)
            if index <= 5:
                enemy.move(399, 600)
            else:
                enemy.move(185, 350)
            # ütközés
            if player.rect.colliderect(enemy):
                punch.play()
                pygame.time.wait(200)
                player = Player(0, 500, 50, 50)
                lives -= 1

        # bombák kirajzolása és ütközés
        for bomb in bombs:
            bomb.draw(screen)
            if bomb.rect.colliderect(player):
                explosions.play()
                player = Player(0, 500, 50, 50)
                lives -= 1

        # cél elérése és ahhoz kapcsolódó események
        if player.rect.colliderect(flag_rect):
            successful = True
            run = False

        # elveszített összes HP
        if lives < 0:
            run = False

        # teleportálások
        if player.rect.colliderect(tp_rect1):
            player = Player(50, 300, 50, 50)
            teleporting.play()

        if player.rect.colliderect(tp_rect2):
            player = Player(0, 500, 50, 50)
            teleporting.play()

        # tp-k kirajzolása
        screen.blit(new_tp_image, tp_rect1)
        screen.blit(new_tp_image, tp_rect2)

        # zászló kirajzolása
        screen.blit(new_flag_image, flag_rect)

        # HP megjelenítése
        screen.blit(new_hp_image, hp_rect)
        hp(screen, lives)

        # FPS megjelenítése
        display_fps(screen, clock, font)

        # Képernyő frissítése
        pygame.display.flip()

        # FPS beállítása
        clock.tick(60)

    if successful:
        lvl2()
    else:
        win_or_lose(screen_width, screen_height, screen, (255, 255, 255), "You Lose")

    # Pygame bezárása
    pygame.quit()
    sys.exit()

