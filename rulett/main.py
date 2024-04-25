import random

import pygame
import math

# Színek

hatter = (53, 113, 87)
feher = (172, 182, 198)
piros = (156, 12, 2)
fekete = (31, 29, 30)
zold = (53, 173, 84)
feher2 = (255, 255, 255)
sarga = (249, 194, 97)
sarga2 = (255, 252, 207)

# táblák

tabla = [["P", "F", "P", "P", "F", "P", "P", "F", "P", "P", "F", "P", "Z"],
         ["F", "P", "F", "F", "P", "F", "F", "P", "F", "F", "P", "F", "Z"],
         ["P", "F", "P", "F", "F", "P", "P", "F", "P", "F", "F", "P", "Z"]]

elso_sor_szoveg = ["3", "6", "9", "12", "15", "18", "21", "24", "27", "30", "33", "36"]
masodik_sor_szoveg = ["2", "5", "8", "11", "14", "17", "20", "23", "26", "29", "32", "35"]
harmadik_sor_szoveg = ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"]
sorhossz = len(elso_sor_szoveg)

# inicializálás
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Casino Rulette Game")
angle = 0
random_szam = ""
# Font objektum létrehozása
betutipus = pygame.font.Font(None, 30)

# képek
logo = pygame.image.load("kepek/rlogo.png")
kerek = pygame.image.load(("kepek/rkerek.png"))
sargabet = pygame.image.load("kepek/sarga.png").convert_alpha()
piros_bet = pygame.image.load("kepek/piros.png").convert_alpha()
zold_bet = pygame.image.load("kepek/zold.png").convert_alpha()
kek_bet = pygame.image.load("kepek/kek.png").convert_alpha()
fekete_bet = pygame.image.load("kepek/fekete.png").convert_alpha()
eger = pygame.image.load("kepek/mousepos.png").convert_alpha()

# betek pozicionálása és érintő pontok
sargabet_rect = sargabet.get_rect()
sargabet_rect.center = (374, 545)
piros_bet_rect = piros_bet.get_rect()
piros_bet_rect.center = (438, 545)
zold_bet_rect = zold_bet.get_rect()
zold_bet_rect.center = (501, 545)
kek_bet_rect = kek_bet.get_rect()
kek_bet_rect.center = (563, 545)
fekete_bet_rect = fekete_bet.get_rect()
fekete_bet_rect.center = (625, 545)

# egyenleg
egyenleg = 100000
tet = 0

# Lista a másolatok tárolására
zseton_masolat_lista = list()
osszegek = list()
ismetelt_osszegek = []
ismetelt_zseton_lista = []
# gombok
torles = pygame.Rect(255, 524, 87, 42)
vissza = pygame.Rect(154, 524, 86, 42)
start = pygame.Rect(682, 524, 113, 42)
ismetles = pygame.Rect(42, 524, 95, 42)
# 5. sor tárolása
piros1 = pygame.Rect(350, 454, 103, 56)
fekete1 = pygame.Rect(455, 454, 96, 53)


# game loop
def teglalap_kirajzolasa(screen, szin, x, y, szelesseg, magassag):
    # téglalap rajzolása
    pygame.draw.rect(screen, szin, (x, y, szelesseg, magassag))


def szoveget_kirajzol(screen, szoveg, szoveg_x, szoveg_y, betumeret=30, szin=feher, betutipus=None, forgatas=False):
    if betutipus is None:
        betutipus = pygame.font.Font(None, betumeret)
    megjelenitendo_szoveg = betutipus.render(szoveg, True, szin)

    if forgatas:
        megjelenitendo_szoveg = pygame.transform.rotate(megjelenitendo_szoveg, 90)
    screen.blit(megjelenitendo_szoveg, (szoveg_x, szoveg_y))


