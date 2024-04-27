import sys
import pygame
import random

pygame.init()

# Ablakok
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 25

# Színek
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
COLORS = [RED, BLUE, GREEN]

# Tetris alakzatok
SHAPES = [
    [
        ['.....',
         '.....',
         '.....',
         'OOOO.',
         '.....'],
        ['.....',
         '..O..',
         '..O..',
         '..O..',
         '..O..']
    ],
    [
        ['.....',
         '.....',
         '..O..',
         '.OOO.',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '..OO.',
         '..O..',
         '.....']
    ],
    [
        [
            '.....',
            '.....',
            '..OO.',
            '.OO..',
            '.....'],
        ['.....',
         '.....',
         '.OO..',
         '..OO.',
         '.....'],
        ['.....',
         '.O...',
         '.OO..',
         '..O..',
         '.....'],
        ['.....',
         '..O..',
         '.OO..',
         '.O...',
         '.....']
    ],
    [
        ['.....',
         '..O..',
         '..O.',
         '..OO.',
         '.....'],
        ['.....',
         '...O.',
         '.OOO.',
         '.....',
         '.....'],
        ['.....',
         '.OO..',
         '..O..',
         '..O..',
         '.....'],
        ['.....',
         '.....',
         '.OOO.',
         '.O...',
         '.....']
    ],
]


class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = random.choice(COLORS)  # különböző színű alakzatok
        self.rotation = 0


class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = self.new_piece()
        self.game_over = False
        self.score = 0  # Pontok Lacikám, pontok

    def new_piece(self):
        # Random alakzat
        shape = random.choice(SHAPES)
        # Alakzat létrehozása objektumként
        return Tetromino(self.width // 2, 0, shape)

    def valid_move(self, piece, x, y, rotation):
        # legális-e az adott lépés
        for i, row in enumerate(piece.shape[(piece.rotation + rotation) % len(piece.shape)]):
            for j, cell in enumerate(row):
                try:
                    if cell == 'O' and (self.grid[piece.y + i + y][piece.x + j + x] != 0):
                        return False
                except IndexError:
                    return False
        return True

    def clear_lines(self):
        # képernyőtörlés
        lines_cleared = 0
        for i, row in enumerate(self.grid[:-1]):
            if all(cell != 0 for cell in row):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [0 for _ in range(self.width)])
        return lines_cleared

    def lock_piece(self, piece):
        # előző alakzat megvizsgálása és új létrehozása
        for i, row in enumerate(piece.shape[piece.rotation % len(piece.shape)]):
            for j, cell in enumerate(row):
                if cell == 'O':
                    self.grid[piece.y + i][piece.x + j] = piece.color
        # sorok törlése
        lines_cleared = self.clear_lines()
        self.score += lines_cleared * 100  # pont növelése
        # új alakzat létrehozása
        self.current_piece = self.new_piece()
        # mikor kapok game over-t
        if not self.valid_move(self.current_piece, 0, 0, 0):
            self.game_over = True
        return lines_cleared

    def update(self):
        # mozgás
        if not self.game_over:
            if self.valid_move(self.current_piece, 0, 1, 0):
                self.current_piece.y += 1
            else:
                self.lock_piece(self.current_piece)

    def draw(self, screen):
        # rajzolás
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))

        if self.current_piece:
            for i, row in enumerate(
                    self.current_piece.shape[self.current_piece.rotation % len(self.current_piece.shape)]):
                for j, cell in enumerate(row):
                    if cell == 'O':
                        pygame.draw.rect(screen, self.current_piece.color, (
                            (self.current_piece.x + j) * GRID_SIZE, (self.current_piece.y + i) * GRID_SIZE,
                            GRID_SIZE - 1,
                            GRID_SIZE - 1))


def draw_score(screen, score, x, y):
    # pontszám
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (x, y))


def draw_game_over(screen, x, y):
    # game over felirat
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (x, y))


def main():
    # játék létrehozása
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Tetris')
    # clock objektum létrehozása
    clock = pygame.time.Clock()
    # tetris objektum létrehozása
    game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
    fall_time = 0
    fall_speed = 90  # zuhanási sebesség
    while True:
        # képernyőszín
        screen.fill(BLACK)
        for event in pygame.event.get():
            # kilépés
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # gomb eventek
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if game.valid_move(game.current_piece, -1, 0, 0):
                        game.current_piece.x -= 1  # balra
                if event.key == pygame.K_RIGHT:
                    if game.valid_move(game.current_piece, 1, 0, 0):
                        game.current_piece.x += 1  # jobbra
                if event.key == pygame.K_DOWN:
                    if game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1  # gyorsabban le
                if event.key == pygame.K_UP:
                    if game.valid_move(game.current_piece, 0, 0, 1):
                        game.current_piece.rotation += 1  # alakzat forgatása
                if event.key == pygame.K_SPACE:
                    while game.valid_move(game.current_piece, 0, 1, 0):
                        game.current_piece.y += 1
                    game.lock_piece(game.current_piece)  # ne tudjon egy idő után forogni
        # zuhanási idő visszaadása
        delta_time = clock.get_rawtime()
        fall_time += delta_time
        if fall_time >= fall_speed:
            # Ne mozogjon az alakzat
            game.update()
            # a zuhanási idő nullázása
            fall_time = 0
        # pont megjelenése
        draw_score(screen, game.score, 10, 10)
        # kirajzolja az alakzatot a képernyőre
        game.draw(screen)
        if game.game_over:
            # Game over
            draw_game_over(screen, WIDTH // 2 - 100, HEIGHT // 2 - 30)  # game over szöveg kiírása
            # bármilyen gomb a játék újraindításához
            # eventek
            if event.type == pygame.KEYDOWN:
                # tetris objektum létrehozása
                game = Tetris(WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE)
        # képernyő frissítés
        pygame.display.flip()
        # 60 fps
        clock.tick(60)


if __name__ == "__main__":
    main()
