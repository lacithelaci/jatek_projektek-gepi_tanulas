import pygame
#készítette: Szemán László

pygame.display.set_caption("Úristen very big project *javított* beta 0.8.5")
pygame.init()
#ablak mérete
size = (800, 600)
#színek
kek = (0,0,255)
fekete = (0,0,0)
piros = (255,0,0)
zold=(124,252,0)
feher=(255,255,255)
barna=(139,69,19)
szurke = (200, 200, 200)
pink=(100,72,77)
szold=(0,128,0)
#játékos elhelyezkedése
player1_x = 0
player1_y = 500
player2_x = 760
player2_y = 500
#platform adatok
platformx = 200
platformy = 350
#hp adatok
eletero1 = 250
eletero2 = 250
#mozgás
udx = 0
udy = 0
udx2 = 0
udy2 = 0
#lövedék iránya és adataik
szam1=135
szam2=110
szam3=600
szam4=110
irany = 12
irany2 = -12
lovedekx = szam1
lovedeky = szam2
lovedekx2 = szam3
lovedeky2 = szam4
baltax=200
baltay=100
balta2x=650
balta2y=100
biranyx= 12
biranyy= 4
biranyx2= -12
biranyy2= 4
dmg=10
dmg2=10
rasenganx=250
rasengany=100
rirany=15
hit=0
hit2=0
fireballx=700
firebally=100
firany=15
ending=0
#fontos dolgok értelmetlen nevekkel
semmi=0
semmi2=0
semmi3=0

semmi4=0
semmi5=0
semmi6=0

bsemmi=1
bsemmi2=1
bsemmi3=1
bsemmi3_1=1

bsemmi4=1
bsemmi5=1
bsemmi6=1


rsemmi=0
rsemmi2=0
rsemmi3=0


fsemmi=0
fsemmi2=0
fsemmi3=0
#betűméret + szöveg
basic_font = pygame.font.SysFont('Times New Roman', 22)
basic_font2 = pygame.font.SysFont('Times New Roman', 50)
basic_font2 = pygame.font.SysFont('Times New Roman', 100)

name1 = "Laci"
name2 = "Patrik"
halal=False
dontetlen="Döntetlen"
gyoztes=""
harc="FIGHT"
#kiírás
ablak = pygame.display.set_mode(size)
start_ticks = pygame.time.get_ticks()
#muzsika lejátszó
shot_sound=pygame.mixer.Sound("gun.mp3")
shot_sound2=pygame.mixer.Sound("gun2.mp3")
pygame.mixer.music.load('hatter_muzsika.mp3')
fejsze_talalat=pygame.mixer.Sound("fejsze.mp3")
rasengan_sound=pygame.mixer.Sound("rasengan.mp3")
fireball_sound=pygame.mixer.Sound("fireball.mp3")
pygame.mixer.music.play(-1)
#képek
p1=pygame.image.load('kep1.png')
p2=pygame.image.load('kep2.jpg')
bullet=pygame.image.load("bullet.jpg")
bullet2=pygame.image.load("bullet2.jpg")
balta=pygame.image.load("balta.jpg")
balta2=pygame.image.load("balta2.jpg")
rasengan=pygame.image.load("rasengan.png")
fireball=pygame.image.load("fireball.png")
pygame.display.set_icon(p1)
pygame.display.set_icon(p2)
#hatter=pygame.image.load('kep.jfif')

clock = pygame.time.Clock()
vege = False

