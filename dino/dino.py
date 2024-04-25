# Készítette: Szemán László
import pygame
import random

# könyvtárak
pygame.init()

size = (800, 600)
# képernyőméret
ablak = pygame.display.set_mode(size)
# képernyőméret megjelenítése
pygame.display.set_caption('Chrome Dino 1.2.0.')
# fejléc

kek = (0, 0, 255)
fekete = (0, 0, 0)
piros = (255, 0, 0)
feher = (255, 255, 255)
szurke = (200, 200, 200)
# színek
dinox = 20
dinoy = 300
kaktusx = 780
kaktusy = 315
retryx = -100
retryy = -100
valtozas = 0
fps = random.randint(1, 60)
pont = 0
pont2 = 0
legjobb_pont = 0
gyorsasag = (-10)
felhox = 500
felhox2 = 150
felho3x = 850
playx = 400
playy = 300
game_over = True
jump = True
Gameover = "Game Over"
# változók
basic_font = pygame.font.SysFont('Times New Roman', 25)
# betűtípus
pygame.mixer.init()
jump_hang = pygame.mixer.Sound("hangok/jump.mp3")
over = pygame.mixer.Sound("hangok/ovr.mp3")
pygame.joystick.init()
# hangok


dino = pygame.image.load('kepek/dino.jfif')
kaktus = pygame.image.load('kepek/th.jfif')
retry = pygame.image.load('kepek/retry.PNG')
felho = pygame.image.load('kepek/felho.PNG')
felho2 = pygame.image.load('kepek/felho.PNG')
felho3 = pygame.image.load('kepek/felho.PNG')
lacithelaci = pygame.image.load('kepek/lacithelaci.PNG')
play = pygame.image.load('kepek/play.PNG')
# képek beolvasása
clock = pygame.time.Clock()
vege = False
# Játék futása
while not vege:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vege = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                vege = True
        if jump:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    valtozas = -10
                    jump = False
                    pygame.mixer.Sound.play(jump_hang)
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 0:
                    valtozas = -10
                    jump = False
                    pygame.mixer.Sound.play(jump_hang)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if button1.collidepoint((mx, my)):
                kaktusx = 780
                pont = 0
                pont2 = 0
                game_over = False
                retryy = -100
                retryx = -100
                gyorsasag = -10
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if playbutton.collidepoint((mx, my)):
                game_over = False
                playy = -1000

    # pygame eventek
    if game_over == False:
        dinoy += valtozas
        if dinoy >= 300:
            dinoy = 300
            jump = True
            fps = random.randint(59, 61, )
        if dinoy < 200:
            valtozas = 5
        kaktusx += gyorsasag
        if kaktusx < 0:
            kaktusx = 780
            pont += 1
            pont2 += 1
        if dinox in range(kaktusx - 50, kaktusx) and dinoy in range(kaktusy - 60, kaktusy):
            game_over = True
            retryx = 400
            retryy = 300
            pygame.mixer.Sound.play(over)
            if pont2 > legjobb_pont:
                legjobb_pont = pont2
        if felhox < -220:
            felhox = 800
        if felhox2 < -220:
            felhox2 = 800
        if felho3x < -220:
            felho3x = 800
        felhox2 -= 1
        felhox -= 1
        felho3x -= 1
    if pont % 10 == 0:
        pont = 1
        gyorsasag -= 1
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

    # Feltételek
    pontok = basic_font.render(f'Score: {pont2}', False, szurke)
    GameOver = basic_font.render(f'{Gameover}', False, szurke)
    fpskep = basic_font.render(f'FPS: {(fps):.1f}', False, szurke)
    legjobb = basic_font.render(f'Best Score: {(legjobb_pont)}', False, szurke)
    # Szöveges változók
    ablak.fill(feher)
    ablak.blit(dino, (dinox, dinoy))
    ablak.blit(kaktus, (kaktusx, kaktusy))
    ablak.blit(pontok, (30, 30))
    ablak.blit(GameOver, (retryx - 40, retryy - 30))
    ablak.blit(fpskep, (680, 20))
    ablak.blit(felho, (felhox, 100))
    ablak.blit(felho2, (felhox2, 100))
    ablak.blit(felho3, (felho3x, 100))
    ablak.blit(lacithelaci, (100, 450))
    ablak.blit(legjobb, (30, 60))
    pygame.draw.rect(ablak, fekete, (0, 365, 1000, 1))
    playbutton = pygame.draw.rect(ablak, fekete, (playx + 6, playy + 6, 30, 30))
    ablak.blit(play, (playx, playy))
    button1 = pygame.draw.rect(ablak, fekete, (retryx, retryy, 42, 35))
    ablak.blit(retry, (retryx, retryy))
    # Változók megjelenítése
    pygame.display.flip()
    clock.tick(fps)
    # FPS korlátozás
