import pygame
import random
from enum import Enum
from collections import deque
import heapq
import math

# Pygame inicializálása
pygame.init()

# ========== KONSTANSOK ==========
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Színek
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
DARK_BLUE = (0, 70, 200)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
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
    def __init__(self, start_x, start_y, color, is_ai=False):
        """A kígyó inicializálása"""
        self.body = deque([
            (start_x, start_y),
            (start_x - 1, start_y),
            (start_x - 2, start_y)
        ])
        self.direction = Direction.RIGHT
        self.next_direction = Direction.RIGHT
        self.color = color
        self.is_ai = is_ai
        self.score = 0
        self.alive = True

    def change_direction(self, new_direction):
        """Az irány megváltoztatása (de nem az ellenkező irányba)"""
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

        head_x, head_y = self.body[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)

        self.body.appendleft(new_head)
        return self.body.pop()

    def grow(self, tail):
        """A kígyó növekedése"""
        self.body.append(tail)
        self.score += 10

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

    def collides_with_other(self, other_snake):
        """Ellenőrizza, hogy ütközött-e a másik kígyóval"""
        head = self.get_head()
        return head in other_snake.body


# ========== ÉTEL OSZTÁLY ==========
class Food:
    def __init__(self, snake1, snake2):
        """Az étel véletlenszerű pozícióban jön létre"""
        self.snake1 = snake1
        self.snake2 = snake2
        self.position = self.generate_random_position()

    def generate_random_position(self):
        """Véletlenszerű pozíció generálása (nem a kígyók testén)"""
        while True:
            pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if pos not in self.snake1.body and pos not in self.snake2.body:
                return pos

    def respawn(self):
        """Az étel új pozícióban jön létre"""
        self.position = self.generate_random_position()


# ========== AI PATHFINDING ==========
class AIPathfinder:
    @staticmethod
    def heuristic(pos, goal):
        """Manhattan távolság heurisztika"""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    @staticmethod
    def get_neighbors(pos, snake_body, other_body):
        """Az elérhető szomszédos pozíciókat adja vissza"""
        neighbors = []
        x, y = pos

        for direction in Direction:
            dx, dy = direction.value
            new_x, new_y = x + dx, y + dy

            # Határok ellenőrzése
            if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT:
                # Nem ütközik saját testével (az utolsó szegmens elhagyható)
                if (new_x, new_y) not in list(snake_body)[:-1] and (new_x, new_y) not in other_body:
                    neighbors.append(((new_x, new_y), direction))

        return neighbors

    @staticmethod
    def find_path_to_food(snake, other_snake, food_pos, max_iterations=1000):
        """A* algoritmus az étel felé való útvonalhoz"""
        start = snake.get_head()
        goal = food_pos

        open_set = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: AIPathfinder.heuristic(start, goal)}

        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1
            _, current = heapq.heappop(open_set)

            if current == goal:
                # Útvonal rekonstruálása
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()

                if path:
                    next_pos = path[0]
                else:
                    next_pos = start

                # Irány meghatározása
                dx = next_pos[0] - start[0]
                dy = next_pos[1] - start[1]

                for direction in Direction:
                    if direction.value == (dx, dy):
                        return direction

                return snake.direction

            for neighbor, direction in AIPathfinder.get_neighbors(current, snake.body, other_snake.body):
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + AIPathfinder.heuristic(neighbor, goal)
                    f_score[neighbor] = f
                    heapq.heappush(open_set, (f, neighbor))

        # Ha nincs útvonal, próbáljon bármerre mozogni
        neighbors = AIPathfinder.get_neighbors(start, snake.body, other_snake.body)
        if neighbors:
            return neighbors[0][1]
        return snake.direction

    @staticmethod
    def make_ai_decision(snake, other_snake, food):
        """Az AI döntést hoz a következő mozgásról"""
        # Először az étel felé próbáljon mozogni
        best_direction = AIPathfinder.find_path_to_food(snake, other_snake, food.position)

        # Ellenőrizzük, hogy az irány biztonságos-e
        head_x, head_y = snake.get_head()
        dx, dy = best_direction.value
        next_pos = (head_x + dx, head_y + dy)

        # Ha az irány biztonságos, használjuk
        if (0 <= next_pos[0] < GRID_WIDTH and
                0 <= next_pos[1] < GRID_HEIGHT and
                next_pos not in list(snake.body)[:-1] and
                next_pos not in other_snake.body):
            snake.change_direction(best_direction)
        else:
            # Keressünk egy biztonságos irányt
            neighbors = AIPathfinder.get_neighbors(snake.get_head(), snake.body, other_snake.body)
            if neighbors:
                snake.change_direction(neighbors[0][1])


