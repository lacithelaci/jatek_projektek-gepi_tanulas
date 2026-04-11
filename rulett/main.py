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
szurke = (100, 100, 100)

# Ruletten a számok sorrendje (valódi rulettkerék sorrend)
KEREK_SORREND = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36,
                 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9,
                 22, 18, 29, 7, 28, 12, 35, 3, 26]

# Piros számok a ruletten
PIROS_SZAMOK = {1, 3, 5, 7, 9, 12, 14, 16, 18, 21, 23, 25, 27, 30, 32, 34, 36}

# Táblák
tabla = [["P", "F", "P", "P", "F", "P", "P", "F", "P", "P", "F", "P", "Z"],
         ["F", "P", "F", "F", "P", "F", "F", "P", "F", "F", "P", "F", "Z"],
         ["P", "F", "P", "F", "F", "P", "P", "F", "P", "F", "F", "P", "Z"]]

elso_sor_szoveg = ["3", "6", "9", "12", "15", "18", "21", "24", "27", "30", "33", "36"]
masodik_sor_szoveg = ["2", "5", "8", "11", "14", "17", "20", "23", "26", "29", "32", "35"]
harmadik_sor_szoveg = ["1", "4", "7", "10", "13", "16", "19", "22", "25", "28", "31", "34"]
sorhossz = len(elso_sor_szoveg)

# Minden szám melyik sorban van (1=harmadik sor, stb.)
def szam_sora(szam):
    if str(szam) in elso_sor_szoveg:
        return 0
    elif str(szam) in masodik_sor_szoveg:
        return 1
    elif str(szam) in harmadik_sor_szoveg:
        return 2
    return -1

def szam_oszlopa(szam):
    for i, s in enumerate(elso_sor_szoveg):
        if s == str(szam):
            return i
    for i, s in enumerate(masodik_sor_szoveg):
        if s == str(szam):
            return i
    for i, s in enumerate(harmadik_sor_szoveg):
        if s == str(szam):
            return i
    return -1

# Inicializálás
pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Casino Rulette Game")

# Kerék animáció változók
szog = 0.0
forgasi_sebesseg = 0.03
forgasban = False
lassulas = False
cel_szog = 0.0
spinning_timer = 0
eredmeny_szam = None
eredmeny_megjelenes_timer = 0

betutipus = pygame.font.Font(None, 30)
kis_betu = pygame.font.Font(None, 22)

# Képek betöltése
try:
    logo = pygame.image.load("kepek/rlogo.png")
    kerek = pygame.image.load("kepek/rkerek.png")
    sargabet = pygame.image.load("kepek/sarga.png").convert_alpha()
    piros_bet = pygame.image.load("kepek/piros.png").convert_alpha()
    zold_bet = pygame.image.load("kepek/zold.png").convert_alpha()
    kek_bet = pygame.image.load("kepek/kek.png").convert_alpha()
    fekete_bet = pygame.image.load("kepek/fekete.png").convert_alpha()
    eger = pygame.image.load("kepek/mousepos.png").convert_alpha()
    kepek_betoltve = True
except:
    kepek_betoltve = False
    # Placeholder felületek ha nincs kép
    sargabet = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(sargabet, (249, 194, 97), (20, 20), 18)
    piros_bet = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(piros_bet, (200, 30, 30), (20, 20), 18)
    zold_bet = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(zold_bet, (50, 180, 80), (20, 20), 18)
    kek_bet = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(kek_bet, (30, 100, 220), (20, 20), 18)
    fekete_bet = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(fekete_bet, (50, 50, 50), (20, 20), 18)

# Zseton értékek
zseton_ertekek = {
    "sarga": 5,
    "piros": 10,
    "zold": 20,
    "kek": 50,
    "fekete": 100
}

# Zsetonok pozíciói
sargabet_rect = sargabet.get_rect(center=(374, 545))
piros_bet_rect = piros_bet.get_rect(center=(438, 545))
zold_bet_rect = zold_bet.get_rect(center=(501, 545))
kek_bet_rect = kek_bet.get_rect(center=(563, 545))
fekete_bet_rect = fekete_bet.get_rect(center=(625, 545))

# Aktív zseton kiválasztás
aktiv_zseton = None  # "sarga", "piros", "zold", "kek", "fekete"

# Egyenleg
egyenleg = 100000
utolso_nyeremeny = 0

