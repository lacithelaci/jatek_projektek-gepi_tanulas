import pygame


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
        self.rect = pygame.Rect(x, y, width, height)
        self.jump_strength = -6.5
        self.moving_up = True

    def move(self, fel_y, le_y):
        if self.moving_up:
            self.rect.y -= self.jump_strength
            if self.rect.y >= fel_y:
                self.moving_up = False
        else:
            self.rect.y += self.jump_strength
            if self.rect.y <= le_y:
                self.moving_up = True

    def draw(self, screen, szin):
        pygame.draw.rect(screen, szin, self.rect)


class Bombs:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, szin):
        pygame.draw.rect(screen, szin, self.rect)


def win_or_lose(screen_width, screen_height, screen, szin, uzenet):
    # Játék vége, üzenet megjelenítése
    font = pygame.font.Font(None, 170)
    text = font.render(f"{uzenet}", True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.fill(szin)
    screen.blit(text, text_rect)
    pygame.display.flip()

    # Várakozás 3 másodpercig
    pygame.time.wait(3000)


def hp(screen, lives):
    font = pygame.font.Font(None, 20)
    text = font.render(f"HP: {lives}", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (30, 30)
    screen.blit(text, text_rect)