# ========== JÁTÉK OSZTÁLY ==========
class Game:
    def __init__(self):
        """A játék inicializálása"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game - Player vs AI")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

        self.game_over = False
        self.winner = None
        self.ai_counter = 0  # AI lassítás számára

        # Két kígyó inicializálása
        self.snake_player = Snake(GRID_WIDTH // 4, GRID_HEIGHT // 2, GREEN, is_ai=False)
        self.snake_ai = Snake(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2, BLUE, is_ai=True)

        self.food = Food(self.snake_player, self.snake_ai)

    def handle_input(self):
        """A felhasználó inputjának kezelése"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake_player.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    self.snake_player.change_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake_player.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake_player.change_direction(Direction.RIGHT)
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_ESCAPE:
                    return False

        return True

    def update(self):
        """A játék állapotának frissítése"""
        if self.game_over:
            return

        # AI döntés (minden 2. frame-ben)
        self.ai_counter += 1
        if self.ai_counter >= 1:  # AI ugyanolyan gyorsan mozog
            AIPathfinder.make_ai_decision(self.snake_ai, self.snake_player, self.food)
            self.ai_counter = 0

        # Mindkét kígyó mozgatása
        tail_player = self.snake_player.move()
        tail_ai = self.snake_ai.move()

        # Étel evés ellenőrzése - játékos
        if self.snake_player.get_head() == self.food.position:
            self.snake_player.grow(tail_player)
            self.food.respawn()

        # Étel evés ellenőrzése - AI
        if self.snake_ai.get_head() == self.food.position:
            self.snake_ai.grow(tail_ai)
            self.food.respawn()

        # Ütközés ellenőrzések - játékos
        if self.snake_player.is_out_of_bounds() or self.snake_player.collides_with_self():
            self.snake_player.alive = False
            self.game_over = True
            self.winner = "AI"

        if self.snake_player.collides_with_other(self.snake_ai):
            self.snake_player.alive = False
            self.game_over = True
            self.winner = "AI"

        # Ütközés ellenőrzések - AI
        if self.snake_ai.is_out_of_bounds() or self.snake_ai.collides_with_self():
            self.snake_ai.alive = False
            self.game_over = True
            self.winner = "Player"

        if self.snake_ai.collides_with_other(self.snake_player):
            self.snake_ai.alive = False
            self.game_over = True
            self.winner = "Player"

    def draw(self):
        """A játék rajzolása"""
        self.screen.fill(BLACK)

        # Játéktér közepén egy vonal
        pygame.draw.line(self.screen, GRAY, (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT), 1)

        # Játékos kígyójának rajzolása (zöld)
        for i, (x, y) in enumerate(self.snake_player.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0:
                pygame.draw.rect(self.screen, GREEN, rect)
            else:
                pygame.draw.rect(self.screen, DARK_GREEN, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)

        # AI kígyójának rajzolása (kék)
        for i, (x, y) in enumerate(self.snake_ai.body):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if i == 0:
                pygame.draw.rect(self.screen, BLUE, rect)
            else:
                pygame.draw.rect(self.screen, DARK_BLUE, rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)

        # Az étel rajzolása (piros kör)
        food_x, food_y = self.food.position
        center = (food_x * GRID_SIZE + GRID_SIZE // 2, food_y * GRID_SIZE + GRID_SIZE // 2)
        pygame.draw.circle(self.screen, ORANGE, center, GRID_SIZE // 2 - 2)

        # Pontszámok
        player_score_text = self.font_medium.render(f"Player: {self.snake_player.score}", True, GREEN)
        ai_score_text = self.font_medium.render(f"AI: {self.snake_ai.score}", True, BLUE)

        self.screen.blit(player_score_text, (20, 20))
        self.screen.blit(ai_score_text, (WINDOW_WIDTH - 300, 20))

        # Játék vége üzenet
        if self.game_over:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            if self.winner == "Player":
                result_text = self.font_large.render("YOU WIN!", True, GREEN)
                color = GREEN
            else:
                result_text = self.font_large.render("AI WINS!", True, BLUE)
                color = BLUE

            restart_text = self.font_medium.render("Press SPACE to restart or ESC to quit", True, YELLOW)

            result_width = result_text.get_width()
            self.screen.blit(result_text, (WINDOW_WIDTH // 2 - result_width // 2, WINDOW_HEIGHT // 2 - 80))

            restart_width = restart_text.get_width()
            self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_width // 2, WINDOW_HEIGHT // 2 + 40))

            # Végső pontszámok
            final_scores = self.font_small.render(
                f"Your score: {self.snake_player.score}  |  AI score: {self.snake_ai.score}",
                True, WHITE
            )
            scores_width = final_scores.get_width()
            self.screen.blit(final_scores, (WINDOW_WIDTH // 2 - scores_width // 2, WINDOW_HEIGHT // 2 + 120))

        pygame.display.flip()

    def restart_game(self):
        """A játék újraindítása"""
        self.snake_player = Snake(GRID_WIDTH // 4, GRID_HEIGHT // 2, GREEN, is_ai=False)
        self.snake_ai = Snake(3 * GRID_WIDTH // 4, GRID_HEIGHT // 2, BLUE, is_ai=True)
        self.food = Food(self.snake_player, self.snake_ai)
        self.game_over = False
        self.winner = None
        self.ai_counter = 0

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