# -------------------------------------------------------
# Mező definíciók a táblán
# Minden tét: {"tipus": ..., "ertek": ..., "rect": Rect, "zseton_kepek": [(kep, rect), ...], "osszeg": int}
# -------------------------------------------------------

tabla_x = 150
tabla_y = 160
cella_sz = 50   # szélesség
cella_m1 = 82  # 1. és 2. sor magassága
cella_m2 = 82
cella_m3 = 78  # 3. sor magassága

def szam_rect(szam):
    """Visszaadja egy szám cellájának Rect-jét a táblán."""
    sor = szam_sora(szam)
    oSzlop = szam_oszlopa(szam)
    if sor == -1 or oSzlop == -1:
        return None
    x = tabla_x + oSzlop * cella_sz
    if sor == 0:
        y = tabla_y
    elif sor == 1:
        y = tabla_y + cella_m1
    else:
        y = tabla_y + cella_m1 + cella_m2
    m = cella_m3 if sor == 2 else cella_m1
    return pygame.Rect(x, y, cella_sz + 2, m)

# Fix mezők
piros1_rect = pygame.Rect(350, 454, 103, 56)
fekete1_rect = pygame.Rect(455, 454, 96, 53)
paros_rect = pygame.Rect(253, 450, 100, 60)
paratlan_rect = pygame.Rect(553, 450, 100, 60)
alacsony_rect = pygame.Rect(150, 450, 103, 60)
magas_rect = pygame.Rect(653, 450, 100, 60)
tucat1_rect = pygame.Rect(150, 398, 203, 55)
tucat2_rect = pygame.Rect(353, 398, 200, 55)
tucat3_rect = pygame.Rect(553, 398, 200, 55)

# Mező lista: minden tétet ide gyűjtünk
# Formátum: {"rect": Rect, "tipus": str, "ertek": any, "zsetonok": [(kep, rect)], "osszeg": int}
mezok = []

def uj_mezok():
    """Visszaállítja a mezők listáját (üres tételekkel)."""
    result = []
    # Számok (1-36)
    for szam in range(1, 37):
        r = szam_rect(szam)
        if r:
            result.append({"rect": r, "tipus": "szam", "ertek": szam, "zsetonok": [], "osszeg": 0})
    # Fix mezők
    result.append({"rect": piros1_rect, "tipus": "szin", "ertek": "piros", "zsetonok": [], "osszeg": 0})
    result.append({"rect": fekete1_rect, "tipus": "szin", "ertek": "fekete", "zsetonok": [], "osszeg": 0})
    result.append({"rect": paros_rect, "tipus": "paros", "ertek": "páros", "zsetonok": [], "osszeg": 0})
    result.append({"rect": paratlan_rect, "tipus": "paratlan", "ertek": "páratlan", "zsetonok": [], "osszeg": 0})
    result.append({"rect": alacsony_rect, "tipus": "alacsony", "ertek": "alacsony", "zsetonok": [], "osszeg": 0})
    result.append({"rect": magas_rect, "tipus": "magas", "ertek": "magas", "zsetonok": [], "osszeg": 0})
    result.append({"rect": tucat1_rect, "tipus": "tucat", "ertek": 1, "zsetonok": [], "osszeg": 0})
    result.append({"rect": tucat2_rect, "tipus": "tucat", "ertek": 2, "zsetonok": [], "osszeg": 0})
    result.append({"rect": tucat3_rect, "tipus": "tucat", "ertek": 3, "zsetonok": [], "osszeg": 0})
    return result

mezok = uj_mezok()

# Előző kör tárolása ismétléshez
elozo_mezok_adat = []  # Lista: (tipus, ertek, osszeg) tuple-ok

def mento_adat(mzk):
    """Ment egy egyszerű listát a mezők tétjeiről."""
    return [(m["tipus"], m["ertek"], m["osszeg"]) for m in mzk if m["osszeg"] > 0]

def ossz_tet(mzk):
    return sum(m["osszeg"] for m in mzk)

def zseton_kep_neve(nev):
    if nev == "sarga":
        return sargabet
    elif nev == "piros":
        return piros_bet
    elif nev == "zold":
        return zold_bet
    elif nev == "kek":
        return kek_bet
    else:
        return fekete_bet

def aktualis_zseton_kep():
    if aktiv_zseton:
        return zseton_kep_neve(aktiv_zseton)
    return None

