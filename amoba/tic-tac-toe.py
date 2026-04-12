import pygame
import random
from enum import Enum
from typing import List, Tuple, Optional

# Pygame inicializálás
pygame.init()

# Konstansok
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 1000
GRID_SIZE = 3
CELL_SIZE = 200
GRID_OFFSET_X = 250  # Középre helyezve
GRID_OFFSET_Y = 300
FPS = 60


# Színek (modern paletta)
class Colors:
    BG_DARK = (15, 23, 42)  # Sötét kék
    PRIMARY = (59, 130, 246)  # Világos kék
    SECONDARY = (139, 92, 246)  # Lila
    SUCCESS = (34, 197, 94)  # Zöld
    DANGER = (239, 68, 68)  # Piros
    TEXT_LIGHT = (241, 245, 250)  # Fehér
    TEXT_DARK = (15, 23, 42)  # Sötét
    GRID_LINE = (75, 85, 99)  # Szürke
    CELL_HOVER = (30, 58, 138)  # Sötét kék hover
    CELL_ACTIVE = (99, 102, 241)  # Indigo


# Játékos típusok
class GameMode(Enum):
    MENU = 1
    PLAYER_VS_AI = 2
    PLAYER_VS_PLAYER = 3
    GAME_OVER = 4


class Difficulty(Enum):
    EASY = 1
    MEDIUM = 2
    HARD = 3


# Gomb osztály
class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: Tuple[int, int, int]):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False
        self.base_color = color

    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        # Szín váltás hover-nél
        color = tuple(min(c + 30, 255) for c in self.base_color) if self.hover else self.base_color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, Colors.PRIMARY, self.rect, 2, border_radius=15)

        # Szöveg
        text_surface = font.render(self.text, True, Colors.TEXT_LIGHT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos)

    def update_hover(self, pos: Tuple[int, int]) -> None:
        self.hover = self.rect.collidepoint(pos)


# TicTacToe játék logika
class TicTacToe:
    def __init__(self):
        self.board: List[List[str]] = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
        self.current_player = "X"
        self.game_over = False
        self.winner: Optional[str] = None
        self.moves = 0

    def make_move(self, row: int, col: int, player: str) -> bool:
        """Lépés végrehajtása"""
        if self.board[row][col] == "-":
            self.board[row][col] = player
            self.moves += 1
            return True
        return False

    def check_winner(self) -> Optional[str]:
        """Győztes ellenőrzése"""
        # Sorok
        for row in self.board:
            if row[0] == row[1] == row[2] != "-":
                return row[0]

        # Oszlopok
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "-":
                return self.board[0][col]

        # Átlók
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "-":
            return self.board[0][0]

        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "-":
            return self.board[0][2]

        return None

    def get_available_moves(self) -> List[Tuple[int, int]]:
        """Elérhető lépések"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "-":
                    moves.append((i, j))
        return moves

    def is_board_full(self) -> bool:
        """Tábla megtelt-e"""
        return self.moves == 9

    def reset(self) -> None:
        """Játék visszaállítása"""
        self.board = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.moves = 0


# AI játékos
class AI:
    def __init__(self, difficulty: Difficulty = Difficulty.HARD):
        self.difficulty = difficulty
        self.player = "O"
        self.opponent = "X"

    def get_best_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Legjobb lépés meghatározása"""
        if self.difficulty == Difficulty.EASY:
            return self._easy_move(board)
        elif self.difficulty == Difficulty.MEDIUM:
            return self._medium_move(board)
        else:  # HARD
            return self._minimax_move(board)

    def _easy_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Könnyű AI - véletlenszerű lépés"""
        available = []
        for i in range(3):
            for j in range(3):
                if board[i][j] == "-":
                    available.append((i, j))
        return random.choice(available) if available else (0, 0)

    def _medium_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Közepes AI - alapvető stratégia"""
        # Próbálunk nyerni
        move = self._find_winning_move(board, self.player)
        if move:
            return move

        # Blokkolunk
        move = self._find_winning_move(board, self.opponent)
        if move:
            return move

        # Közép foglalása
        if board[1][1] == "-":
            return (1, 1)

        # Szögek
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [c for c in corners if board[c[0]][c[1]] == "-"]
        if available_corners:
            return random.choice(available_corners)

        # Véletlenszerű
        return self._easy_move(board)

    def _minimax_move(self, board: List[List[str]]) -> Tuple[int, int]:
        """Nehéz AI - Minimax algoritmus"""
        best_score = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] == "-":
                    board[i][j] = self.player
                    score = self._minimax(board, 0, False)
                    board[i][j] = "-"

                    if score > best_score:
                        best_score = score
                        best_move = (i, j)

        return best_move if best_move else (0, 0)

    def _minimax(self, board: List[List[str]], depth: int, is_maximizing: bool) -> int:
        """Minimax rekurzív függvény"""
        winner = self._check_winner(board)

        if winner == self.player:
            return 10 - depth
        elif winner == self.opponent:
            return depth - 10

        # Döntetlen
        if all(board[i][j] != "-" for i in range(3) for j in range(3)):
            return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "-":
                        board[i][j] = self.player
                        score = self._minimax(board, depth + 1, False)
                        board[i][j] = "-"
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "-":
                        board[i][j] = self.opponent
                        score = self._minimax(board, depth + 1, True)
                        board[i][j] = "-"
                        best_score = min(score, best_score)
            return best_score

    def _find_winning_move(self, board: List[List[str]], player: str) -> Optional[Tuple[int, int]]:
        """Nyerő vagy blokkoló lépés keresése"""
        for i in range(3):
            for j in range(3):
                if board[i][j] == "-":
                    board[i][j] = player
                    if self._check_winner(board) == player:
                        board[i][j] = "-"
                        return (i, j)
                    board[i][j] = "-"
        return None

    @staticmethod
    def _check_winner(board: List[List[str]]) -> Optional[str]:
        """Győztes ellenőrzése"""
        # Sorok
        for row in board:
            if row[0] == row[1] == row[2] != "-":
                return row[0]

        # Oszlopok
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "-":
                return board[0][col]

        # Átlók
        if board[0][0] == board[1][1] == board[2][2] != "-":
            return board[0][0]

        if board[0][2] == board[1][1] == board[2][0] != "-":
            return board[0][2]

        return None


