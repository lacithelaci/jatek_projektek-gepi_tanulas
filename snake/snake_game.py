import pygame
import random
from enum import Enum
from collections import deque

# Pygame inicializálása
pygame.init()

# ========== KONSTANSOK ==========
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Színek
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

# FPS
FPS = 10


# ========== IRÁNYOK ==========
class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


# ========== KÍGYÓ OSZTÁLY ==========
class Snake:
    def __init__(self):
        """A kígyó inicializálása a játékterület közepén"""
        start_x = GRID_WIDTH // 2
        start_y = GRID_HEIGHT // 2
        # A test egy deque-ként tároljuk (x, y) koordinátákkal
        self.body = deque([
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT

    def change_direction(self, new_direction):
        """Az irány megváltoztatása (de nem az ellenkező irányba)"""
        # Ellenkező irányok elkerülése
        opposite_directions = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT
        }

        if new_direction != opposite_directions[self.direction]:
            self.next_direction = new_direction

    def move(self):
        """A kígyó mozgatása az aktuális irányba"""
        self.direction = self.next_direction

        # Az új fej pozíciójának kiszámítása
        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        # Az új fej hozzáadása
        self.body.appendleft(new_head)

        # Az utolsó szegmens eltávolítása (ha nem ettünk)
        return self.body.pop()

    def grow(self):
        """A kígyó növekedése (maradék pont marad, nem távolítjuk el)"""
        pass  # A move() metódusban az utolsó szegmens eltávolítása elmarad

    def get_head(self):
        """A kígyó fejének pozíciója"""
        return self.body[0]

    def collides_with_self(self):
        """Ellenőrizza, hogy a kígyó önmagába ütközött-e"""
        head = self.get_head()
        return head in list(self.body)[1:]

    def is_out_of_bounds(self):
        """Ellenőrizze, hogy a kígyó kilépett-e a játéktérből"""
        head_x, head_y = self.get_head()
        return head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT


# ========== ÉTEL OSZTÁLY ==========
class Food:
    def __init__(self):
        """Az étel véletlenszerű pozícióban jön létre"""
        self.position = self.generate_random_position()

    def generate_random_position(self):
        """Véletlenszerű pozíció generálása"""
        return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def respawn(self):
        """Az étel új pozícióban jön létre"""
        self.position = self.generate_random_position()


# ========== JÁTÉK OSZTÁLY ==========
class Game:
    def __init__(self):
        """A játék inicializálása"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.game_over = False
        self.score = 0

        self.snake = Snake()
        self.food = Food()

    def handle_input(self):
        """A felhasználó inputjának kezelése"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction(Direction.RIGHT)
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.restart_game()

        return True

    def update(self):
        """A játék állapotának frissítése"""
        if self.game_over:
            return

        # A kígyó mozgatása
        tail = self.snake.move()

        # Ellenőrizze, hogy az étel megevésre került-e
        if self.snake.get_head() == self.food.position:
            self.score += 10
            # A kígyó nő (az utolsó szegmens vissza kerül)
            self.snake.body.append(tail)
            self.food.respawn()

        # Ütközés ellenőrzések
        if self.snake.is_out_of_bounds() or self.snake.collides_with_self():
            self.game_over = True

    def draw(self):
        """A játék rajzolása"""
        self.screen.fill(BLACK)

        # A kígyó rajzolása
        for i, (x, y) in enumerate(self.snake.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            # A fej világosabb zöld
            if i == 0:
                pygame.draw.rect(self.screen, GREEN, rect)
            else:
                pygame.draw.rect(self.screen, DARK_GREEN, rect)
            # Keretezés
            pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Az étel rajzolása (piros kör)
        food_x, food_y = self.food.position
        center = (food_x * GRID_SIZE + GRID_SIZE // 2, food_y * GRID_SIZE + GRID_SIZE // 2)
        pygame.draw.circle(self.screen, RED, center, GRID_SIZE // 2 - 2)

        # A pontszám megjelenítése
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Játék vége üzenet
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.font.render("Press SPACE to restart", True, YELLOW)

            text_width = game_over_text.get_width()
            self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - text_width // 2, WINDOW_HEIGHT // 2 - 50))

            text_width = restart_text.get_width()
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - text_width // 2, WINDOW_HEIGHT // 2 + 20))

        pygame.display.flip()

    def restart_game(self):
        """A játék újraindítása"""
        self.snake = Snake()
        self.food = Food()
        self.game_over = False
        self.score = 0

    def run(self):
        """A játékhurok"""
        running = True

        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


# ========== FŐPROGRAM ==========
if __name__ == "__main__":
    game = Game()
    game.run()