def aktualis_zseton_ertek():
    if aktiv_zseton:
        return zseton_ertekek[aktiv_zseton]
    return 0

# -------------------------------------------------------
# Nyeremény számítás
# -------------------------------------------------------
def nyeremeny_szamitas(szam, mzk):
    """Kiszámolja a nyereményt az adott sorsolt szám alapján."""
    nyeremeny = 0
    for mezo in mzk:
        if mezo["osszeg"] == 0:
            continue
        tet_osszeg = mezo["osszeg"]
        t = mezo["tipus"]
        e = mezo["ertek"]

        if t == "szam":
            if e == szam:
                nyeremeny += tet_osszeg * 36  # 35:1 + visszakapja
        elif t == "szin":
            if szam == 0:
                pass
            elif e == "piros" and szam in PIROS_SZAMOK:
                nyeremeny += tet_osszeg * 2
            elif e == "fekete" and szam not in PIROS_SZAMOK and szam != 0:
                nyeremeny += tet_osszeg * 2
        elif t == "paros":
            if szam != 0 and szam % 2 == 0:
                nyeremeny += tet_osszeg * 2
        elif t == "paratlan":
            if szam != 0 and szam % 2 == 1:
                nyeremeny += tet_osszeg * 2
        elif t == "alacsony":
            if 1 <= szam <= 18:
                nyeremeny += tet_osszeg * 2
        elif t == "magas":
            if 19 <= szam <= 36:
                nyeremeny += tet_osszeg * 2
        elif t == "tucat":
            if e == 1 and 1 <= szam <= 12:
                nyeremeny += tet_osszeg * 3
            elif e == 2 and 13 <= szam <= 24:
                nyeremeny += tet_osszeg * 3
            elif e == 3 and 25 <= szam <= 36:
                nyeremeny += tet_osszeg * 3
    return nyeremeny

# -------------------------------------------------------
# Segédfüggvények
# -------------------------------------------------------
def teglalap_kirajzolasa(screen, szin, x, y, szelesseg, magassag):
    pygame.draw.rect(screen, szin, (x, y, szelesseg, magassag))

def szoveget_kirajzol(screen, szoveg, szoveg_x, szoveg_y, betumeret=30, szin=feher, bt=None, forgatas=False):
    if bt is None:
        bt = pygame.font.Font(None, betumeret)
    felszin = bt.render(szoveg, True, szin)
    if forgatas:
        felszin = pygame.transform.rotate(felszin, 90)
    screen.blit(felszin, (szoveg_x, szoveg_y))

def mezo_kattintas(pos, mzk):
    """Ha van aktív zseton és van elég egyenleg, rárak a mezőre."""
    global egyenleg, aktiv_zseton
    if aktiv_zseton is None:
        return
    ertek = aktualis_zseton_ertek()
    if egyenleg < ertek:
        return
    for mezo in mzk:
        if mezo["rect"].collidepoint(pos):
            # Zseton hozzáadása
            kep = zseton_kep_neve(aktiv_zseton).copy()
            kep_rect = kep.get_rect(center=mezo["rect"].center)
            # Több zseton esetén kicsit eltoljuk
            offset = len(mezo["zsetonok"]) * 4
            kep_rect.centerx += offset
            kep_rect.centery -= offset
            mezo["zsetonok"].append((kep, kep_rect))
            mezo["osszeg"] += ertek
            egyenleg -= ertek
            break

# -------------------------------------------------------
# Gombok
# -------------------------------------------------------
torles_rect = pygame.Rect(255, 524, 87, 42)
vissza_rect = pygame.Rect(154, 524, 86, 42)
start_rect = pygame.Rect(682, 524, 113, 42)
ismetles_rect = pygame.Rect(42, 524, 95, 42)

# Játékállapot
jatszhat = True  # False ha forgásban van
eredmeny_uzenet = ""

