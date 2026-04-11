import pygame
import sys
import random
from pygame.locals import *
from kor import Circle


SKY_TOP = (113, 197, 207)
SKY_BOT = (160, 220, 230)
GROUND_COLOR = (222, 184, 135)
GRASS_COLOR = (83, 179, 77)
PIPE_COLOR = (83, 179, 77)
PIPE_BORDER = (55, 140, 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 220, 50)

WIDTH, HEIGHT = 480, 640
GROUND_H = 80
PIPE_WIDTH = 70
PIPE_GAP = 160
PIPE_SPEED = 3
GRAVITY = 0.5
JUMP_FORCE = -9
FPS = 60


def draw_background(screen, clouds):
    screen.fill(SKY_TOP)
    for cx, cy in clouds:
        pygame.draw.ellipse(screen, WHITE, (cx, cy, 80, 35))
        pygame.draw.ellipse(screen, WHITE, (cx + 20, cy - 15, 60, 35))
        pygame.draw.ellipse(screen, WHITE, (cx + 45, cy, 70, 30))


def draw_ground(screen):
    pygame.draw.rect(screen, GROUND_COLOR, (0, HEIGHT - GROUND_H, WIDTH, GROUND_H))
    pygame.draw.rect(screen, GRASS_COLOR, (0, HEIGHT - GROUND_H, WIDTH, 18))


def draw_pipe(screen, x, gap_y):
    top_h = gap_y
    bot_y = gap_y + PIPE_GAP
    bot_h = HEIGHT - GROUND_H - bot_y

    pygame.draw.rect(screen, PIPE_COLOR, (x, 0, PIPE_WIDTH, top_h - 10))
    pygame.draw.rect(screen, PIPE_BORDER, (x - 5, top_h - 30, PIPE_WIDTH + 10, 30))
    pygame.draw.rect(screen, PIPE_BORDER, (x - 4, top_h - 29, PIPE_WIDTH + 8, 28))
    pygame.draw.rect(screen, PIPE_COLOR, (x + 2, top_h - 28, PIPE_WIDTH - 4, 26))

    pygame.draw.rect(screen, PIPE_COLOR, (x, bot_y + 10, PIPE_WIDTH, bot_h))
    pygame.draw.rect(screen, PIPE_BORDER, (x - 5, bot_y, PIPE_WIDTH + 10, 30))
    pygame.draw.rect(screen, PIPE_BORDER, (x - 4, bot_y + 1, PIPE_WIDTH + 8, 28))
    pygame.draw.rect(screen, PIPE_COLOR, (x + 2, bot_y + 2, PIPE_WIDTH - 4, 26))


