import pygame
import math
import random
from typing import Tuple

# Pygame hangrendszer inicializálása
pygame.mixer.init()
jump_sound = pygame.mixer.Sound('hangok/jump.mp3')  # ugrás hangja


# Játék vége üzenet megjelenítése
def win_or_lose(screen_width: int, screen_height: int, screen: pygame.Surface, szin: Tuple[int, int, int],
                uzenet: str) -> None:
    # Háttérszín kitöltése
    screen.fill(szin)

    # Kép betöltése az üzenet alapján
    if uzenet.upper() == "YOU WIN!":
        image_path = "kepek/win.jpg"
    else:
        image_path = "kepek/lose.jpg"

    # Kép betöltése és átméretezése a képernyőhöz
    img = pygame.image.load(image_path).convert_alpha()
    img = pygame.transform.scale(img, (screen_width, screen_height))

    # Kép kirajzolása
    screen.blit(img, (0, 0))
    pygame.display.flip()  # frissítés

    # 3 másodperc várakozás
    pygame.time.wait(3000)


# HP megjelenítése
def hp(screen: pygame.Surface, lives: int, hp_poz: Tuple[int, int] = (50, 65)) -> None:
    font = pygame.font.Font(None, 20)  # kis betűméret
    text = font.render(f"{lives}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = hp_poz
    screen.blit(text, text_rect)


# FPS megjelenítése
def display_fps(screen: pygame.Surface, clock: pygame.time.Clock, font: pygame.font.Font,
                color: Tuple[int, int, int] = (255, 255, 255), pos: Tuple[int, int] = (695, 5)) -> None:
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, color)
    screen.blit(fps_text, pos)


# Játékos osztály
class Player:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)  # játékos téglalap
        self.speed = 5
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.on_ground = False

    # Játékos mozgatása
    def move(self, keys: pygame.key.ScancodeWrapper, screen_width: int) -> None:
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = self.jump_strength
            jump_sound.play()
            self.on_ground = False

        # Képernyő széleinek ellenőrzése
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > screen_width - self.rect.width:
            self.rect.x = screen_width - self.rect.width

    # Gravitáció alkalmazása
    def apply_gravity(self) -> None:
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

    # Platformokkal való ütközés ellenőrzése
    def check_collision(self, platforms: list[pygame.Rect]) -> None:
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

    # Játékos kirajzolása
    def draw(self, screen: pygame.Surface, szin: Tuple[int, int, int]) -> None:
        pygame.draw.rect(screen, szin, self.rect)


# Ugráló ellenfél osztály
class JumpingEnemy:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = pygame.image.load('kepek/bee.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.jump_strength = 350  # ugrás sebessége
        self.moving_up = True
        self.last_update = pygame.time.get_ticks()

    # Mozgás fel-le
    def move(self, fel_y: int, le_y: int) -> None:
        now = pygame.time.get_ticks()
        elapsed_time = now - self.last_update
        self.last_update = now

        if self.moving_up:
            self.y -= self.jump_strength * elapsed_time / 1000
            self.rect.y = int(self.y)
            if self.rect.y <= fel_y:
                self.moving_up = False
        else:
            self.y += self.jump_strength * elapsed_time / 1000
            self.rect.y = int(self.y)
            if self.y >= le_y:
                self.moving_up = True

    # Ellenfél kirajzolása
    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)


