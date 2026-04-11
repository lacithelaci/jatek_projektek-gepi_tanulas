import pygame

# Created by: Szemán László
# Refactored: osztályok, fizikai ugrás, tisztább fegyverlogika

pygame.init()
pygame.display.set_caption("Úristen very big project *javított* beta 0.9.0")

# ── Képernyő ──────────────────────────────────────────────────────────────────
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock  = pygame.time.Clock()

# ── Színek ────────────────────────────────────────────────────────────────────
BLUE       = (0,   0,   255)
BLACK      = (0,   0,   0)
RED        = (255, 0,   0)
GREEN      = (124, 252, 0)
WHITE      = (255, 255, 255)
BROWN      = (139, 69,  19)
GRAY       = (200, 200, 200)
PINK       = (100, 72,  77)
DARK_GREEN = (0,   128, 0)

GRAVITY     = 0.5
JUMP_SPEED  = -16
GROUND_Y    = 500   # ahol a játékos áll a talajon

# ── Platform ──────────────────────────────────────────────────────────────────
PLATFORM = pygame.Rect(200, 350, 400, 40)

# ── Fontok ────────────────────────────────────────────────────────────────────
basic_font = pygame.font.SysFont('Times New Roman', 22)
large_font = pygame.font.SysFont('Times New Roman', 50)
huge_font  = pygame.font.SysFont('Times New Roman', 100)

# ── Hangok ────────────────────────────────────────────────────────────────────
shot_sound    = pygame.mixer.Sound("hangok/gun.mp3")
shot_sound2   = pygame.mixer.Sound("hangok/gun2.mp3")
axe_hit_sound = pygame.mixer.Sound("hangok/fejsze.mp3")
rasengan_sound= pygame.mixer.Sound("hangok/rasengan.mp3")
fireball_sound= pygame.mixer.Sound("hangok/fireball.mp3")
pygame.mixer.music.load('hangok/hatter_muzsika.mp3')
pygame.mixer.music.play(-1)

# ── Képek ─────────────────────────────────────────────────────────────────────
player1_img  = pygame.image.load('kepek/kep1.png')
player2_img  = pygame.image.load('kepek/kep2.jpg')
bullet1_img  = pygame.image.load("kepek/bullet.jpg")
bullet2_img  = pygame.image.load("kepek/bullet2.jpg")
axe1_img     = pygame.image.load("kepek/balta.jpg")
axe2_img     = pygame.image.load("kepek/balta2.jpg")
rasengan_img = pygame.image.load("kepek/rasengan.png")
fireball_img = pygame.image.load("kepek/fireball.png")
pygame.display.set_icon(player1_img)


