import pygame, sys, random

# ----- Inicialização -----
pygame.init()

# ----- Tela cheia -----
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("🐍 Galme Snake")
clock = pygame.time.Clock()

# ----- Cores -----
BLACK = (20, 20, 20)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
WHITE = (255, 255, 255)
RED = (220, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 215, 0)
BUTTON_COLOR = (50, 50, 50)
HOVER_COLOR = (100, 100, 100)
GRADIENT_TOP = (10, 10, 40)
GRADIENT_BOTTOM = (0, 50, 100)
MAZE_COLOR = (50, 50, 50)  # cor das linhas do labirinto

# ----- Fontes -----
font = pygame.font.SysFont("Arial", 32, bold=True)
big_font = pygame.font.SysFont("Arial", 72, bold=True)

# ----- Fundo gradiente -----
def draw_gradient():
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(GRADIENT_TOP[0] * (1 - ratio) + GRADIENT_BOTTOM[0] * ratio)
        g = int(GRADIENT_TOP[1] * (1 - ratio) + GRADIENT_BOTTOM[1] * ratio)
        b = int(GRADIENT_TOP[2] * (1 - ratio) + GRADIENT_BOTTOM[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

# ----- Labirinto estilo grid -----
def draw_maze_lines():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, MAZE_COLOR, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, MAZE_COLOR, (0, y), (WIDTH, y))

# ----- Cobra -----
def draw_snake(snake, direction):
    for i, (x, y) in enumerate(snake):
        color = (0, 255 - i*5, 0) if i != 0 else GREEN
        pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), border_radius=6)
        if i == 0:
            eye_radius = 3
            if direction == "UP":
                pygame.draw.circle(screen, WHITE, (x + 5, y + 5), eye_radius)
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 5, y + 5), eye_radius)
            elif direction == "DOWN":
                pygame.draw.circle(screen, WHITE, (x + 5, y + CELL_SIZE - 5), eye_radius)
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 5, y + CELL_SIZE - 5), eye_radius)
            elif direction == "LEFT":
                pygame.draw.circle(screen, WHITE, (x + 5, y + 5), eye_radius)
                pygame.draw.circle(screen, WHITE, (x + 5, y + CELL_SIZE - 5), eye_radius)
            elif direction == "RIGHT":
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 5, y + 5), eye_radius)
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE - 5, y + CELL_SIZE - 5), eye_radius)
            pygame.draw.arc(screen, RED, (x + 4, y + 8, 12, 8), 3.14, 0, 2)

# ----- Maçã -----
def draw_apple(food):
    pygame.draw.circle(screen, RED, (food[0]+CELL_SIZE//2, food[1]+CELL_SIZE//2), CELL_SIZE//2-2)
    pygame.draw.circle(screen, GREEN, (food[0]+CELL_SIZE//2, food[1]-4), 6)
    pygame.draw.rect(screen, BROWN, (food[0]+CELL_SIZE//2-2, food[1]-6, 4, 8))

# ----- Menu -----
def menu_screen():
    waiting = True
    button_width, button_height = 350, 60
    stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]
    snake_anim = [(WIDTH//2 - 100, HEIGHT//2), (WIDTH//2 - 120, HEIGHT//2), (WIDTH//2 - 140, HEIGHT//2)]

    while waiting:
        screen.fill(BLACK)
        draw_gradient()

        # Fundo animado (estrelas)
        for i, (sx, sy) in enumerate(stars):
            pygame.draw.circle(screen, WHITE, (sx, sy), 2)
            stars[i] = (sx, (sy + 1) % HEIGHT)

        # Cobra animada atrás do título
        for i, (x, y) in enumerate(snake_anim):
            color = (0, 255 - i*20, 0)
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE), border_radius=6)
        for i in range(len(snake_anim)-1, 0, -1):
            snake_anim[i] = snake_anim[i-1]
        snake_anim[0] = (snake_anim[0][0]+2 if snake_anim[0][0]+2 < WIDTH//2+100 else WIDTH//2 - 100, snake_anim[0][1])

        # Título
        title = big_font.render("🐍 Galme Snake", True, YELLOW)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4 - 50))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Botão Jogar
        start_rect = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - 50, button_width, button_height)
        pygame.draw.rect(screen, HOVER_COLOR if start_rect.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR,
                         start_rect, border_radius=12)
        start_text = font.render("JOGAR", True, WHITE)
        screen.blit(start_text, (start_rect.centerx - start_text.get_width()//2, start_rect.centery - start_text.get_height()//2))

        # Botão Sair
        exit_rect = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 40, button_width, button_height)
        pygame.draw.rect(screen, HOVER_COLOR if exit_rect.collidepoint(mouse_x, mouse_y) else BUTTON_COLOR,
                         exit_rect, border_radius=12)
        exit_text = font.render("SAIR", True, WHITE)
        screen.blit(exit_text, (exit_rect.centerx - exit_text.get_width()//2, exit_rect.centery - exit_text.get_height()//2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_rect.collidepoint(event.pos):
                    waiting = False
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# ----- Game Over -----
def game_over_screen(score):
    screen.fill(BLACK)
    draw_gradient()
    draw_maze_lines()
    over_text = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    restart_text = font.render("Pressione ESPAÇO para reiniciar", True, YELLOW)
    exit_text = font.render("Pressione ESC para sair", True, WHITE)

    screen.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 120))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 40))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 40))
    screen.blit(exit_text, (WIDTH//2 - exit_text.get_width()//2, HEIGHT//2 + 100))
    pygame.display.flip()

# ----- Jogo principal -----
def main():
    menu_screen()
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"
    food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
    score = 0
    speed = 10
    running = True
    game_over = False

    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
                elif event.key == pygame.K_SPACE and game_over:
                    return main()
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            x, y = snake[0]
            if direction == "UP":
                y -= CELL_SIZE
            elif direction == "DOWN":
                y += CELL_SIZE
            elif direction == "LEFT":
                x -= CELL_SIZE
            elif direction == "RIGHT":
                x += CELL_SIZE

            new_head = (x, y)

            if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)

                if new_head == food:
                    score += 10
                    speed += 0.5
                    food = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
                else:
                    snake.pop()

            # Fundo, labirinto e elementos
            draw_gradient()
            draw_maze_lines()
            draw_snake(snake, direction)
            draw_apple(food)
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (20, 20))
            pygame.display.flip()
        else:
            game_over_screen(score)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
