import pygame
import random

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("2048")
timer = pygame.time.Clock()
fps = 60
# font_size = 24
font = pygame.font.Font("freesansbold.ttf", 24)

# 2048 game color library
colors = {
    # 0:(r,g,b),
    # 2:(r,g,b),
    0: "#CDC1B4",
    2: "#EEE4DA",
    4: "#EDE0C8",
    8: "#F2B179",
    16: "#F59563",
    32: "#F67C5F",
    64: "#F65E3B",
    128: "#EDCF72",
    256: "#EDCC61",
    512: "#EDC850",
    1024: "#EDC53F",
    2048: "#EDC22E",
    "light text": (249, 246, 242),
    "dark text": (119, 110, 101),
    "other": (0, 0, 0),
    "bg": (187, 173, 160),
}

# game variables initialization
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ""


# take your turn based on direction
def take_turn(direc, board):
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == "UP":
        go_up(direc, board, merged)
    elif direc == "DOWN":
        go_down(direc, board, merged)
    elif direc == "LEFT":
        go_left(direc, board, merged)
    elif direc == "RIGHT":
        go_right(direc, board, merged)
    return board


def go_up(direc, board, merged):
    # going thru every square on the board
    for i in range(4):
        for j in range(4):
            shift = 0
            # if not in the top row, bc top row can't go up
            if i > 0:
                for q in range(i):
                    if board[q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[i - shift][j] = board[i][j]
                    board[i][j] = 0
                if (
                    board[i - shift - 1][j] == board[i - shift][j]
                    and not merged[i - shift - 1][j]
                    and not merged[i - shift][j]
                ):
                    board[i - shift - 1][j] *= 2
                    board[i - shift][j] = 0
                    merged[i - shift - 1][j] = True


def go_down(direc, board, merged):
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
                if (
                    board[2 - i + shift][j] == board[3 - i + shift][j]
                    and not merged[3 - i + shift][j]
                    and not merged[2 - i + shift][j]
                ):
                    board[3 - i + shift][j] *= 2
                    board[2 - i + shift][j] = 0
                    merged[3 - i + shift][j] = True


def go_left(direc, board, merged):
    for i in range(4):
        for j in range(4):
            shift = 0
            for q in range(j):
                if board[i][q] == 0:
                    shift += 1
            if shift > 0:
                board[i][j - shift] = board[i][j]
                board[i][j] = 0
            if (
                board[i][j - shift] == board[i][j - shift - 1]
                and not merged[i][j - shift - 1]
                and not merged[i][j - shift]
            ):
                board[i][j - shift - 1] *= 2
                board[i][j - shift] = 0
                merged[i][j - shift - 1] = True


def go_right(direc, board, merged):
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
                if (
                    board[i][4 - j + shift] == board[i][3 - j + shift]
                    and not merged[i][4 - j + shift]
                    and not merged[i][3 - j + shift]
                ):
                    board[i][4 - j + shift] *= 2
                    board[i][3 - j + shift] = 0
                    merged[i][4 - j + shift] = True


# spawning in new pieces randomly when turns begin
def new_pieces(board):
    full = False
    count = 0
    # checking if there are any empty tiles to still populate
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            # this gives a 1/10 chance of getting a 4 instead of a 2
            # as the new value that populates the empty tile
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors["bg"], [0, 0, 400, 400], 0, 10)
    pass


# draw tiles for the game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors["light text"]
            else:
                value_color = colors["dark text"]
            if value <= 2048:
                color = colors[value]
            else:
                color = colors["other"]
            # first two are top right and left corner
            # this uses a 20 gap bt each tile
            # border radius of 5
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)

            # if value is > 0, you get a blank background, not a 0
            # makes font smaller as the length gets larger
            # 48 is baseline, and the font size shrinks by 5 for every additional character
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font("freesansbold.ttf", 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rectangle = value_text.get_rect(
                    center=(j * 95 + 20 + (1 / 2 * 75), i * 95 + 20 + (1 / 2 * 75))
                )
                screen.blit(value_text, text_rectangle)
                pygame.draw.rect(
                    screen, "black", [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5
                )


# main loop for the game
run = True
while run:
    timer.tick(fps)
    # fills screen
    screen.fill("gray")
    # background, score, high score
    draw_board()
    # the values / tiles
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != "":
        board_values = take_turn(direction, board_values)
        direction = ""
        spawn_new = True

    for event in pygame.event.get():
        # quit = when you pres red x
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = "UP"
            elif event.key == pygame.K_DOWN:
                direction = "DOWN"
            elif event.key == pygame.K_LEFT:
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT:
                direction = "RIGHT"
            # else:

    pygame.display.flip()
# exiting while loop to exit program
pygame.quit()
