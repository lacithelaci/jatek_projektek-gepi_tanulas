#all rights reserved, ha kereskednél vele, donétold nekem a 50%-át a profitból
# Van még benne elég sok hiba, de nem annyi mint a szájberpánkban, meg ez egy ingyenes játék szóval don't panic, majd kijavítom
import pygame

pygame.init()

size = (800, 600)
pygame.display.set_caption('Szegény Ember Pong-ja 0.9.5 Beta')
#ablak neve
ablak = pygame.display.set_mode(size)
# ablak mérete
szurke = (200, 200, 200)
"""mixer.music.load('muzsika.mp3')
mixer.music.play(-1)"""
#muzsika lejátszó
"""hatter=pygame.image.load('kep.jfif')"""
#háttér beolvasás
kek = (0,0,255)
fekete = (0,0,0)
piros = (255,0,0)
zold=(124,252,0)
feher=(255,255,255)
#színek
r = 30
kx = 300
ky = 300
alma=560
dx = 5
dy = 5
x = 300
udx = 5
xd=60
laci=300
laciudx=5
pont = 0
nulla=0
jatekos1_pont = 0
jatekos2_pont = 0
basic_font = pygame.font.Font('freesansbold.ttf', 32)
alma2=750
#kordináták, betűméret, és a többi alap
clock = pygame.time.Clock()
#idő
vege = False
#emiatt indul az egész







while not vege:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vege = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                udx =- 5
            if event.key == pygame.K_d:
                udx += 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                udx = 0
            if event.key == pygame.K_d:
                udx = 0
        #játékos egy mozgása
        if event.type == pygame.QUIT:
            vege = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                laciudx =- 5
            if event.key == pygame.K_RIGHT:
                laciudx = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                laciudx = 0
            if event.key == pygame.K_RIGHT:
                laciudx = 0
        #játékos 2 mozgása
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                vege = True
        #gyors kilépés

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_b:
                alma2=50
            if event.key == pygame.K_b:
                alma2=50
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_j:
                alma2=750
            if event.key == pygame.K_j:
                alma2=750
        #változtatás

    ablak.fill(fekete)
   # ablak.blit(hatter,(0,0))
    #hattér betöltés
    pygame.draw.rect(ablak, kek, (x, alma, 200, 30))
    pygame.draw.rect(ablak,zold,(laci,nulla, 200, 30))
    labda=pygame.draw.circle(ablak, piros, (kx , ky), r)
    # mozgó dolgok
    pygame.draw.rect(ablak, feher, (0, 0, 10, 800))
    pygame.draw.rect(ablak, feher, (790, 0, 10, 800))
    pygame.draw.rect(ablak, feher, (10, 0, 800, 5))
    pygame.draw.rect(ablak, feher, (10, 595, 800, 5))
    pygame.draw.rect(ablak, feher, (10, 300, 800, 5))
    #pálya rajza




    kx += dx
    ky += dy
    x += udx
    laci += laciudx
    if x < 0:
        x = 0

    if laci < 0:
        laci = 0

    if x + 200 > 800:
        x = 600

    if laci + 200 > 800:
        laci = 600

    if kx > 800 - r or kx<r:
        dx =- dx

    if ky<r:
        dy =- dy

    if ky > 600 - r:
        jatekos2_pont += 1

        kx = 400
        ky = 300
        x = 300
        laci = 300

    if ky < 0 + r:

        jatekos1_pont += 1

        kx = 400
        ky = 300
        x = 300
        laci = 300
    #ne mennyen ki a labda  a pályáról, reset funkciók,labda mozgása, visszapattanás stb
    jatekos1_gyozelem = basic_font.render(f"A győztes a játékos1! {jatekos1_pont}:{jatekos2_pont} arányra", False,(feher))
    jatekos2_gyozelem = basic_font.render(f"A győztes a játékos2! {jatekos2_pont}:{jatekos1_pont} arányra", False,(feher))
    basic_font = pygame.font.Font('freesansbold.ttf', 32)
    #pontok, betűtípus, betűméret, és a többi hülyeség
    if kx in range(x, x + 201) and ky > 560 - r:
        dy =- dy


    if kx in range(laci, laci + 201) and ky < 30 + r:
        dy= -dy
    #labda visszapattanása az ütőkről


    jatekos_szoveg = basic_font.render(f'{jatekos1_pont}', False, szurke)
    ablak.blit(jatekos_szoveg, (alma2, 560))

    jatekos2_szoveg = basic_font.render(f'{jatekos2_pont}', False, szurke)
    ablak.blit(jatekos2_szoveg, (alma2, 20))
    # pontok megjelenése
    if jatekos1_pont==7:
        print(f"A győztes a játékos1! {jatekos1_pont}:{jatekos2_pont} arányra")
        ablak.blit(jatekos1_gyozelem, (100, 400))
        pygame.time.wait(2000)
        vege=True
    # játekos egy győzelme


    if jatekos2_pont==7:
        print(f"A győztes a játékos2! {jatekos2_pont}:{jatekos1_pont} arányra")
        ablak.blit(jatekos2_gyozelem, (100, 400))

        pygame.time.wait(2000)
        vege=True
    # játékos 2 győzelme



    pygame.display.flip()
    clock.tick(xd)
    #gyorsítás
    #Készítette: Szemán László









    #Tesztelte:  Jónás Ábris
    #            Juhász Bence
    #            Németh Gergő
    #Külön köszönet Ladányi Attilának a játék egyik funkciójáért

    """Patch Notes(0.9.5): 
    -ESC:gyors kilépés
    -Pontrendszer működése
    -Reset funkció
    -Félig meddig működő ending screen
    -Pálya kirajzolása
                            """
    """
    Várható frissítések az 1.0-ig:
    -ending screen tökéletesítése
    -lehetőleg már .exe-ből lesz indítható a játék
    -valószínüleg már csak 1-2 update lesz és új játeékba kezdek
    """
    """
    Játék irányítása és logikája:
    P1: A-D
    p2:nyilak
    Cél: a labdát be kell ütni az ellenfél kapujába, az győz aki hamarabb éri el a 7 pontot
    """