running = True
while running:
    # egér pozíció
    pos = pygame.mouse.get_pos()
    screen.fill(hatter)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # q-val ki lehet lépni
            if event.key == pygame.K_q:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # sárgabet érintőpont és zsetonok másolása
            if sargabet_rect.collidepoint(pos):
                sargabet_masolat = sargabet.copy()
                sargabet_masolat_rect = sargabet_masolat.get_rect()
                sargabet_masolat_rect.topleft = event.pos
                zseton_masolat_lista.append((sargabet_masolat, sargabet_masolat_rect))
                osszegek.append(5)
                egyenleg -= 5

            # piros érintőpont és zsetonok másolása
            elif piros_bet_rect.collidepoint(pos):
                piros_bet_masolat = piros_bet.copy()
                piros_bet_masolat_rect = piros_bet_masolat.get_rect()
                piros_bet_masolat_rect.topleft = event.pos
                zseton_masolat_lista.append((piros_bet_masolat, piros_bet_masolat_rect))
                osszegek.append(10)
                egyenleg -= 10

            # zöld érintőpont és zsetonok másolása
            elif zold_bet_rect.collidepoint(pos):
                zold_bet_masolat = zold_bet.copy()
                zold_bet_masolat_rect = zold_bet_masolat.get_rect()
                zold_bet_masolat_rect.topleft = event.pos
                zseton_masolat_lista.append((zold_bet_masolat, zold_bet_masolat_rect))
                osszegek.append(20)
                egyenleg -= 20
            # kék érintőpont és zsetonok másolása
            elif kek_bet_rect.collidepoint(pos):
                kek_bet_masolat = kek_bet.copy()
                kek_bet_masolat_rect = kek_bet_masolat.get_rect()
                kek_bet_masolat_rect.topleft = event.pos
                zseton_masolat_lista.append((kek_bet_masolat, kek_bet_masolat_rect))
                osszegek.append(50)
                egyenleg -= 50

            # fekete érintőpontok és zsetonok másolása
            elif fekete_bet_rect.collidepoint(pos):
                fekete_bet_masolat = fekete_bet.copy()
                fekete_bet_masolat_rect = fekete_bet_masolat.get_rect()
                fekete_bet_masolat_rect.topleft = event.pos
                zseton_masolat_lista.append((fekete_bet_masolat, fekete_bet_masolat_rect))
                osszegek.append(100)
                egyenleg -= 100

            # törlés gomb működése
            elif torles.collidepoint(pos):
                ismetelt_osszegek = osszegek
                ismetelt_zseton_lista = zseton_masolat_lista
                zseton_masolat_lista = []
                egyenleg += sum(osszegek)
                osszegek = []


            # vissza gomb működése
            elif vissza.collidepoint(pos):
                if len(zseton_masolat_lista) > 0:
                    zseton_masolat_lista.pop(-1)
                    egyenleg += osszegek[-1]
                    osszegek.pop(-1)

            elif ismetles.collidepoint(pos):
                if sum(ismetelt_osszegek) != 0:
                    osszegek = ismetelt_osszegek
                    zseton_masolat_lista = ismetelt_zseton_lista


            # start gomb működése
            elif start.collidepoint(pos):
                random_szam = random.randint(0, 36)
                zseton_masolat_lista = []
                osszegek = []

        print(event)

    # Egyenleg
    utolso_nyeremeny = ""
    pygame.draw.rect(screen, sarga, (40, 20, 260, 100), 3)
    szoveget_kirajzol(screen, f"HUF: {egyenleg}", 45, 30, 10, feher, betutipus)
    szoveget_kirajzol(screen, f"Tét: {tet}", 45, 60, 10, feher, betutipus)
    szoveget_kirajzol(screen, f"Utolsó Nyeremény: {utolso_nyeremeny}", 45, 90, 10, feher, betutipus)

    # tabla 1-3 sorának kirajzolasához a változók
    uj_sorkezdes = 0
    tabla_x_koordinata = 150
    tabla_y_koordinata = 160
    teglalap_szelessege = 52
    teglalap_hossza = 82

    # tábla 1-3 sorának kirajzolása
    for i in range(3):
        for y in range(0, len(tabla[0]) - 1):

            if tabla[i][y] == "P":
                pygame.draw.rect(screen, piros, (
                    tabla_x_koordinata + y * 50, tabla_y_koordinata, teglalap_szelessege, teglalap_hossza))

            else:
                pygame.draw.rect(screen, fekete, (
                    tabla_x_koordinata + y * 50, tabla_y_koordinata, teglalap_szelessege, teglalap_hossza))
            uj_sorkezdes += 1

        if uj_sorkezdes == 12:
            tabla_y_koordinata += 83

        if uj_sorkezdes == 24:
            tabla_y_koordinata += 77
            teglalap_hossza = 78

    # 1. sor számok
    for i in range(0, sorhossz):
        szoveget_kirajzol(screen, f"{elso_sor_szoveg[i]}", 165 + i * 50, 195, 50, feher, betutipus, forgatas=True)

    # 2. sor számok
    for i in range(0, sorhossz):
        szoveget_kirajzol(screen, f"{masodik_sor_szoveg[i]}", 165 + i * 50, 195 + 75, 50, feher, betutipus,
                          forgatas=True)
    # 3. sor számok
    for i in range(0, sorhossz):
        szoveget_kirajzol(screen, f"{harmadik_sor_szoveg[i]}", 165 + i * 50, 195 + 150, 50, feher, betutipus,
                          forgatas=True)

    # fehér vonalak kirajzolása
    feher_vonal_y = 160
    feher_vonal_uj_sor = 0

    for i in range(0, 3):
        if i == 1:
            feher_vonal_y += 80
        if i == 2:
            feher_vonal_y += 80

        for y in range(150, 800, 50):
            # felső vonal
            pygame.draw.line(screen, feher, (y, feher_vonal_y), (y + 50, feher_vonal_y), 3)
            # oldalsó vonal
            oldalso_vonal = pygame.Rect(y, feher_vonal_y, 3, 80)
            # alsó vonalak
            pygame.draw.line(screen, feher, (y, feher_vonal_y + 80), (y + 50, feher_vonal_y + 80), 3)
            feher_vonal_uj_sor += 1
            # sárga vagy fehér
            if oldalso_vonal.collidepoint(pos):
                pygame.draw.rect(screen, sarga, oldalso_vonal, 3)
            else:
                pygame.draw.rect(screen, feher, oldalso_vonal, 3)

    # 4. sor
    pygame.draw.rect(screen, feher, (150, 398, 203, 55), 3)
    pygame.draw.rect(screen, feher, (150, 398, 603, 55), 3)
    pygame.draw.rect(screen, feher, (150, 398, 403, 55), 3)

    # tucatok kirajzolása
    for i in range(0, 3):
        szoveget_kirajzol(screen, f"{i + 1}. tucat", 200 * i + 200, 420, 10, feher, betutipus)

    # 5. sor
    pygame.draw.rect(screen, piros, piros1)
    pygame.draw.rect(screen, fekete, fekete1)
    pygame.draw.rect(screen, feher, (150, 450, 603, 60), 3)
    pygame.draw.rect(screen, feher, (150, 450, 203, 60), 3)
    pygame.draw.rect(screen, feher, (150, 450, 403, 60), 3)
    pygame.draw.rect(screen, feher, (253, 450, 100, 60), 3)
    pygame.draw.rect(screen, feher, (453, 450, 100, 60), 3)
    pygame.draw.rect(screen, feher, (653, 450, 100, 60), 3)

    # szövegek kirajzolása
    szoveget_kirajzol(screen, f"páratlan", 560, 470, 10, feher, betutipus)
    szoveget_kirajzol(screen, f"magas", 660, 470, 10, feher, betutipus)
    szoveget_kirajzol(screen, f"páros", 270, 470, 10, feher, betutipus)
    szoveget_kirajzol(screen, f"alacsony", 155, 470, 10, feher, betutipus)

    # oldalsó bizbasz
    pygame.draw.line(screen, feher, (115, 161), (150, 161), 2)
    pygame.draw.line(screen, feher, (115, 394), (150, 396), 2)
    pygame.draw.line(screen, feher, (115, 161), (105, 188), 2)
    pygame.draw.line(screen, feher, (115, 394), (105, 367), 2)
    pygame.draw.line(screen, feher, (105, 190), (105, 365), 2)
    pygame.draw.ellipse(screen, zold, (114, 245, 30, 72))  # 0

    # elozmeny
    pygame.draw.rect(screen, feher, (590, 20, 225, 50), 3)
    szoveget_kirajzol(screen, f"Sorsolt szám: {random_szam}", 600, 35, 10, feher, betutipus)

    # Kerek
    pygame.display.set_icon(logo)
    screen.blit(kerek, (375, 15))
    x = 440
    y = 80
    pygame.draw.circle(screen, feher, (x, y), 45, 2)
    golyocska = pygame.draw.circle(screen, feher2, (53 * math.cos(angle) + x, 53 * math.sin(angle) + y), 3)
    angle += 0.03

    # gombok

    # ismetles
    pygame.draw.rect(screen, sarga, (38, 520, 103, 50), 3)
    pygame.draw.rect(screen, sarga2, ismetles)
    szoveget_kirajzol(screen, f"ismétlés", 45, 537, 10, feher, betutipus)

    # start
    pygame.draw.rect(screen, sarga, (678, 520, 122, 50), 3)
    pygame.draw.rect(screen, sarga2, start)
    szoveget_kirajzol(screen, f"start", 715, 537, 10, feher, betutipus)

    # vissza
    pygame.draw.rect(screen, sarga, (149, 520, 96, 50), 3)
    pygame.draw.rect(screen, sarga2, vissza)
    szoveget_kirajzol(screen, f"vissza", 163, 537, 10, feher, betutipus)

    # torles
    pygame.draw.rect(screen, sarga2, torles)
    pygame.draw.rect(screen, sarga, (251, 520, 96, 50), 3)
    szoveget_kirajzol(screen, f"törlés", 270, 537, 10, feher, betutipus)

    # Zseton mozgatás
    for masolt_zsetonok, masolt_zsetonok_rect in zseton_masolat_lista:
        if pygame.mouse.get_pressed()[0]:
            if masolt_zsetonok_rect.collidepoint(pygame.mouse.get_pos()):
                masolt_zsetonok_rect.center = pygame.mouse.get_pos()
    # másolt zseton kirajzolás
    for masolt_zsetonok, masolt_zsetonok_rect in zseton_masolat_lista:
        screen.blit(masolt_zsetonok, masolt_zsetonok_rect)

    # eredeti zsetonok megjelenítése
    screen.blit(sargabet, sargabet_rect)
    screen.blit(piros_bet, piros_bet_rect)
    screen.blit(zold_bet, zold_bet_rect)
    screen.blit(kek_bet, kek_bet_rect)
    screen.blit(fekete_bet, fekete_bet_rect)

    # eger
    egkep = screen.blit(eger, (-100, -10))
    pygame.mouse.set_visible(False)
    egkep.center = pos
    screen.blit(eger, egkep)

    # képfrissítés
    pygame.display.update()

    # Képkocka frissítése
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