while not vege:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vege = True
            # gyors kilépés
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                vege=True
        #mozgások tiltásokkal
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                udx = - 5
                if semmi3 == 0:
                    irany = - 12
                if bsemmi3==1:
                    biranyx=-12
                if rsemmi3==0:
                    rirany=-15
            if event.key == pygame.K_d:
                udx = 5
                if semmi3 == 0:
                    irany = 12
                if bsemmi3==1:
                    biranyx = 12
                if rsemmi3==0:
                    rirany=15
            if event.key == pygame.K_LEFT:
                udx2 = - 5
                if semmi6 == 0:
                    irany2 = - 12
                if fsemmi3==0:
                    firany= -15
            if event.key == pygame.K_RIGHT:
                udx2 = 5
                if semmi6 == 0:
                    irany2 = 12
                if fsemmi3==0:
                    firany= 15
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                udx = 0
            if event.key == pygame.K_d:
                udx = 0
            if event.key == pygame.K_LEFT:
                udx2 = 0
            if event.key == pygame.K_RIGHT:
                udx2 = 0
        if semmi2==0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    lovedekx= player1_x+40
                    lovedeky= player1_y+20
                    semmi3=1



            if event.type == pygame.KEYUP:
                if event.key == pygame.K_1:

                    semmi=1
                    semmi2=1
                    pygame.mixer.Sound.play(shot_sound)
                    #pygame.mixer.music.stop()
        if semmi5 == 0:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    lovedekx2= player2_x-20
                    lovedeky2= player2_y+20
                    semmi6 = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_i:
                    semmi4 = 1
                    semmi5 = 1
                    pygame.mixer.Sound.play(shot_sound2)
                    #pygame.mixer.music.stop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                udy = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                udy = 5
                bsemmi3_1=1
                if bsemmi3_1==1:
                    biranyy=4

        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        udy2 = -5

        if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        udy2 = 5

                    pygame.event.clear()
        if bsemmi2==1:
            if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_2:
                            baltax=player1_x+20
                            baltay=player1_y-40
                            bsemmi3 = 0
            if event.type == pygame.KEYUP:
                        if event.key == pygame.K_2:
                            bsemmi=0
                            bsemmi2 = 0

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                bsemmi3_1=0
                if bsemmi3_1==0:
                    biranyy=-4
        if bsemmi5 == 1:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    balta2x = player2_x - 20
                    balta2y = player2_y - 40
                    bsemmi6 = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_o:
                        bsemmi4=0
                        bsemmi5=0


        if hit>=3:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    rasenganx = player1_x + 20
                    rasengany = player1_y
                    rsemmi3 = 1
                    pygame.mixer.Sound.play(rasengan_sound)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_3:
                    rsemmi=1
                    rsemmi2=1
        if hit2 >= 3:
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        fireballx = player2_x - 20
                        firebally = player2_y
                        fsemmi3 = 1
                        pygame.mixer.Sound.play(fireball_sound)

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_p:
                        fsemmi = 1
                        fsemmi2 = 1


    #mozgás

    player1_x += udx
    player1_y += udy
    player2_x += udx2
    player2_y += udy2
    #lövedék iránya gyakorlatban
    if semmi==1:
        lovedekx += irany
    if semmi4==1:
        lovedekx2 += irany2
    if bsemmi==0:
        baltax+=biranyx
        baltay+=biranyy
    if bsemmi4==0:
        balta2x+=biranyx2
        balta2y+=biranyy2
    if rsemmi==1:
        rasenganx += rirany
        hit=0


    if fsemmi==1:
        fireballx += firany
        hit2=0




    ablak.fill(feher)
    #tilás
    if player1_y > 500:
        player1_y = 500
    if player1_y < 130:
        player1_y = 130
    if player1_x < 0:
        player1_x = 0
    if player1_x > 760:
        player1_x = 760

    if player2_y > 500:
        player2_y = 500
    if player2_y < 130:
        player2_y = 130
    if player2_x < 0:
        player2_x = 0
    if player2_x > 760:
        player2_x = 760

    #háttér
    # ablak.blit(hatter,(0,0))
    #rajz
    pygame.draw.rect(ablak, barna, (0,540, 800, 60))
    pygame.draw.rect(ablak, szold, (0, 540, 800, 30))
    #pygame.draw.rect(ablak,zold,(player1_x,player1_y,40,40))
    ablak.blit(p1, (player1_x, player1_y))
    #pygame.draw.rect(ablak, kek, (player2_x, player2_y, 40, 40))
    ablak.blit(p2, (player2_x, player2_y))
    pygame.draw.rect(ablak,barna,(platformx,platformy,400,40))
    pygame.draw.rect(ablak, szold, (200, 350, 400, 20))
    pygame.draw.rect(ablak, piros, (40, 20, eletero1, 20))
    pygame.draw.rect(ablak, piros, (500, 20, eletero2, 20))
    pygame.draw.circle(ablak, pink, (385, 40), 30)
    #töltény rajz
    #pygame.draw.rect(ablak, barna, (lovedekx, lovedeky, 10,5))
    ablak.blit(bullet, (lovedekx, lovedeky))

    #pygame.draw.rect(ablak, barna, (lovedekx2, lovedeky2, 10,5))
    ablak.blit(bullet2, (lovedekx2, lovedeky2))
    #képesség2
    ablak.blit(balta,(baltax,baltay))
    ablak.blit(balta2,(balta2x,balta2y))
    #képesség 3
    ablak.blit(rasengan, (rasenganx, rasengany))
    ablak.blit(fireball,(fireballx,firebally))
    #hitbox és töltény reset
    if lovedekx in range(player2_x, player2_x+40) and lovedeky in range(player2_y,player2_y+40):
        eletero2 -= dmg
        lovedekx = szam1
        lovedeky = szam2
        semmi=0
        semmi2=0
        semmi3 = 0
        hit+=1
    if lovedekx>800 or lovedekx<0:
        lovedekx = szam1
        lovedeky = szam2
        semmi = 0
        semmi2 = 0
        semmi3 = 0
    if lovedekx2 in range(player1_x, player1_x+40) and lovedeky2 in range(player1_y,player1_y+40):
        eletero1 -= dmg2
        lovedekx2 = szam3
        lovedeky2 = szam4
        semmi4 = 0
        semmi5 = 0
        semmi6 = 0
        hit2+=1
    if lovedekx2 > 800 or lovedekx2 < 0:
        lovedekx2 = szam3
        lovedeky2 = szam4
        semmi4 = 0
        semmi5 = 0
        semmi6 = 0
    if baltax > 800 or baltax< 0 or baltay<0 or baltay>600:
            baltax=200
            baltay=100
            bsemmi=1
            bsemmi2=1
            bsemmi3=1
    if baltax in range(player2_x-40, player2_x + 40) and baltay in range(player2_y-40, player2_y + 40):
            baltax = 200
            baltay = 100
            bsemmi = 1
            bsemmi2= 1
            bsemmi3 = 1
            eletero2-=dmg
            hit+=1
            pygame.mixer.Sound.play(fejsze_talalat)
    if balta2x > 800 or balta2x< 0 or balta2y<0 or balta2y>600:
            balta2x=650
            balta2y=100
            bsemmi4 = 1
            bsemmi5 = 1
            bsemmi6 = 1
    if balta2x in range(player1_x-40, player1_x + 40) and balta2y in range(player1_y-40, player1_y + 40):
            balta2x = 650
            balta2y = 100
            eletero1 -= dmg2
            bsemmi4 = 1
            bsemmi5 = 1
            bsemmi6 = 1
            hit2+=1
            pygame.mixer.Sound.play(fejsze_talalat)
    if rasenganx in range(player2_x, player2_x+40) and rasengany in range(player2_y,player2_y+40):
        eletero2 -= 50
        rasenganx = 250
        rasengany = 100
        rsemmi=0
        rsemmi2=0
        rsemmi3 = 0
    if rasenganx>800 or rasenganx<0:
        rasenganx = 250
        rasengany = 100
        rsemmi = 0
        rsemmi2 = 0
        rsemmi3 = 0



    if fireballx in range(player1_x, player1_x+40) and firebally in range(player1_y,player1_y+40):
        eletero1 -= 50
        fireballx = 700
        firebally = 100
        fsemmi=0
        fsemmi2=0
        fsemmi3 = 0
    if fireballx>800 or fireballx<0:
        fireballx = 700
        firebally = 100
        fsemmi = 0
        fsemmi2 = 0
        fsemmi3 = 0

    if player1_y == 360 and player1_x in range(platformx - 40,platformx + 400):
        player1_y = 400

    if player1_y == 310 and player1_x in range(platformx - 40,platformx + 400):
        player1_y = 305


    if player2_y == 360 and player2_x in range(platformx - 40,platformx + 400):
        player2_y = 400

    if player2_y == 310 and player2_x in range(platformx - 40,platformx + 400):
        player2_y=305
    #idő
    seconds = (pygame.time.get_ticks() - start_ticks) //1000
    ido=180-seconds


    #hp !<0
    if eletero1<0:
        eletero1=0
    if eletero2<0:
        eletero2=0

    #kiírások
    jatekos_szoveg = basic_font.render(f'HP:{eletero1}', False, piros)
    ablak.blit(jatekos_szoveg, (180, 60))
    jatekos_szoveg = basic_font.render(f'HP:{eletero2}', False, piros)
    ablak.blit(jatekos_szoveg, (660, 60))
    jatekos_szoveg = basic_font.render(f'Név: {name1}', False, zold)
    ablak.blit(jatekos_szoveg, (40, 60))
    jatekos_szoveg = basic_font.render(f'Név: {name2}', False, kek)
    ablak.blit(jatekos_szoveg, (500, 60))
    jatekos_szoveg = basic_font.render(f'{ido}', False, szurke)
    ablak.blit(jatekos_szoveg, (370, 25))
    jatekos_szoveg = basic_font.render(f'{"p1 bullet: "}', False, szurke)
    ablak.blit(jatekos_szoveg, (40, 100))
    jatekos_szoveg = basic_font.render(f'{"p2 bullet: "}', False, szurke)
    ablak.blit(jatekos_szoveg, (500, 100))
    jatekos_szoveg2 = basic_font2.render(f'{harc}', False, piros)
    ablak.blit(jatekos_szoveg2, (270, 250))


    if ido<=177:
        harc=""
    jatekos_szoveg3 = basic_font2.render(f'{gyoztes}', False, piros)
    ablak.blit(jatekos_szoveg3, (270, 250))
    if eletero1==0:
        gyoztes="A győztes a játékos 2"
        print(gyoztes)
        ending=100

    if eletero2 == 0:
        gyoztes = "A győztes a játékos 1"
        print(gyoztes)
        ending=100
    if ido==0:
        gyoztes="Döntetlen"
        print(gyoztes)
        ending=100

    if ending==100:
        pygame.time.wait(2000)
        vege = True

    #vég

    #sebzés növelés

    if ido==60:
        dmg=20
        dmg2=20
    if eletero2 in range(0,120+1):
        dmg2=30
    if eletero1 in range(0, 120 + 1):
        dmg = 30

    pygame.display.flip()
    clock.tick(60)


    """
    Megjegyzések:
    Irányítás: 
    p1: mozgás: a,d,w
    lövés:s
    p2: nyilak:
    lövés: lefelenyíl
    
    
    bugfix/update:
    -Attila által észrevett "repülés" kivétele a platformon 
    -A végén a játék győztest hírdet
    -Kifizettem a grafikust,így már kicsivel szebben vannak elhelyezve a tárgyak
    -játéktér növelése
    -intelligens hp/dmg arány kiosztása a fair játékélményért
    -lövéshang
    -háttérzene
    -négyzetek helyett igazi karaktere
    -1 töltény helyett 3 lehet majd kilőni
    
    irányítás: 
    p1: 
    mozgás:wasd
    lövés:1,2
    speciális lövés: 3 találatnál:3
    balta fel/le irányítása:w,s
    p2: 
    mozgás:nyilak
    lövés:i,o
    speciális lövés: 3 találatnál:p
    balta fel/le irányítása:lenyíl,felnyíl
    

    """