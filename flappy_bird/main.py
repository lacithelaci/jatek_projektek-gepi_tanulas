import pygame
import sys
import random
from pygame.locals import *
from kor import Circle


def game() -> None:
    # inicializálás
    pygame.init()

    # képkockák
    fps = 60
    fpsClock = pygame.time.Clock()

    # képernyő és futás
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Flappy bird")
    run = True

    # színek
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (34, 139, 34)
    WHITE = (255, 255, 255)

    # koordináták
    labda_x, labda_y = 20, 300
    teglalap1_x, teglalap1_y = 760, 300
    teglalap1_szelesseg, teglalap1_magassag = 40, 800

    teglalap2_x, teglalap2_y = 760, -125
    teglalap2_szelesseg, teglalap2_magassag = 40, 300

    # betű betöltése pontszámláló és szöveg előkészítése
    pontszam = 0
    betu = pygame.font.Font(None, 36)

    # Game loop.
    while run:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_SPACE:
                    labda_y -= 40

        # érintő objektumok létrehozása
        teglalap1 = pygame.Rect(teglalap1_x, teglalap1_y, teglalap1_szelesseg, teglalap1_magassag)
        teglalap2 = pygame.Rect(teglalap2_x, teglalap2_y, teglalap2_szelesseg, teglalap2_magassag)
        kor = Circle(labda_x, labda_y, 20, RED, 2)

        # pontszám és megjelenítés
        text = betu.render(f'Pontszám: {pontszam}', True, WHITE)

        # adatok frissítése
        teglalap1_x -= 5
        teglalap2_x -= 5
        labda_y += 2

        # ütközés
        if kor.collides_with_rect(teglalap1):
            run = False
        if kor.collides_with_rect(teglalap2):
            run = False

        # csövek mozgása
        if teglalap1_x < -40:
            teglalap1_x = width - teglalap1_szelesseg
            teglalap1_y = random.randint(300, 400)
        if teglalap2_x < -40:
            teglalap2_x = width - teglalap2_szelesseg
            teglalap2_y = random.randint(-150, -100)
        if labda_x + 40 == teglalap2_x:
            pontszam += 1
        if labda_y < 0 or labda_y > 800:
            run = False

        # alakzatok kirajzolása
        pygame.draw.rect(screen, GREEN, teglalap1)
        pygame.draw.rect(screen, GREEN, teglalap2)
        # szöveg kirajzolása
        kor.draw(screen)
        screen.blit(text, (300, 30))
        pygame.display.flip()
        fpsClock.tick(fps)

    menu()
    pygame.quit()
    sys.exit()


def menu() -> None:
    # Pygame inicializálása
    pygame.init()

    # Ablak mérete
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Menü")

    # Színek
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    # Betűtípus beállítása
    font = pygame.font.Font(None, 74)

    # Gomb tulajdonságai
    button_width = 200
    button_height = 100
    button_color = GREEN
    button_x = (width - button_width) // 2
    button_y = (height - button_height) // 2

    # Fő ciklus változó
    running = True
    in_menu = True

    # Függvény a gomb megjelenítéséhez
    def draw_button(screen, text, x, y, width, height, color):
        pygame.draw.rect(screen, color, (x, y, width, height))
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        screen.blit(text_surface, text_rect)

    # Menü ciklus
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (button_x <= mouse_x <= button_x + button_width and
                        button_y <= mouse_y <= button_y + button_height):
                    in_menu = False
                elif (button_x <= mouse_x <= button_x + button_width and
                      button_y + 120 <= mouse_y <= 120 + button_y + button_height):
                    running = False

        screen.fill(BLACK)

        if in_menu:
            draw_button(screen, "Start", button_x, button_y, button_width, button_height, button_color)
            draw_button(screen, "Kilépés", button_x, button_y + 120, button_width, button_height, RED)
        else:
            game()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    jatekter = 'menu'
    if jatekter == 'menu':
        menu()