# Főalkalmazás
class TicTacToeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("TicTacToe - Modern Edition")
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 28)

        self.game_mode = GameMode.MENU
        self.difficulty = Difficulty.HARD
        self.game = TicTacToe()
        self.ai = AI(self.difficulty)
        self.ai_thinking = False
        self.ai_move_timer = 0

        # Gombok
        self.menu_buttons = [
            Button(150, 300, 600, 80, "Játékos vs AI", Colors.PRIMARY),
            Button(150, 420, 600, 80, "Játékos vs Játékos", Colors.SECONDARY),
            Button(150, 540, 600, 80, "Kilépés", Colors.DANGER)
        ]

        self.difficulty_buttons = [
            Button(150, 300, 600, 80, "Könnyű", Colors.SUCCESS),
            Button(150, 420, 600, 80, "Közepes", Colors.PRIMARY),
            Button(150, 540, 600, 80, "Nehéz", Colors.DANGER)
        ]

        self.game_over_buttons = [
            Button(150, 700, 600, 80, "Új játék", Colors.PRIMARY),
            Button(150, 820, 600, 80, "Menü", Colors.SECONDARY)
        ]

        self.exit_button = Button(800, 20, 80, 50, "✕", Colors.DANGER)

    def handle_events(self) -> bool:
        """Event kezelés"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Kilépés gomb (minden képernyőn)
                if self.exit_button.is_clicked(pos) and self.game_mode != GameMode.MENU:
                    self.game_mode = GameMode.MENU
                    self.game.reset()

                if self.game_mode == GameMode.MENU:
                    if self.menu_buttons[0].is_clicked(pos):
                        self.game_mode = GameMode.PLAYER_VS_AI
                        self.show_difficulty_selection()
                    elif self.menu_buttons[1].is_clicked(pos):
                        self.game_mode = GameMode.PLAYER_VS_PLAYER
                        self.game.reset()
                    elif self.menu_buttons[2].is_clicked(pos):
                        return False

                elif self.game_mode == GameMode.PLAYER_VS_AI:
                    self.handle_game_click(pos, is_ai=True)

                elif self.game_mode == GameMode.PLAYER_VS_PLAYER:
                    self.handle_game_click(pos, is_ai=False)

                elif self.game_mode == GameMode.GAME_OVER:
                    if self.game_over_buttons[0].is_clicked(pos):
                        self.game.reset()
                        if hasattr(self, '_is_ai_game'):
                            self.show_difficulty_selection()
                            self.game_mode = GameMode.PLAYER_VS_AI
                        else:
                            self.game_mode = GameMode.PLAYER_VS_PLAYER
                    elif self.game_over_buttons[1].is_clicked(pos):
                        self.game_mode = GameMode.MENU

            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                if self.game_mode == GameMode.MENU:
                    for btn in self.menu_buttons:
                        btn.update_hover(pos)
                elif self.game_mode == GameMode.GAME_OVER:
                    for btn in self.game_over_buttons:
                        btn.update_hover(pos)
                else:
                    self.exit_button.update_hover(pos)

        return True

    def show_difficulty_selection(self) -> None:
        """Nehézség kiválasztása"""
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.difficulty_buttons[0].is_clicked(pos):
                        self.difficulty = Difficulty.EASY
                        self.ai = AI(self.difficulty)
                        selecting = False
                    elif self.difficulty_buttons[1].is_clicked(pos):
                        self.difficulty = Difficulty.MEDIUM
                        self.ai = AI(self.difficulty)
                        selecting = False
                    elif self.difficulty_buttons[2].is_clicked(pos):
                        self.difficulty = Difficulty.HARD
                        self.ai = AI(self.difficulty)
                        selecting = False

                if event.type == pygame.MOUSEMOTION:
                    pos = pygame.mouse.get_pos()
                    for btn in self.difficulty_buttons:
                        btn.update_hover(pos)

            self.draw_difficulty_selection()

    def handle_game_click(self, pos: Tuple[int, int], is_ai: bool) -> None:
        """Játék kattintás kezelése"""
        if self.game.game_over or self.ai_thinking:
            return

        col = (pos[0] - GRID_OFFSET_X) // CELL_SIZE
        row = (pos[1] - GRID_OFFSET_Y) // CELL_SIZE

        if 0 <= row < 3 and 0 <= col < 3:
            if self.game.make_move(row, col, "X"):
                winner = self.game.check_winner()

                if winner:
                    self.game.game_over = True
                    self.game.winner = winner
                    self.game_mode = GameMode.GAME_OVER
                elif self.game.is_board_full():
                    self.game.game_over = True
                    self.game_mode = GameMode.GAME_OVER
                elif is_ai:
                    self.ai_thinking = True
                    self.ai_move_timer = 60  # 1 másodperc
                    self._is_ai_game = True

    def update(self) -> None:
        """Frissítés logika"""
        if self.game_mode == GameMode.PLAYER_VS_AI and self.ai_thinking:
            self.ai_move_timer -= 1

            if self.ai_move_timer <= 0:
                move = self.ai.get_best_move(self.game.board)
                if self.game.make_move(move[0], move[1], "O"):
                    winner = self.game.check_winner()

                    if winner:
                        self.game.game_over = True
                        self.game.winner = winner
                        self.game_mode = GameMode.GAME_OVER
                    elif self.game.is_board_full():
                        self.game.game_over = True
                        self.game_mode = GameMode.GAME_OVER

                self.ai_thinking = False

    def draw(self) -> None:
        """Rajzolás"""
        self.screen.fill(Colors.BG_DARK)

        if self.game_mode == GameMode.MENU:
            self.draw_menu()
        elif self.game_mode == GameMode.PLAYER_VS_AI or self.game_mode == GameMode.PLAYER_VS_PLAYER:
            self.draw_game()
        elif self.game_mode == GameMode.GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self) -> None:
        """Menü rajzolása"""
        # Cím
        title = self.font_large.render("TicTacToe", True, Colors.PRIMARY)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        subtitle = self.font_small.render("Modern Edition", True, Colors.TEXT_LIGHT)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 170))
        self.screen.blit(subtitle, subtitle_rect)

        # Gombok
        for btn in self.menu_buttons:
            btn.draw(self.screen, self.font_medium)

    def draw_game(self) -> None:
        """Játéktábla rajzolása"""
        # Cím
        if self.game_mode == GameMode.PLAYER_VS_AI:
            title_text = "Játékos vs AI"
        else:
            title_text = f"Játékos vs Játékos - {self.game.current_player} lép"

        title = self.font_medium.render(title_text, True, Colors.PRIMARY)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        # Kilépés gomb
        self.exit_button.draw(self.screen, self.font_medium)

        # Tábla rajzolása
        for i in range(3):
            for j in range(3):
                x = GRID_OFFSET_X + j * CELL_SIZE
                y = GRID_OFFSET_Y + i * CELL_SIZE

                # Cella
                pygame.draw.rect(self.screen, Colors.CELL_ACTIVE, (x, y, CELL_SIZE, CELL_SIZE), 2)

                # Tartalom
                cell_content = self.game.board[i][j]
                if cell_content != "-":
                    color = Colors.PRIMARY if cell_content == "X" else Colors.SECONDARY
                    text = self.font_large.render(cell_content, True, color)
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)

        # AI gondolkozik jelzés
        if self.ai_thinking:
            thinking = self.font_small.render("AI gondolkozik...", True, Colors.DANGER)
            thinking_rect = thinking.get_rect(center=(WINDOW_WIDTH // 2, 900))
            self.screen.blit(thinking, thinking_rect)

    def draw_game_over(self) -> None:
        """Játék vége rajzolása"""
        self.draw_game()

        # Overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(Colors.BG_DARK)
        self.screen.blit(overlay, (0, 0))

        # Üzenet
        if self.game.winner:
            if self.game.winner == "X":
                msg = "🎉 GRATULÁLOK! Nyertél! 🎉"
                color = Colors.SUCCESS
            else:
                msg = "Az AI nyert! 🤖"
                color = Colors.DANGER
        else:
            msg = "Döntetlen! 🤝"
            color = Colors.PRIMARY

        title = self.font_large.render(msg, True, color)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 300))
        self.screen.blit(title, title_rect)

        # Gombok
        for btn in self.game_over_buttons:
            btn.draw(self.screen, self.font_medium)

    def draw_difficulty_selection(self) -> None:
        """Nehézség kiválasztása rajzolása"""
        self.screen.fill(Colors.BG_DARK)

        # Cím
        title = self.font_medium.render("Válassz nehézségi szintet!", True, Colors.PRIMARY)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Gombok
        for btn in self.difficulty_buttons:
            btn.draw(self.screen, self.font_medium)

        pygame.display.flip()

    def run(self) -> None:
        """Főciklus"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


# Alkalmazás futtatása
if __name__ == "__main__":
    game = TicTacToeGame()
    game.run()
