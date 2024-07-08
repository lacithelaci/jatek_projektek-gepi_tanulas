import pygame
import sys
from lvl1 import lvl1


def menu() -> None:
    # Pygame inicializálása
    pygame.init()

    # Színek
    red = (255, 0, 0)
    green = (0, 255, 0)

    # Ablak létrehozása
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Menu')

    # Háttérkép betöltése
    background = pygame.image.load('kepek/menu.jpeg').convert()
    background = pygame.transform.scale(background, (850, 600))

    # gombok
    play = pygame.Rect(148, 496, 250, 80)
    kilep = pygame.Rect(420, 495, 250, 80)

    # Fő ciklus
    running = True
    while running:

        # Események kezelése
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if play.collidepoint(mouse_pos):
                    lvl1()

                elif kilep.collidepoint(mouse_pos):
                    running = False

        # gombok kirajzolása
        pygame.draw.rect(screen, red, play)
        pygame.draw.rect(screen, green, kilep)

        # Háttérkép megjelenítése
        screen.blit(background, (0, 0))

        # Frissítés
        pygame.display.flip()

    # Pygame bezárása
    pygame.quit()
    sys.exit()


def main() -> None:
    menu()


if __name__ == '__main__':
    main()
