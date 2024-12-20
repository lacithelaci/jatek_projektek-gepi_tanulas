import pygame


class Dino:
    def __init__(self, x: int, y: int, image_path: str) -> None:
        self.x: int = x
        self.y: int = y
        self.start_y: int = y  # Eredeti pozíció a gravitációhoz
        self.image: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        self.jump_speed: int = -15  # Kezdő ugrás sebesség
        self.gravity: int = 1  # Gravitációs gyorsulás
        self.is_jumping: bool = False  # Ugrott-e a dino?
        self.velocity: int = 0  # Sebesség változó

        # A dínó téglalapjának létrehozása
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self) -> None:
        if self.is_jumping:
            self.velocity += self.gravity  # Gravitációval növeljük a sebességet
            self.y += self.velocity  # Pozíció frissítése a sebesség alapján

            if self.y >= self.start_y:
                self.y = self.start_y
                self.is_jumping = False
                self.velocity = 0

        self.rect.topleft = (self.x, self.y)

    def jump(self) -> None:
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity = self.jump_speed

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class Cloud:
    def __init__(self, x: int, y: int, image_path: str, speed: int) -> None:
        self.x: int = x
        self.y: int = y
        self.image: pygame.Surface = pygame.image.load(image_path).convert_alpha()
        self.speed: int = speed

    def update(self) -> None:
        self.x -= self.speed
        if self.x < -220:
            self.x = 800  # Felhő visszaállítása

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class Cactus:
    def __init__(self, x: int, y: int, image: str, speed: int) -> None:
        self.x: int = x
        self.y: int = y
        self.image: pygame.Surface = pygame.image.load(image).convert_alpha()
        self.width: int = self.image.get_width()
        self.height: int = self.image.get_height()
        self.speed: int = speed

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self) -> None:
        self.x += self.speed
        if self.x < -self.width:
            self.x = 780  # Ha a kaktusz elérte a bal oldalt

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, dino: Dino) -> bool:
        return self.rect.colliderect(dino.rect)  # Ütközés vizsgálat


class Picture:
    def __init__(self, x: int, y: int, image_path: str) -> None:
        self.x: int = x
        self.y: int = y
        self.image: pygame.Surface = pygame.image.load(image_path)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class Subtitle:
    def __init__(self, x: int, y: int, szoveg: str, betutipus: str = "Arial", betumeret: int = 20,
                 szin: tuple = (0, 0, 0)) -> None:
        self.x: int = x
        self.y: int = y
        self.szoveg: str = szoveg
        self.szin: tuple = szin
        self.betutipus: pygame.font.Font = pygame.font.SysFont(betutipus, betumeret)

    def draw(self, screen: pygame.Surface) -> None:
        text_surface: pygame.Surface = self.betutipus.render(self.szoveg, True, self.szin)
        screen.blit(text_surface, (self.x, self.y))

    def update_szoveg(self, uj_szoveg: str) -> None:
        self.szoveg = uj_szoveg
