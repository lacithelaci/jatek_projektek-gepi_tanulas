import pygame

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


def hp(screen, lives):
    font = pygame.font.Font(None, 20)
    text = font.render(f"{lives}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (50, 65)
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