# ══════════════════════════════════════════════════════════════════════════════
#  Segéd: téglalap ütközésvizsgálat
# ══════════════════════════════════════════════════════════════════════════════
def rects_collide(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


# ══════════════════════════════════════════════════════════════════════════════
#  Lövedék osztály (golyó / rasengan / tűzgömb)
# ══════════════════════════════════════════════════════════════════════════════
class Projectile:
    """Vízszintesen mozgó lövedék."""

    def __init__(self, img, damage, speed, reset_x, reset_y, w=30, h=30):
        self.img     = img
        self.damage  = damage
        self.speed   = speed      # pozitív = jobbra, negatív = balra
        self.reset_x = reset_x
        self.reset_y = reset_y
        self.w       = w
        self.h       = h
        self.x       = reset_x
        self.y       = reset_y
        self.active  = False      # mozog-e éppen

    def fire(self, start_x, start_y, direction):
        """Kilő a megadott pozícióból, adott irányba."""
        if self.active:
            return   # már repül, nem lőhet újat
        self.x      = start_x
        self.y      = start_y
        self.speed  = abs(self.speed) * (1 if direction > 0 else -1)
        self.active = True

    def update(self):
        if self.active:
            self.x += self.speed
            # Képernyőn kívülre ért → visszaállít
            if self.x > SCREEN_WIDTH or self.x < 0:
                self.reset()

    def check_hit(self, target):
        """Megvizsgálja, hogy eltalálta-e a célt. Ha igen, visszaállít és visszaadja a sebzést."""
        if not self.active:
            return 0
        if rects_collide(self.x, self.y, self.w, self.h,
                         target.x, target.y, target.w, target.h):
            self.reset()
            return self.damage
        return 0

    def reset(self):
        self.x      = self.reset_x
        self.y      = self.reset_y
        self.active = False

    def draw(self, surface):
        if self.active:
            surface.blit(self.img, (self.x, self.y))


# ══════════════════════════════════════════════════════════════════════════════
#  Fejsze osztály (parabolikus röppálya)
# ══════════════════════════════════════════════════════════════════════════════
class Axe:
    """Parabolikus pályán mozgó fejsze."""

    def __init__(self, img, damage, reset_x, reset_y, w=30, h=30):
        self.img     = img
        self.damage  = damage
        self.reset_x = reset_x
        self.reset_y = reset_y
        self.w       = w
        self.h       = h
        self.x       = reset_x
        self.y       = reset_y
        self.vx      = 0
        self.vy      = 0
        self.active  = False

    def throw(self, start_x, start_y, direction):
        if self.active:
            return
        self.x      = start_x
        self.y      = start_y
        self.vx     = 12 * (1 if direction > 0 else -1)
        self.vy     = -8          # felfelé indulva szép ívet ír le
        self.active = True

    def update(self):
        if not self.active:
            return
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.4            # gravitáció a fejszére
        if self.x > SCREEN_WIDTH or self.x < 0 or self.y > SCREEN_HEIGHT or self.y < 0:
            self.reset()

    def check_hit(self, target):
        if not self.active:
            return 0
        if rects_collide(self.x, self.y, self.w, self.h,
                         target.x, target.y, target.w, target.h):
            self.reset()
            pygame.mixer.Sound.play(axe_hit_sound)
            return self.damage
        return 0

    def reset(self):
        self.x      = self.reset_x
        self.y      = self.reset_y
        self.active = False

    def draw(self, surface):
        if self.active:
            surface.blit(self.img, (self.x, self.y))# ══════════════════════════════════════════════════════════════════════════════
#  Játékos osztály
# ══════════════════════════════════════════════════════════════════════════════
class Player:
    PLAYER_W = 40
    PLAYER_H = 40

    def __init__(self, name, img, start_x, start_y, color,
                 bullet, axe, special,
                 bullet_key, axe_key, special_key,
                 left_key, right_key, jump_key,
                 health_bar_x):
        self.name         = name
        self.img          = img
        self.x            = start_x
        self.y            = float(start_y)
        self.color        = color
        self.w            = self.PLAYER_W
        self.h            = self.PLAYER_H

        # Mozgás
        self.vx           = 0
        self.vy           = 0.0
        self.on_ground    = False
        self.facing       = 1   # 1 = jobbra, -1 = balra

        # Fegyverek
        self.bullet       = bullet
        self.axe          = axe
        self.special      = special
        self.bullet_ready = True   # True = lehet lőni

        # Billentyűk
        self.left_key     = left_key
        self.right_key    = right_key
        self.jump_key     = jump_key
        self.bullet_key   = bullet_key
        self.axe_key      = axe_key
        self.special_key  = special_key

        # Statisztika
        self.health       = 250
        self.hits_given   = 0   # mennyiszer talált (speciál feltétel)
        self.health_bar_x = health_bar_x

        # Speciál hang
        self.special_sound = None

    # ── Esemény kezelés ───────────────────────────────────────────────────────
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.left_key:
                self.vx = -5
                self.facing = -1
            if event.key == self.right_key:
                self.vx = 5
                self.facing = 1
            if event.key == self.jump_key and self.on_ground:
                self.vy = JUMP_SPEED
                self.on_ground = False

            # Lövés: egy gombnyomásra egy lövedék
            if event.key == self.bullet_key and self.bullet_ready and not self.bullet.active:
                self.bullet.fire(
                    self.x + (self.w if self.facing > 0 else -self.bullet.w),
                    self.y + self.h // 2 - self.bullet.h // 2,
                    self.facing
                )
                self.bullet_ready = False
                pygame.mixer.Sound.play(shot_sound if self.color == GREEN else shot_sound2)

            # Fejsze dobás
            if event.key == self.axe_key and not self.axe.active:
                self.axe.throw(self.x, self.y - self.axe.h, self.facing)

            # Speciál (csak 3+ találat után)
            if event.key == self.special_key and self.hits_given >= 3 and not self.special.active:
                self.special.fire(
                    self.x + (self.w if self.facing > 0 else -self.special.w),
                    self.y + self.h // 2 - self.special.h // 2,
                    self.facing
                )
                if self.special_sound:
                    pygame.mixer.Sound.play(self.special_sound)

        if event.type == pygame.KEYUP:
            if event.key == self.left_key and self.vx < 0:
                self.vx = 0
            if event.key == self.right_key and self.vx > 0:
                self.vx = 0
            # Lövés újratöltése key up-ra
            if event.key == self.bullet_key:
                self.bullet_ready = True

    # ── Frissítés ─────────────────────────────────────────────────────────────
    def update(self):
        # Vízszintes mozgás
        self.x += self.vx
        self.x = max(0, min(SCREEN_WIDTH - self.w, self.x))

        # Gravitáció
        self.vy += GRAVITY
        self.y  += self.vy

        # Talaj
        if self.y >= GROUND_Y:
            self.y        = GROUND_Y
            self.vy       = 0
            self.on_ground= True

        # Platform ütközés
        foot_y = self.y + self.h
        head_y = self.y

        # Fentről leesés → megáll a platformon
        if self.vy >= 0:
            if (self.x + self.w > PLATFORM.left and
                    self.x < PLATFORM.right and
                    PLATFORM.top <= foot_y <= PLATFORM.top + self.vy + 2):
                self.y        = PLATFORM.top - self.h
                self.vy       = 0
                self.on_ground= True

        # Alulról ugrik → fejjel bever, visszapattan
        if self.vy < 0:
            if (self.x + self.w > PLATFORM.left and
                    self.x < PLATFORM.right and
                    PLATFORM.bottom >= head_y >= PLATFORM.bottom + self.vy - 2):
                self.y  = PLATFORM.bottom
                self.vy = 0   # megállítja a felfelé mozgást

        # Fejlövedékek frissítése
        self.bullet.update()
        self.axe.update()
        self.special.update()

    def receive_damage(self, amount):
        self.health = max(0, self.health - amount)

    def register_hit(self):
        """Hívd meg, ha ez a játékos eltalált valakit."""
        self.hits_given += 1

    # ── Rajzolás ──────────────────────────────────────────────────────────────
    def draw(self, surface):
        surface.blit(self.img, (int(self.x), int(self.y)))
        self.bullet.draw(surface)
        self.axe.draw(surface)
        self.special.draw(surface)

    def draw_hud(self, surface):
        # Életerő sáv (max 250px széles, rögzített pozíción)
        pygame.draw.rect(surface, RED, (self.health_bar_x, 20, self.health, 20))
        hp_text   = basic_font.render(f'HP:{self.health}', False, RED)
        name_text = basic_font.render(f'Név: {self.name}', False, self.color)
        # Rögzített x pozíció, nem függ az életerő szélességétől
        surface.blit(name_text, (self.health_bar_x,       55))
        surface.blit(hp_text,   (self.health_bar_x + 150, 55))


# ══════════════════════════════════════════════════════════════════════════════
#  Játékosok létrehozása
# ══════════════════════════════════════════════════════════════════════════════

# Játékos 1 fegyverei
p1_bullet  = Projectile(bullet1_img,  damage=10, speed=12, reset_x=135, reset_y=110)
p1_axe     = Axe(axe1_img,            damage=10, reset_x=200, reset_y=100)
p1_special = Projectile(rasengan_img, damage=50, speed=15, reset_x=250, reset_y=100, w=40, h=40)

# Játékos 2 fegyverei
p2_bullet  = Projectile(bullet2_img,  damage=10, speed=-12, reset_x=600, reset_y=110)
p2_axe     = Axe(axe2_img,            damage=10, reset_x=650, reset_y=100)
p2_special = Projectile(fireball_img, damage=50, speed=-15, reset_x=700, reset_y=100, w=40, h=40)

player1 = Player(
    name="Laci", img=player1_img,
    start_x=0,   start_y=GROUND_Y,
    color=GREEN,
    bullet=p1_bullet, axe=p1_axe, special=p1_special,
    bullet_key=pygame.K_1, axe_key=pygame.K_2, special_key=pygame.K_3,
    left_key=pygame.K_a, right_key=pygame.K_d, jump_key=pygame.K_w,
    health_bar_x=40
)
player1.special_sound = rasengan_sound

player2 = Player(
    name="Patrik", img=player2_img,
    start_x=760, start_y=GROUND_Y,
    color=BLUE,
    bullet=p2_bullet, axe=p2_axe, special=p2_special,
    bullet_key=pygame.K_i, axe_key=pygame.K_o, special_key=pygame.K_p,
    left_key=pygame.K_LEFT, right_key=pygame.K_RIGHT, jump_key=pygame.K_UP,
    health_bar_x=500
)
player2.special_sound = fireball_sound


# ══════════════════════════════════════════════════════════════════════════════
#  Fő játékhurok
# ══════════════════════════════════════════════════════════════════════════════
start_ticks = pygame.time.get_ticks()
winner_text = ""
fight_text  = "FIGHT"
game_over   = False
running     = True

while running:
    # ── Események ─────────────────────────────────────────────────────────────
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        if not game_over:
            player1.handle_event(event)
            player2.handle_event(event)

    # ── Logika ────────────────────────────────────────────────────────────────
    if not game_over:
        player1.update()
        player2.update()

        # Sebzés: p1 fegyverek → p2
        for proj in (player1.bullet, player1.axe, player1.special):
            dmg = proj.check_hit(player2)
            if dmg:
                player2.receive_damage(dmg)
                player1.register_hit()

        # Sebzés: p2 fegyverek → p1
        for proj in (player2.bullet, player2.axe, player2.special):
            dmg = proj.check_hit(player1)
            if dmg:
                player1.receive_damage(dmg)
                player2.register_hit()

        # Idő
        seconds   = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, 180 - seconds)

        # Sebzésnövelés 60 mp alatt
        if time_left <= 60:
            player1.bullet.damage = 20
            player1.axe.damage    = 20
            player2.bullet.damage = 20
            player2.axe.damage    = 20

        # Gyenge játékos kapjon több sebzést (izgalmas comeback)
        if player2.health <= 120:
            player1.axe.damage = 30
        if player1.health <= 120:
            player2.bullet.damage = 30

        # Győztes meghatározása
        if player1.health == 0:
            winner_text = "A győztes a játékos 2"
            game_over = True
        elif player2.health == 0:
            winner_text = "A győztes a játékos 1"
            game_over = True
        elif time_left == 0:
            winner_text = "Döntetlen"
            game_over = True

    # ── Rajzolás ──────────────────────────────────────────────────────────────
    screen.fill(WHITE)

    # Háttér
    pygame.draw.rect(screen, BROWN,      (0, 540, 800, 60))
    pygame.draw.rect(screen, DARK_GREEN, (0, 540, 800, 30))

    # Platform
    pygame.draw.rect(screen, BROWN,      PLATFORM)
    pygame.draw.rect(screen, DARK_GREEN, (PLATFORM.x, PLATFORM.y, PLATFORM.width, 20))

    # Játékosok
    player1.draw(screen)
    player2.draw(screen)

    # HUD
    player1.draw_hud(screen)
    player2.draw_hud(screen)

    # Időzítő kör
    pygame.draw.circle(screen, PINK, (385, 40), 30)
    timer_text = basic_font.render(f'{time_left}', False, GRAY)
    screen.blit(timer_text, (370, 25))

    # FIGHT felirat (3 mp-ig)
    if time_left > 177:
        fight_display = large_font.render(fight_text, False, RED)
        screen.blit(fight_display, (270, 250))

    # Győztes felirat
    if winner_text:
        win_display = large_font.render(winner_text, False, RED)
        screen.blit(win_display, (200, 250))

    # Speciál töltöttség jelző
    s1 = basic_font.render(f'Speciál: {"KÉSZ" if player1.hits_given >= 3 else player1.hits_given}/3', False, GREEN)
    s2 = basic_font.render(f'Speciál: {"KÉSZ" if player2.hits_given >= 3 else player2.hits_given}/3', False, BLUE)
    screen.blit(s1, (40,  100))
    screen.blit(s2, (500, 100))

    pygame.display.flip()
    clock.tick(60)

    # Kilépés győztes után
    if game_over and winner_text:
        pygame.time.wait(2000)
        running = False

pygame.quit()
