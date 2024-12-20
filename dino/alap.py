import pygame
from modellek import Dino, Cloud, Cactus, Picture, Subtitle


def main() -> None:
    # Initialization
    pygame.init()

    # Screen dimensions
    SCREEN_WIDTH: int = 800
    SCREEN_HEIGHT: int = 600
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pygame Base File")

    # Colors
    BLACK: tuple[int, int, int] = (0, 0, 0)
    WHITE: tuple[int, int, int] = (255, 255, 255)
    FPS_COLOR: tuple[int, int, int] = (0, 0, 0)  # Color of the FPS text (black)

    # Dino Position
    x: int = 20
    y: int = 300

    # score
    score: int = 0
    best_score: int = 0

    # Cactus Position and speed
    cactus_x: int = 780
    cactus_y: int = 315
    speed: int = -10

    # Clock for framerate control
    clock: pygame.time.Clock = pygame.time.Clock()

    # Inheritance
    dino: Dino = Dino(x, y, 'kepek/dino.jfif')

    cloud1: Cloud = Cloud(150, 80, 'kepek/felho.png', 2)
    cloud2: Cloud = Cloud(500, 80, 'kepek/felho.png', 2)
    cloud3: Cloud = Cloud(850, 80, 'kepek/felho.png', 2)

    cactus: Cactus = Cactus(cactus_x, cactus_y, 'kepek/th.jfif', speed)

    lacithelaci_felirat: Picture = Picture(100, 450, 'kepek/lacithelaci.PNG')
    score_subtitle: Subtitle = Subtitle(20, 20, f'Score: {score}')
    best_score_subtitle: Subtitle = Subtitle(20, 50, f'Best Score: {best_score}')

    # Load images for buttons
    play_button_image: pygame.Surface = pygame.image.load('kepek/play.png')  # Replace with your image path
    retry_button_image: pygame.Surface = pygame.image.load('kepek/retry.png')  # Replace with your image path

    # Get the rectangles for buttons
    play_button_rect: pygame.Rect = play_button_image.get_rect(center=(400, 300))
    retry_button_rect: pygame.Rect = retry_button_image.get_rect(center=(400, 300))

    # sounds
    pygame.mixer.init()
    jumping_sound: pygame.mixer.Sound = pygame.mixer.Sound("hangok/jump.mp3")
    game_over_sound: pygame.mixer.Sound = pygame.mixer.Sound("hangok/ovr.mp3")

    # Font for FPS
    font: pygame.font.Font = pygame.font.SysFont("Arial", 30)

    # Running state
    running: bool = True
    game_over: bool = False
    game_started: bool = False  # Flag to check if the game has started

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_SPACE and not game_over and game_started:
                    dino.jump()
                    jumping_sound.play()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Check if the play button was clicked
                if not game_started and play_button_rect.collidepoint((mx, my)):
                    # Start the game
                    game_started = True

                # Check if the retry button was clicked (only when game over)
                if game_over and retry_button_rect.collidepoint((mx, my)):
                    # Restart the game
                    score = 0
                    cactus.x = 780
                    game_over = False
                    game_started = True  # Game restarts

        if game_started and not game_over:
            # Game logic
            dino.update()
            cloud1.update()
            cloud2.update()
            cloud3.update()
            cactus.update()

            # Scoring
            if dino.x == cactus.x:
                score += 1
                score_subtitle.update_szoveg(f'Score: {score}')

            # Collision detection
            if cactus.check_collision(dino):
                # Check if the score is higher than the best score
                if score > best_score:
                    best_score = score
                    best_score_subtitle.update_szoveg(f'Best Score: {best_score}')

                # Reset score after collision
                score = 0
                score_subtitle.update_szoveg(f'Score: {score}')
                if not game_over:
                    game_over_sound.play()
                game_over = True

        # Screen update
        screen.fill(WHITE)

        # Drawing game objects
        dino.draw(screen)
        cloud1.draw(screen)
        cloud2.draw(screen)
        cloud3.draw(screen)
        cactus.draw(screen)
        lacithelaci_felirat.draw(screen)
        score_subtitle.draw(screen)
        best_score_subtitle.draw(screen)

        # Draw ground line
        ground_y: int = 370
        pygame.draw.line(screen, BLACK, (0, ground_y), (SCREEN_WIDTH, ground_y), 5)

        # FPS count and display
        fps: float = clock.get_fps()
        fps_text: pygame.Surface = font.render(f"FPS: {fps:.1f}", True, FPS_COLOR)
        screen.blit(fps_text, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 590))

        # If game over, show retry button
        if game_over:
            screen.blit(retry_button_image, retry_button_rect)  # Draw the retry button

        # Draw the play button (if game has not started yet)
        if not game_started:
            screen.blit(play_button_image, play_button_rect)  # Draw the play button

        # Refresh the screen
        pygame.display.flip()

        # FPS control
        clock.tick(60)

    # Quit
    pygame.quit()


if __name__ == '__main__':
    main()