def game_over_screen(screen, font_big, font_small, score, best):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))
    screen.blit(overlay, (0, 0))

    panel = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 - 110, 260, 220)
    pygame.draw.rect(screen, (255, 240, 180), panel, border_radius=16)
    pygame.draw.rect(screen, (200, 160, 60), panel, 3, border_radius=16)

    go_text = font_big.render("Game Over", True, (180, 60, 30))
    screen.blit(go_text, go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 70)))

    sc_text = font_small.render(f"Pontszám: {score}", True, BLACK)
    screen.blit(sc_text, sc_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))

    best_text = font_small.render(f"Legjobb: {best}", True, (80, 80, 80))
    screen.blit(best_text, best_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

    btn = pygame.Rect(WIDTH // 2 - 80, HEIGHT // 2 + 60, 160, 45)
    pygame.draw.rect(screen, GRASS_COLOR, btn, border_radius=10)
    pygame.draw.rect(screen, (40, 120, 40), btn, 2, border_radius=10)
    btn_text = font_small.render("Újra (SPACE)", True, WHITE)
    screen.blit(btn_text, btn_text.get_rect(center=btn.center))

    return btn


def game(best_score=0):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    font_big = pygame.font.Font(None, 52)
    font_mid = pygame.font.Font(None, 42)
    font_small = pygame.font.Font(None, 32)

    bird = Circle(100, HEIGHT // 2, 20, (255, 160, 30), GRAVITY)

    pipes = []
    pipe_timer = 0
    PIPE_INTERVAL = 90
    pipe_id_counter = 0

    clouds = [(random.randint(0, WIDTH - 80), random.randint(20, 150)) for _ in range(4)]
    cloud_speed = 0.1

    score = 0
    best = best_score
    started = False
    alive = True
    passed_pipes = set()

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    if alive:
                        bird.jump(JUMP_FORCE)
                        started = True
                    else:
                        return score
            if event.type == MOUSEBUTTONDOWN:
                if alive:
                    bird.jump(JUMP_FORCE)
                    started = True

        if started and alive:
            bird.update(GRAVITY)

            pipe_timer += 1
            if pipe_timer >= PIPE_INTERVAL:
                gap_y = random.randint(120, HEIGHT - GROUND_H - PIPE_GAP - 60)
                pipes.append([WIDTH, gap_y, pipe_id_counter])
                pipe_id_counter += 1
                pipe_timer = 0

            for p in pipes:
                p[0] -= PIPE_SPEED

            pipes = [p for p in pipes if p[0] > -PIPE_WIDTH - 10]


            clouds = [((cx - cloud_speed) % (WIDTH + 80) - 80, cy) for cx, cy in clouds]

            for px, gap_y, pid in pipes:
                top_rect = pygame.Rect(px - 5, 0, PIPE_WIDTH + 10, gap_y - 10)
                bot_rect = pygame.Rect(px - 5, gap_y + PIPE_GAP + 10, PIPE_WIDTH + 10,
                                       HEIGHT - GROUND_H - gap_y - PIPE_GAP - 10)
                if bird.collides_with_rect(top_rect) or bird.collides_with_rect(bot_rect):
                    alive = False

                if pid not in passed_pipes and px + PIPE_WIDTH < bird.x:
                    score += 1
                    if score > best:
                        best = score
                    passed_pipes.add(pid)

            if bird.y - bird.sugar < 0:
                bird.y = bird.sugar
                bird.velocity = 0
            if bird.y + bird.sugar >= HEIGHT - GROUND_H:
                alive = False

        draw_background(screen, clouds)

        for px, gap_y, _ in pipes:
            draw_pipe(screen, px, gap_y)

        draw_ground(screen)
        bird.draw(screen)

        if not started:
            hint = font_small.render("Nyomj SPACE-t az indításhoz!", True, WHITE)
            shadow = font_small.render("Nyomj SPACE-t az indításhoz!", True, BLACK)
            screen.blit(shadow, hint.get_rect(center=(WIDTH // 2 + 1, HEIGHT // 3 + 1)))
            screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

        score_text = font_mid.render(str(score), True, WHITE)
        score_shadow = font_mid.render(str(score), True, BLACK)
        screen.blit(score_shadow, score_text.get_rect(center=(WIDTH // 2 + 2, 52)))
        screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, 50)))

        if not alive:
            btn = game_over_screen(screen, font_big, font_small, score, best)

        pygame.display.flip()

        if not alive:
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        waiting = False
                    if event.type == MOUSEBUTTONDOWN:
                        if btn.collidepoint(event.pos):
                            waiting = False
            return score


def menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    font_title = pygame.font.Font(None, 80)
    font_btn = pygame.font.Font(None, 42)
    font_small = pygame.font.Font(None, 28)

    clouds = [(random.randint(0, WIDTH - 80), random.randint(20, 150)) for _ in range(4)]
    best = 0

    while True:
        clock.tick(FPS)
        clouds = [((cx - 0.4) % (WIDTH + 80) - 80, cy) for cx, cy in clouds]

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == K_SPACE:
                    result = game(best)
                    if result > best:
                        best = result
            if event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                start_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 55)
                quit_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 95, 200, 55)
                if start_btn.collidepoint(mx, my):
                    result = game(best)
                    if result > best:
                        best = result
                if quit_btn.collidepoint(mx, my):
                    pygame.quit()
                    sys.exit()

        draw_background(screen, clouds)
        draw_ground(screen)

        title = font_title.render("Flappy", True, YELLOW)
        title2 = font_title.render("Bird", True, YELLOW)
        t_shadow = font_title.render("Flappy", True, (180, 120, 0))
        t2_shadow = font_title.render("Bird", True, (180, 120, 0))
        screen.blit(t_shadow, title.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 3 - 17)))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 20)))
        screen.blit(t2_shadow, title2.get_rect(center=(WIDTH // 2 + 3, HEIGHT // 3 + 53)))
        screen.blit(title2, title2.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 50)))

        start_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 55)
        quit_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 95, 200, 55)

        pygame.draw.rect(screen, GRASS_COLOR, start_btn, border_radius=12)
        pygame.draw.rect(screen, (40, 120, 40), start_btn, 2, border_radius=12)
        st = font_btn.render("Start", True, WHITE)
        screen.blit(st, st.get_rect(center=start_btn.center))

        pygame.draw.rect(screen, (200, 70, 60), quit_btn, border_radius=12)
        pygame.draw.rect(screen, (140, 40, 30), quit_btn, 2, border_radius=12)
        qt = font_btn.render("Kilépés", True, WHITE)
        screen.blit(qt, qt.get_rect(center=quit_btn.center))

        if best > 0:
            b = font_small.render(f"Legjobb: {best}", True, WHITE)
            screen.blit(b, b.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 175)))

        hint = font_small.render("vagy nyomj SPACE-t", True, (220, 220, 220))
        screen.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 10)))

        pygame.display.flip()


if __name__ == '__main__':
    menu()
