import pygame
import math


class Circle:
    def __init__(self, x, y, sugar, szin, zuhanas):
        self.x = x
        self.y = y
        self.sugar = sugar
        self.color = szin
        self.zuhanas = zuhanas
        self.velocity = 0

    def jump(self, ero: int = -9) -> None:
        self.velocity = ero

    def update(self, gravity: float = 0.5) -> None:
        self.velocity += gravity
        if self.velocity > 12:
            self.velocity = 12
        self.y += self.velocity

    def draw(self, screen) -> None:
        angle = max(-30, min(self.velocity * 5, 90))

        beak_color = (255, 165, 0)
        eye_color = (255, 255, 255)
        pupil_color = (0, 0, 0)
        belly_color = (255, 220, 100)

        rad = math.radians(-angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)

        def rot(ox, oy):
            rx = ox * cos_a - oy * sin_a + self.x
            ry = ox * sin_a + oy * cos_a + self.y
            return (int(rx), int(ry))

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.sugar)

        belly_points = [rot(0, 2), rot(self.sugar - 4, 6), rot(self.sugar - 4, -4), rot(0, -6)]
        pygame.draw.polygon(screen, belly_color, belly_points)

        beak_points = [rot(self.sugar - 2, -3), rot(self.sugar + 8, 0), rot(self.sugar - 2, 3)]
        pygame.draw.polygon(screen, beak_color, beak_points)

        eye_pos = rot(4, -6)
        pygame.draw.circle(screen, eye_color, eye_pos, 5)
        pupil_pos = rot(5, -6)
        pygame.draw.circle(screen, pupil_color, pupil_pos, 3)

        wing_points = [rot(-4, 0), rot(-2, -self.sugar + 2), rot(6, -self.sugar + 4), rot(8, -2)]
        pygame.draw.polygon(screen, (200, 80, 0), wing_points)

    def collides_with_rect(self, rect) -> bool:
        closest_x = max(rect.left, min(self.x, rect.right))
        closest_y = max(rect.top, min(self.y, rect.bottom))

        distance_x = self.x - closest_x
        distance_y = self.y - closest_y

        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        return distance < self.sugar - 2
