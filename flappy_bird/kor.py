import pygame
import math


class Circle:
    def __init__(self, x, y, sugar, szin, zuhanas):
        self.x = x
        self.y = y
        self.sugar = sugar
        self.color = szin
        self.zuhanas = zuhanas

    def move(self) -> None:
        self.y += self.zuhanas

    def draw(self, screen) -> None:
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.sugar)

    def collides_with_rect(self, rect) -> bool:
        # Legközelebbi pont meghatározása a téglalaphoz képest
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))

        # Távolság kiszámítása a kör középpontja és a legközelebbi pont között
        distance_x = self.x - closest_x
        distance_y = self.y - closest_y

        # Euklideszi távolság kiszámítása
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # Ütközés vizsgálata
        return distance < self.sugar
