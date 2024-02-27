import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 400, 570
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption('2048')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 24)

# Define colors used in the game
colors = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121), 16: (245, 149, 99),
          32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114), 256: (237, 204, 97), 512: (237, 200, 80),
          1024: (237, 197, 63), 2048: (237, 194, 46), 'light text': (249, 246, 242), 'dark text': (119, 110, 101),
          'other': (0, 0, 0), 'bg': (187, 173, 160)}

# Initialize game state variables
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
player_name = ''
start_time = None
elapsed_time = 0

# Function to draw the scoreboard on the screen
def draw_scoreboard(top_scorers):
    score_text = font.render(f'Score: {score}', True, 'black')
    timer_text = font.render(f'Time: {elapsed_time} s', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(timer_text, (10, 450))

    for i, (name, s, t) in enumerate(top_scorers[:3], start=1):
        player_text = font.render(f'{i}. {name}: {s} - {t} s', True, 'black')
        screen.blit(player_text, (10, 450 + i * 30))

# Function to read top scorers from the file and return them
def get_top_scorers():
    try:
        with open("scoreboard.txt", "r") as file:
            lines = file.readlines()
            scores = [line.strip().split(",") for line in lines if line.strip() and len(line.strip().split(",")) >= 3]
            scores.sort(key=lambda x: (int(x[1]), -float(x[2])), reverse=True)
            return scores[:3]
    except FileNotFoundError:
        return []

# Function to draw the game board on the screen
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)

# Function to draw the pieces (numbers) on the game board
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font_size = max(48 - (5 * value_len), 10)
                font = pygame.font.SysFont('Arial', font_size)
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

# Function to generate new pieces on the board
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full

# Function to handle the player's move and update the score
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]

    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift - 1][j] and not \
                            merged[i - shift][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True
    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] and not \
                            merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True
    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] and not merged[i][
                    j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True
    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] and not \
                            merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board

# Function to draw the game over screen
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 300], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Spacebar to Restart', True, 'white')
    name_text = font.render(f'Player: {player_name}', True, 'white')
    score_text = font.render(f'Score: {score}', True, 'white')
    elapsed_time_text = font.render(f'Time: {elapsed_time}', True, 'white')
    screen.blit(game_over_text1, (90, 75))
    screen.blit(game_over_text2, (90, 115))
    screen.blit(name_text, (90, 155))
    screen.blit(score_text, (90, 195))
    screen.blit(elapsed_time_text, (90, 235))

# Function to draw the name entry screen
def draw_name_entry():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 300], 0, 10)
    entry_text = font.render('Enter Your Name:', True, 'white')
    name_input_text = font.render(player_name, True, 'white')
    screen.blit(entry_text, (100, 120))
    screen.blit(name_input_text, (150, 200))

# Main game loop
run = True
name_entry_mode = True
play_button_pressed = False

while run:
    screen.fill((128, 128, 128))

    if name_entry_mode:
        draw_name_entry()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE and player_name.strip() != '' and player_name not in [name for name, _, _ in get_top_scorers()]:
                    name_entry_mode = False
                    play_button_pressed = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode if event.unicode.isalnum() or event.unicode.isspace() else ""

    elif play_button_pressed:
        # Reset game state here
        play_button_pressed = False
        board_values = [[0 for _ in range(4)] for _ in range(4)]
        spawn_new = True
        init_count = 0
        score = 0
        direction = ''
        game_over = False
        start_time = None

    else:
        draw_board()
        draw_pieces(board_values)
        draw_scoreboard(get_top_scorers())

        if spawn_new or init_count < 2:
            board_values, game_over = new_pieces(board_values)
            spawn_new = False
            init_count += 1

        if direction != '' and not game_over:
            if start_time is None:
                start_time = time.time()
            board_values = take_turn(direction, board_values)
            direction = ''
            spawn_new = True

        if game_over:
            draw_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open("scoreboard.txt", "a") as file:
                        file.write(f"{player_name},{score},{elapsed_time}\n")
                    run = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        with open("scoreboard.txt", "a") as file:
                            file.write(f"{player_name},{score},{elapsed_time}\n")
                        player_name = ""
                        name_entry_mode = True
                        board_values = [[0 for _ in range(4)] for _ in range(4)]
                        spawn_new = True
                        init_count = 0
                        score = 0
                        direction = ''
                        game_over = False
                        start_time = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'

        if not game_over and start_time is not None:
            elapsed_time = round(time.time() - start_time, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()