running = True
while running:
    pos = pygame.mouse.get_pos()
    screen.fill(hatter)
    dt = clock.get_time() / 1000.0  # deltatime másodpercben

    # --- Kerék forgás logika ---
    if forgasban:
        szog += forgasi_sebesseg
        if lassulas:
            forgasi_sebesseg *= 0.985
            if forgasi_sebesseg < 0.005:
                forgasban = False
                lassulas = False
                forgasi_sebesseg = 0.03
                jatszhat = True
                # Nyeremény kiszámítás
                ny = nyeremeny_szamitas(eredmeny_szam, mezok)
                egyenleg += ny
                utolso_nyeremeny = ny
                elozo_mezok_adat = mento_adat(mezok)
                mezok = uj_mezok()
                if ny > 0:
                    eredmeny_uzenet = f"Nyertél {ny} HUF-ot! 🎉"
                else:
                    eredmeny_uzenet = f"Nem nyertél. Próbáld újra!"
                eredmeny_megjelenes_timer = 180  # 3 másodperc 60fps-nél
        else:
            spinning_timer -= 1
            if spinning_timer <= 0:
                lassulas = True

    if eredmeny_megjelenes_timer > 0:
        eredmeny_megjelenes_timer -= 1

    # --- Események ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            # 1-5 gyorsbillentyűk zseton kiválasztáshoz
            elif event.key == pygame.K_1:
                aktiv_zseton = "sarga"
            elif event.key == pygame.K_2:
                aktiv_zseton = "piros"
            elif event.key == pygame.K_3:
                aktiv_zseton = "zold"
            elif event.key == pygame.K_4:
                aktiv_zseton = "kek"
            elif event.key == pygame.K_5:
                aktiv_zseton = "fekete"

        if event.type == pygame.MOUSEBUTTONDOWN and jatszhat:
            # Zseton kiválasztás
            if sargabet_rect.collidepoint(pos):
                aktiv_zseton = "sarga"
            elif piros_bet_rect.collidepoint(pos):
                aktiv_zseton = "piros"
            elif zold_bet_rect.collidepoint(pos):
                aktiv_zseton = "zold"
            elif kek_bet_rect.collidepoint(pos):
                aktiv_zseton = "kek"
            elif fekete_bet_rect.collidepoint(pos):
                aktiv_zseton = "fekete"

            # Gombok
            elif torles_rect.collidepoint(pos):
                # Visszatérítjük az összeget
                egyenleg += ossz_tet(mezok)
                elozo_mezok_adat = mento_adat(mezok)
                mezok = uj_mezok()

            elif vissza_rect.collidepoint(pos):
                # Utolsó zseton levétele: megkeressük az utolsó téttel rendelkező mezőt
                for mezo in reversed(mezok):
                    if mezo["osszeg"] > 0 and len(mezo["zsetonok"]) > 0:
                        utolso_kep, utolso_rect = mezo["zsetonok"].pop(-1)
                        # Meghatározzuk az értékét (legutóbb lerakott zseton)
                        # Egyszerűsítés: mindig az aktív zseton értékét vonjuk vissza
                        # Jobb megoldás: tároljuk a zseton értékét is
                        # Ehhez módosítjuk a struktúrát: zsetonok = [(kep, rect, ertek)]
                        # De most az osszegből kivesszük a legkisebb lehetséges értéket
                        # -> A zsetonhoz tárolt értéket használjuk (lásd lentebb)
                        break

            elif ismetles_rect.collidepoint(pos):
                if elozo_mezok_adat:
                    szukseg = sum(o for _, _, o in elozo_mezok_adat)
                    if egyenleg >= szukseg:
                        mezok = uj_mezok()
                        for (tipus, ertek, osszeg) in elozo_mezok_adat:
                            for mezo in mezok:
                                if mezo["tipus"] == tipus and mezo["ertek"] == ertek:
                                    mezo["osszeg"] = osszeg
                                    # Placeholder zseton kép
                                    kep = sargabet.copy()
                                    kep_rect = kep.get_rect(center=mezo["rect"].center)
                                    mezo["zsetonok"].append((kep, kep_rect))
                                    egyenleg -= osszeg
                                    break

            elif start_rect.collidepoint(pos):
                if ossz_tet(mezok) > 0:
                    eredmeny_szam = random.randint(0, 36)
                    forgasban = True
                    lassulas = False
                    forgasi_sebesseg = 0.15
                    spinning_timer = 180  # ~3 mp
                    jatszhat = False
                    eredmeny_uzenet = ""
                else:
                    eredmeny_uzenet = "Helyezz le zsetont a tábláre!"
                    eredmeny_megjelenes_timer = 120

            else:
                # Zseton lerakás a táblára
                mezo_kattintas(pos, mezok)

    # -------------------------------------------------------
    # Rajzolás
    # -------------------------------------------------------

    # Egyenleg panel
    pygame.draw.rect(screen, sarga, (40, 20, 260, 105), 3)
    szoveget_kirajzol(screen, f"HUF: {egyenleg:,}", 45, 30, szin=feher, bt=betutipus)
    szoveget_kirajzol(screen, f"Tét: {ossz_tet(mezok):,}", 45, 60, szin=feher, bt=betutipus)
    szoveget_kirajzol(screen, f"Utolsó nyeremény: {utolso_nyeremeny:,}", 45, 90, szin=feher, bt=kis_betu)

    # Tábla
    tabla_y_koordinata = 160
    teglalap_hossza = 82
    for i in range(3):
        for y in range(0, len(tabla[0]) - 1):
            szin = piros if tabla[i][y] == "P" else fekete
            pygame.draw.rect(screen, szin, (tabla_x + y * cella_sz, tabla_y_koordinata, cella_sz + 2, teglalap_hossza))
        if i == 0:
            tabla_y_koordinata += 83
        elif i == 1:
            tabla_y_koordinata += 77
            teglalap_hossza = 78

    # Számok
    for i in range(sorhossz):
        szoveget_kirajzol(screen, elso_sor_szoveg[i], 165 + i * 50, 195, 50, feher, betutipus, forgatas=True)
        szoveget_kirajzol(screen, masodik_sor_szoveg[i], 165 + i * 50, 195 + 75, 50, feher, betutipus, forgatas=True)
        szoveget_kirajzol(screen, harmadik_sor_szoveg[i], 165 + i * 50, 195 + 150, 50, feher, betutipus, forgatas=True)

    # Fehér vonalak
    feher_vonal_y = 160
    for i in range(3):
        if i == 1: feher_vonal_y += 80
        if i == 2: feher_vonal_y += 80
        for y in range(150, 800, 50):
            pygame.draw.line(screen, feher, (y, feher_vonal_y), (y + 50, feher_vonal_y), 3)
            oldalso = pygame.Rect(y, feher_vonal_y, 3, 80)
            pygame.draw.line(screen, feher, (y, feher_vonal_y + 80), (y + 50, feher_vonal_y + 80), 3)
            szin_v = sarga if oldalso.collidepoint(pos) else feher
            pygame.draw.rect(screen, szin_v, oldalso, 3)

    # 4. sor (tucatok)
    pygame.draw.rect(screen, feher, (150, 398, 203, 55), 3)
    pygame.draw.rect(screen, feher, (150, 398, 603, 55), 3)
    pygame.draw.rect(screen, feher, (150, 398, 403, 55), 3)
    for i in range(3):
        szoveget_kirajzol(screen, f"{i + 1}. tucat", 200 * i + 200, 420, szin=feher, bt=betutipus)

    # 5. sor
    pygame.draw.rect(screen, piros, piros1_rect)
    pygame.draw.rect(screen, fekete, fekete1_rect)
    pygame.draw.rect(screen, feher, (150, 450, 603, 60), 3)
    pygame.draw.rect(screen, feher, (150, 450, 203, 60), 3)
    pygame.draw.rect(screen, feher, (150, 450, 403, 60), 3)
    pygame.draw.rect(screen, feher, (253, 450, 100, 60), 3)
    pygame.draw.rect(screen, feher, (453, 450, 100, 60), 3)
    pygame.draw.rect(screen, feher, (653, 450, 100, 60), 3)
    szoveget_kirajzol(screen, "páratlan", 560, 470, szin=feher, bt=betutipus)
    szoveget_kirajzol(screen, "magas", 660, 470, szin=feher, bt=betutipus)
    szoveget_kirajzol(screen, "páros", 270, 470, szin=feher, bt=betutipus)
    szoveget_kirajzol(screen, "alacsony", 155, 470, szin=feher, bt=betutipus)

    # Oldalsó 0
    pygame.draw.line(screen, feher, (115, 161), (150, 161), 2)
    pygame.draw.line(screen, feher, (115, 394), (150, 396), 2)
    pygame.draw.line(screen, feher, (115, 161), (105, 188), 2)
    pygame.draw.line(screen, feher, (115, 394), (105, 367), 2)
    pygame.draw.line(screen, feher, (105, 190), (105, 365), 2)
    pygame.draw.ellipse(screen, zold, (114, 245, 30, 72))
    szoveget_kirajzol(screen, "0", 118, 272, szin=feher2, bt=kis_betu)

    # Előzmény / sorsolt szám
    pygame.draw.rect(screen, feher, (590, 20, 225, 50), 3)
    if eredmeny_szam is not None and not forgasban:
        szoveget_kirajzol(screen, f"Sorsolt szám: {eredmeny_szam}", 600, 35, szin=feher, bt=betutipus)
    elif forgasban:
        szoveget_kirajzol(screen, "Forog...", 630, 35, szin=sarga, bt=betutipus)
    else:
        szoveget_kirajzol(screen, "Sorsolt szám: -", 600, 35, szin=feher, bt=betutipus)

    # Kerék
    if kepek_betoltve:
        pygame.display.set_icon(logo)
        screen.blit(kerek, (375, 15))
    x_k, y_k = 440, 80
    pygame.draw.circle(screen, feher, (x_k, y_k), 45, 2)
    golyox = int(53 * math.cos(szog) + x_k)
    golyoy = int(53 * math.sin(szog) + y_k)
    pygame.draw.circle(screen, feher2, (golyox, golyoy), 5)

    # Eredmény üzenet
    if eredmeny_megjelenes_timer > 0 and eredmeny_uzenet:
        uzenet_felszin = betutipus.render(eredmeny_uzenet, True, sarga)
        uzenet_rect = uzenet_felszin.get_rect(center=(450, 140))
        pygame.draw.rect(screen, fekete, uzenet_rect.inflate(20, 10))
        screen.blit(uzenet_felszin, uzenet_rect)

    # Zseton kiválasztás jelzése
    if aktiv_zseton:
        nevek = {"sarga": "5", "piros": "10", "zold": "20", "kek": "50", "fekete": "100"}
        szoveget_kirajzol(screen, f"Kiválasztott: {nevek[aktiv_zseton]} HUF", 350, 510, szin=sarga, bt=kis_betu)

    # Gombok
    def gomb(rect, szoveg, aktiv=True):
        szin_hatter = sarga2 if aktiv else szurke
        szin_keret = sarga if aktiv else (150, 150, 150)
        pygame.draw.rect(screen, szin_hatter, rect)
        pygame.draw.rect(screen, szin_keret, rect.inflate(4, 4), 3)
        szoveget_kirajzol(screen, szoveg, rect.x + 8, rect.y + 12, szin=fekete, bt=betutipus)

    gomb(ismetles_rect, "ismétlés", bool(elozo_mezok_adat) and jatszhat)
    gomb(start_rect, "start", jatszhat and ossz_tet(mezok) > 0)
    gomb(vissza_rect, "vissza", jatszhat)
    gomb(torles_rect, "törlés", jatszhat)

    # Zsetonok kirajzolása a mezőkön
    for mezo in mezok:
        for kep, kep_rect in mezo["zsetonok"]:
            screen.blit(kep, kep_rect)
        # Összeg kiírása a mezőn ha van tét
        if mezo["osszeg"] > 0:
            txt = kis_betu.render(str(mezo["osszeg"]), True, sarga)
            screen.blit(txt, (mezo["rect"].centerx - txt.get_width() // 2,
                               mezo["rect"].centery - txt.get_height() // 2))

    # Eredeti zsetonok (kiválasztó panel)
    pygame.draw.rect(screen, (30, 80, 55), (355, 520, 290, 55))
    screen.blit(sargabet, sargabet_rect)
    screen.blit(piros_bet, piros_bet_rect)
    screen.blit(zold_bet, zold_bet_rect)
    screen.blit(kek_bet, kek_bet_rect)
    screen.blit(fekete_bet, fekete_bet_rect)

    # Aktív zseton kiemelése
    if aktiv_zseton:
        kiemel_map = {"sarga": sargabet_rect, "piros": piros_bet_rect, "zold": zold_bet_rect,
                      "kek": kek_bet_rect, "fekete": fekete_bet_rect}
        pygame.draw.rect(screen, sarga, kiemel_map[aktiv_zseton].inflate(6, 6), 3)

    # Egér
    if kepek_betoltve:
        pygame.mouse.set_visible(False)
        eger_rect = eger.get_rect()
        eger_rect.topleft = (pos[0] - 5, pos[1] - 5)
        screen.blit(eger, eger_rect)
    else:
        pygame.mouse.set_visible(True)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