# Bomba osztály
class Bombs:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = pygame.image.load('kepek/bomb.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width, height)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    # Bomba kirajzolása
    def draw(self, screen: pygame.Surface) -> None:
        self.rect.topleft = (self.x, self.y)
        screen.blit(self.image, self.rect)


# Forgó tűzgolyó osztály
class FireBall:
    def __init__(self, width: int, height: int, orbit_center: Tuple[int, int], orbit_radius: int, orbit_speed: float,
                 initial_angle: float):
        self.rect = None
        self.width = width
        self.height = height
        self.orbit_center = orbit_center
        self.orbit_radius = orbit_radius
        self.orbit_speed = orbit_speed
        self.angle = initial_angle
        self.image = pygame.image.load('kepek/fire.png')
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    # Kirajzolás
    def draw(self, surface: pygame.Surface) -> None:
        cx, cy = self.orbit_center
        image_center_x = cx + self.orbit_radius * math.cos(self.angle)
        image_center_y = cy + self.orbit_radius * math.sin(self.angle)
        image_top_left_x = image_center_x - self.width // 2
        image_top_left_y = image_center_y - self.height // 2
        self.rect = pygame.Rect(image_top_left_x, image_top_left_y, self.width, self.height)
        surface.blit(self.image, self.rect.topleft)

    # Mozgatás pályán
    def update(self) -> None:
        self.angle += self.orbit_speed
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi

    # Ütközés vizsgálata a játékossal
    def collides_with(self, other_rect: Player) -> bool:
        return self.rect.colliderect(other_rect)


# Tüskés akadály osztály
class Spike(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, height: int, width: int, left_max: int, right_max: int, speed: int):
        super().__init__()
        self.image = pygame.image.load('kepek/spike.png')
        self.image = pygame.transform.scale(self.image, (width, height))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # mozgás iránya
        self.start_x = x
        self.move_counter = 0
        self.left_max = left_max
        self.right_max = right_max
        self.speed = speed

    # Mozgás jobbra-balra
    def update(self) -> None:
        self.rect.x += self.direction * self.speed
        if self.rect.left < self.left_max:
            self.rect.left = self.left_max
            self.direction = 1
        elif self.rect.right > self.right_max:
            self.rect.right = self.right_max
            self.direction = -1

    # Kirajzolás
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


# Peashooter osztály
class Peashooter:
    def __init__(self, x: int, y: int, width: int, height: int, bullet_speed: int = 3, spacing: int = 15,
                 upside_down: bool = False):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_image = pygame.image.load('kepek/peashooter.png').convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (width, height))

        # Ha fejjel lefelé, tükrözzük függőlegesen
        self.image = self.original_image
        if upside_down:
            self.image = pygame.transform.flip(self.original_image, False, True)

        self.bullet_speed = bullet_speed
        self.spacing = spacing
        self.bullets = [
            pygame.Rect(x + width + i * spacing, y + height // 2 - 5, 10, 10) for i in range(4)
        ]

    def update(self, screen_width: int) -> None:
        all_passed = True
        for bullet in self.bullets:
            bullet.x += self.bullet_speed  # lövedékek az eredeti irányban mennek
            if bullet.x <= screen_width:
                all_passed = False

        if all_passed:
            self.bullets = [
                pygame.Rect(self.rect.right + i * self.spacing, self.rect.y + self.rect.height // 2 - 5, 10, 10)
                for i in range(4)
            ]

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
        for bullet in self.bullets:
            pygame.draw.circle(surface, (0, 255, 0), bullet.center, 5)

    # Ütközés vizsgálata játékossal
    def check_collision(self, player: Player) -> bool:
        if self.rect.colliderect(player.rect):
            return True
        for bullet in self.bullets:
            if bullet.colliderect(player.rect):
                return True
        return False


# Tallnut osztály (kontakt halál)
class Tallnut:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load("kepek/tallnut.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    # Kirajzolás
    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    # Ütközés vizsgálata
    def check_collision(self, player: Player) -> bool:
        return self.rect.colliderect(player.rect)


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, x_left, x_right, y):
        super().__init__()
        # Sprite
        self.image = pygame.image.load("kepek/bowser.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x_left, y))

        # Mozgás
        self.speed = random.randint(1, 3)  # véletlenszerű sebesség
        self.direction = random.choice([-1, 1])
        self.move_range = (x_left, x_right)

        # Ugrás
        self.gravity = 0
        self.on_ground = True
        self.jump_cooldown = 0

        # Lövedékek
        self.fireballs = pygame.sprite.Group()
        self.shoot_cooldown = 0

    def update(self):
        # Mozgás a két x között
        self.rect.x += self.speed * self.direction

        # Határok ellenőrzése
        if self.rect.left <= self.move_range[0]:
            self.rect.left = self.move_range[0]
            self.direction = 1
        elif self.rect.right >= self.move_range[1]:
            self.rect.right = self.move_range[1]
            self.direction = -1

        # Véletlenszerű irányváltás (5% esély minden frissítéskor)
        if random.randint(0, 100) < 5:
            self.direction *= -1

        # Gravitáció
        self.rect.y += self.gravity
        if not self.on_ground:
            self.gravity += 0.7
        if self.rect.bottom >= 580:
            self.rect.bottom = 580
            self.on_ground = True
            self.gravity = 0

        # Véletlenszerű ugrás
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
        else:
            if self.on_ground and random.randint(0, 100) < 2:
                self.gravity = -12
                self.on_ground = False
                self.jump_cooldown = 120

        # Lövés cooldown (jobb oldalra)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            if random.randint(0, 100) < 2:
                self.shoot_fireball()

        # Lövedékek frissítése
        self.fireballs.update()

    def shoot_fireball(self):
        fireball = Fireball(self.rect.centerx, self.rect.centery, 1)  # csak jobbra
        self.fireballs.add(fireball)
        self.shoot_cooldown = 90

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.fireballs.draw(screen)


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 80, 0), (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6 * direction

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
