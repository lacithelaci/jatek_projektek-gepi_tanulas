import pygame
import sys
from karakterekFeliratok import Player, JumpingEnemy, Bombs, win_or_lose, hp


def lvl1() -> None:
    # Pygame inicializálása
    pygame.init()

    # Képernyő beállítása
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Platformer Game Demo")

    # Színek
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    brown = (150, 75, 0)
    yellow = (255, 255, 0)
    green = (34, 139, 34)

    # Platformok
    platforms = [
        pygame.Rect(0 + 0 * 150, 550, 50, 50), pygame.Rect(0 + 1 * 150, 550, 50, 50),
        pygame.Rect(0 + 2 * 150, 550, 50, 50), pygame.Rect(0 + 3 * 150, 550, 50, 50),
        pygame.Rect(0 + 4 * 150, 550, 50, 50), pygame.Rect(0 + 5 * 150, 550, 50, 50),
        pygame.Rect(0, 340, 200, 50), pygame.Rect(330, 340, 200, 50), pygame.Rect(650, 340, 200, 50),
        pygame.Rect(700, 290, 50, 50), pygame.Rect(750, 240, 50, 100),
        pygame.Rect(0, 160, 700, 25)
    ]

    # cél
    goal = pygame.Rect(100, 10, 10, 150)

    # Teleport
    tp = pygame.Rect(750, 545, 50, 15)

    # Játékos példányosítása
    player = Player(0, 500, 50, 50)

    # ellenfelek példányosítása és tárolása
    enemies = [JumpingEnemy(100, 500, 15, 15), JumpingEnemy(250, 455, 15, 15), JumpingEnemy(400, 485, 15, 15),
               JumpingEnemy(550, 385, 15, 15), JumpingEnemy(700, 375, 15, 15),
               JumpingEnemy(570, 250, 15, 15), JumpingEnemy(250, 300, 15, 15)
               ]

    bombs = [Bombs(600, 130, 30, 30), Bombs(400, 130, 30, 30), Bombs(200, 130, 30, 30),
             Bombs(500, 130, 30, 30), Bombs(300, 130, 30, 30),
             ]

    # Élet
    lives = 20

    # Játék ciklus
    clock = pygame.time.Clock()

    # sikeresen befejeződött_e a játék?
    successful = False

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

        # teleportálás
        if player.rect.colliderect(tp):
            player = Player(0, 300, 50, 50)

        # Képernyő törlése
        screen.fill(white)

        # Játékos és platformok kirajzolása
        player.draw(screen, blue)

        for platform in platforms:
            pygame.draw.rect(screen, brown, platform)

        # ellenfelek kirajzolása és mozgatása és ütközések kezelése
        for index, enemy in enumerate(enemies, 1):
            enemy.draw(screen, red)
            if index <= 5:
                enemy.move(600, 399)
            else:
                enemy.move(350, 185)
            # ütközés
            if player.rect.colliderect(enemy):
                player = Player(0, 500, 50, 50)
                lives -= 1

        # bombák kirajzolása és ütközés
        for bomb in bombs:
            bomb.draw(screen, black)
            if player.rect.colliderect(bomb):
                player = Player(0, 500, 50, 50)
                lives -= 1

        # cél elérése és ahhoz kapcsolódó események

        if player.rect.colliderect(goal):
            successful = True
            run = False

        if lives < 0:
            run = False

        # tp kirajzolása
        pygame.draw.rect(screen, yellow, tp)

        # cél kirajzolása
        pygame.draw.rect(screen, green, goal)

        hp(screen, lives)

        # Képernyő frissítése
        pygame.display.flip()

        # FPS beállítása
        clock.tick(60)

    # győzelem vagy vereség felirat

    if successful:
        win_or_lose(screen_width, screen_height, screen, white, "You Win")
        pygame.display.flip()
    else:
        win_or_lose(screen_width, screen_height, screen, white, "You Lose")
        pygame.display.flip()

    # Pygame bezárása
    pygame.quit()
    sys.exit()


# main
def main() -> None:
    lvl1()


if __name__ == '__main__':
    main()
