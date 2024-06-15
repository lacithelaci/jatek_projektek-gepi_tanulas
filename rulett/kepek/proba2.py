import pygame
import os

# Inicializálás
pygame.init()

# Képernyő mérete
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Kép mozgatás")

# Színek
WHITE = (255, 255, 255)

# Képek betöltése
image = pygame.image.load("fekete.png")
image_rect = image.get_rect()

# Lista a másolatok tárolására
image_copies = []

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Bal kattintás
                if image_rect.collidepoint(event.pos):
                    # Készíts másolatot az eredeti képről
                    image_copy = image.copy()
                    image_copy_rect = image_copy.get_rect()
                    image_copy_rect.topleft = event.pos
                    image_copies.append((image_copy, image_copy_rect))

    # Mozgatás
    for image_copy, image_copy_rect in image_copies:
        if pygame.mouse.get_pressed()[0]:  # Ha lenyomva van a bal gomb
            if image_copy_rect.collidepoint(pygame.mouse.get_pos()):
                image_copy_rect.center = pygame.mouse.get_pos()

    # Képek kirajzolása
    screen.blit(image, image_rect)
    for image_copy, image_copy_rect in image_copies:
        screen.blit(image_copy, image_copy_rect)

    pygame.display.flip()

pygame.quit()
