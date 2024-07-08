import pygame
import math

# hang
pygame.mixer.init()
jump_sound = pygame.mixer.Sound('hangok/jump.mp3')


# feliratok
def win_or_lose(screen_width, screen_height, screen, szin, uzenet):
    # Játék vége, üzenet megjelenítése
    font = pygame.font.Font(None, 170)
    text = font.render(f"{uzenet}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.fill(szin)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)


def hp(screen, lives, hp_poz=(50, 65)):
    font = pygame.font.Font(None, 20)
    text = font.render(f"{lives}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = hp_poz
    screen.blit(text, text_rect)


# fps megjelenítés
def display_fps(screen, clock, font, color=(255, 255, 255), pos=(695, 5)):
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, color)
    screen.blit(fps_text, pos)


class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = False

    def move(self, keys, screen_width):

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
            jump_sound.play()
            self.on_ground = False
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - self.rect.width:
            self.rect.x = screen_width - self.rect.width

    def apply_gravity(self):
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    def check_collision(self, platforms):
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0 and self.rect.bottom <= platform.bottom:
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0 and self.rect.top >= platform.top:
                    self.rect.top = platform.bottom
                    self.velocity_y = 0
                elif self.rect.right > platform.left > self.rect.left:
                    self.rect.right = platform.left
                elif self.rect.left < platform.right < self.rect.right:
                    self.rect.left = platform.right

    def draw(self, screen, szin):
        pygame.draw.rect(screen, szin, self.rect)


class JumpingEnemy:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = pygame.image.load('kepek/bee.png').convert_alpha()  # Kép betöltése
        self.image = pygame.transform.scale(self.original_image, (width, height)).convert_alpha()  # Kép átméretezése
        self.rect = self.image.get_rect()  # Kép téglalap alakú helye
        self.rect.topleft = (self.x, self.y)
        self.jump_strength = 350  # pozitív ugrási erővel működik
        self.moving_up = True
        self.last_update = pygame.time.get_ticks()  # Utolsó frissítés időpontja

    def move(self, fel_y, le_y):
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update
        self.last_update = now

        if self.moving_up:
            self.y -= self.jump_strength * elapsed_time / 1000  # Az ugrási erő időfüggővé tétele
            self.rect.y = int(self.y)  # Koordináta egész számra korrigálása
            if self.rect.y <= fel_y:
                self.moving_up = False
        else:
            self.y += self.jump_strength * elapsed_time / 1000  # Az ugrási erő időfüggővé tétele
            self.rect.y = int(self.y)  # Koordináta egész számra korrigálása
            if self.y >= le_y:
                self.moving_up = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Bombs:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = pygame.image.load('kepek/bomb.png').convert_alpha()  # Kép betöltése
        self.image = pygame.transform.scale(self.original_image, (width, height)).convert_alpha()  # Kép átméretezése
        self.rect = self.image.get_rect()  # Kép téglalap alakú helye
        # Frissítjük a téglalapot az aktuális pozícióval
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        # Frissítjük a téglalapot az aktuális pozícióval
        self.rect.topleft = (self.x, self.y)
        # Kép kirajzolása a megadott pozícióra
        screen.blit(self.image, self.rect)


class FireBall:

    def __init__(self, width, height, orbit_center, orbit_radius, orbit_speed, initial_angle):
        self.width = width
        self.height = height
        self.orbit_center = orbit_center
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.angle = initial_angle  # Kezdeti szög beállítása

        # Kép betöltése és méretezése
        self.image = pygame.image.load('kepek/fire.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, surface):
        # Középpont koordinátái
        cx, cy = self.orbit_center

        # Kép középpontjának számítása a körpályán
        image_center_x = cx + self.orbit_radius * math.cos(self.angle)
        image_center_y = cy + self.orbit_radius * math.sin(self.angle)

        # Kép bal felső sarkának számítása
        image_top_left_x = image_center_x - self.width // 2
        image_top_left_y = image_center_y - self.height // 2

        # Téglalap definiálása a kép köré
        self.rect = pygame.Rect(image_top_left_x, image_top_left_y, self.width, self.height)

        # Kép kirajzolása
        surface.blit(self.image, self.rect.topleft)

    def update(self):
        # Szög frissítése a forgatáshoz
        self.angle += self.orbit_speed
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi

    def collides_with(self, other_rect):
        # Ütközés vizsgálata egy másik téglalappal
        return self.rect.colliderect(other_rect)


import pygame


class Spike(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, left_max, right_max, speed):
        super().__init__()
        # Kép betöltése és méretezése
        self.image = pygame.image.load('kepek/spike.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # 1: jobbra, -1: balra
        self.start_x = x
        self.move_counter = 0
        self.left_max = left_max
        self.right_max = right_max
        self.speed = speed

    def update(self):
        # Mozgás balra vagy jobbra
        self.rect.x += self.direction * self.speed

        # Ellenőrzés, hogy elérte-e a megadott x koordinátákat
        if self.rect.left < self.left_max:
            self.rect.left = self.left_max
            self.direction = 1
        elif self.rect.right > self.right_max:
            self.rect.right = self.right_max
            self.direction = -1

    def draw(self, surface):
        # Kép kirajzolása a megadott felületre
        surface.blit(self.image, self.rect)
