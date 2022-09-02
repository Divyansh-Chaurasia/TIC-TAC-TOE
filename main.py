import pygame

pygame.init()

WIDTH, HEIGHT = 550, 570
# ICON = pygame.image.load('Icon.ico')

WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# pygame.display.set_icon(ICON)
pygame.display.set_caption('Tic Tac Toe')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (51, 153, 255)
BG_COLOR = (242, 159, 47)
GRID_COLOR = (98, 85, 64)

TOP_PANEL = 80
BOTTOM_PANEL = 60

GAMEBOARD_WIDTH = 325
GAMEBOARD_HEIGHT = 325

GAMEBOARD_X = WIDTH//2 - GAMEBOARD_WIDTH//2
GAMEBOARD_Y = HEIGHT//2 - GAMEBOARD_HEIGHT//2 - BOTTOM_PANEL//2 + TOP_PANEL//2

CELLS = 3
CELL_SIZE = GAMEBOARD_WIDTH//CELLS

GRID_WIDTH = 10
PADDING = 20

PLAYER_X = 'X'
PLAYER_O = 'O'

X_IMAGE = pygame.transform.scale(pygame.image.load(
    'X.png'), (CELL_SIZE - 50, CELL_SIZE - 50))
O_IMAGE = pygame.transform.scale(pygame.image.load(
    'O.png'), (CELL_SIZE - 50, CELL_SIZE - 50))

HOME_IMAGE_BLACK = pygame.transform.scale(
    pygame.image.load('Home_black.png'), (25, 25))
HOME_IMAGE_WHITE = pygame.transform.scale(
    pygame.image.load('Home_white.png'), (25, 25))

TITLE_SCREEN_IMAGE = pygame.transform.scale(
    pygame.image.load('Title_screen.png'), (200, 200))

FPS = 30


class Image_Button():
    def __init__(self, pos, width, height, bg_color, image):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.image = image

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color,
                         (self.x, self.y, self.width, self.height))
        surface.blit(self.image, (self.x + self.width//2 - self.image.get_width() //
                     2, self.y + self.height//2 - self.image.get_height()//2))

    def is_hovering(self):
        x, y = pygame.mouse.get_pos()
        if self.x + self.width > x > self.x and self.y + self.height > y > self.y:
            return True
        return False


class Text_Button():
    def __init__(self, pos, width, height, text, text_color, bg_color, text_size, radius=0):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.text_color = text_color
        self.bg_color = bg_color
        self.text_size = text_size
        self.radius = radius

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect,
                         border_radius=self.radius)
        font = pygame.font.Font('Nunito-Black.ttf', self.text_size)
        text = font.render(self.text, 1, self.text_color)
        surface.blit(text, (self.x + self.width//2 - text.get_width() //
                     2, self.y + self.height//2 - text.get_height()//2))

    def is_hovering(self):
        x, y = pygame.mouse.get_pos()
        if self.x + self.width > x > self.x and self.y + self.height > y > self.y:
            return True
        return False


class Board():
    def __init__(self):
        self.board = [[0 for i in range(CELLS)] for j in range(CELLS)]
        self.filled = False

    def draw(self, surface):
        for row in range(CELLS):
            for col in range(CELLS):
                if self.board[row][col] != 0:
                    image = X_IMAGE if self.board[row][col] == PLAYER_X else O_IMAGE
                    surface.blit(image, (GAMEBOARD_X + col * CELL_SIZE + (CELL_SIZE//2 - image.get_width(
                    )//2), GAMEBOARD_Y + row * CELL_SIZE + (CELL_SIZE//2 - image.get_width()//2)))

        for i in range(CELLS - 1):
            pygame.draw.line(surface, GRID_COLOR, (GAMEBOARD_X + (i + 1) * CELL_SIZE, GAMEBOARD_Y),
                             (GAMEBOARD_X + (i + 1) * CELL_SIZE, GAMEBOARD_Y + GAMEBOARD_WIDTH), GRID_WIDTH)
        for j in range(CELLS - 1):
            pygame.draw.line(surface, GRID_COLOR, (GAMEBOARD_X, GAMEBOARD_Y + (j + 1) * CELL_SIZE),
                             (GAMEBOARD_X + GAMEBOARD_HEIGHT, GAMEBOARD_Y + (j + 1) * CELL_SIZE), GRID_WIDTH)

    def place_piece(self, pos, player):
        if self.board[pos[1]][pos[0]] == 0:
            self.board[pos[1]][pos[0]] = player
            return True
        return False

    def check_win(self, current_player):
        for i in range(CELLS):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != 0:
                return [current_player, ((0, i), (2, i)), (1, 0)]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != 0:
                return [current_player, ((i, 0), (i, 2)), (0, 1)]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[1][1] != 0:
            return [current_player, ((0, 0), (2, 2)), (1, 1)]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[1][1] != 0:
            return [current_player, ((0, 2), (2, 0)), (-1, -1)]

        blank_space_found = False

        for i in range(CELLS):
            for j in range(CELLS):
                if self.board[i][j] == 0:
                    blank_space_found = True
                    break

        self.filled = not blank_space_found

        return None

    def reset(self):
        self.board = [[0 for i in range(CELLS)] for j in range(CELLS)]
        self.filled = False


class Game:
    def __init__(self):
        self.turn = PLAYER_X
        self.x_wins = 0
        self.o_wins = 0
        self.gameover = False
        self.match_over = False
        self.game_draw = False
        self.winner = None
        self.win_pos = None
        self.direction = None
        self.board = Board()

    def change_turn(self):
        self.turn = PLAYER_X if self.turn == PLAYER_O else PLAYER_O

    def place_piece(self, pos):
        if not self.gameover:
            piece_placed = self.board.place_piece(pos, self.turn)
            if piece_placed:
                if self.x_wins == 3 or self.o_wins == 3:
                    self.match_over = True
                self.winner = self.board.check_win(self.turn)
                self.change_turn()
                self.check_for_gameover()

    def check_for_gameover(self):
        if self.x_wins < 3 and self.o_wins < 3:
            if self.winner != None:
                self.win_pos = self.winner[1]
                self.direction = self.winner[2]
                self.winner = self.winner[0]
                self.gameover = True

                if self.winner == PLAYER_X:
                    self.x_wins += 1
                else:
                    self.o_wins += 1

            elif self.board.filled:
                self.gameover = True
                self.game_draw = True

    def draw_gameover(self, surface):
        if self.gameover and not self.match_over:
            color = RED if self.turn == PLAYER_O else BLUE
            if self.direction == (1, 0):
                pygame.draw.line(surface, color, (GAMEBOARD_X + self.win_pos[0][0] * CELL_SIZE + PADDING, GAMEBOARD_Y + self.win_pos[0][1] * CELL_SIZE + CELL_SIZE//2), (
                    GAMEBOARD_X + self.win_pos[1][0] * CELL_SIZE + CELL_SIZE - PADDING, GAMEBOARD_Y + self.win_pos[1][1] * CELL_SIZE + CELL_SIZE//2), GRID_WIDTH//2)
            if self.direction == (0, 1):
                pygame.draw.line(surface, color, (GAMEBOARD_X + self.win_pos[0][0] * CELL_SIZE + CELL_SIZE//2, GAMEBOARD_Y + self.win_pos[0][1] * CELL_SIZE + PADDING), (
                    GAMEBOARD_X + self.win_pos[1][0] * CELL_SIZE + CELL_SIZE//2, GAMEBOARD_Y + self.win_pos[1][1] * CELL_SIZE + CELL_SIZE - PADDING), GRID_WIDTH//2)
            if self.direction == (1, 1):
                pygame.draw.line(surface, color, (GAMEBOARD_X + self.win_pos[0][0] * CELL_SIZE + PADDING, GAMEBOARD_Y + self.win_pos[0][1] * CELL_SIZE + PADDING), (
                    GAMEBOARD_X + self.win_pos[1][0] * CELL_SIZE + CELL_SIZE - PADDING, GAMEBOARD_Y + self.win_pos[1][1] * CELL_SIZE + CELL_SIZE - PADDING), GRID_WIDTH//2)
            if self.direction == (-1, -1):
                pygame.draw.line(surface, color, (GAMEBOARD_X + self.win_pos[0][0] * CELL_SIZE + PADDING, GAMEBOARD_Y + self.win_pos[0][1] * CELL_SIZE + CELL_SIZE - PADDING), (
                    GAMEBOARD_X + self.win_pos[1][0] * CELL_SIZE + CELL_SIZE - PADDING, GAMEBOARD_Y + self.win_pos[1][1] * CELL_SIZE + PADDING), GRID_WIDTH//2)

    def reset_board(self):
        self.turn = PLAYER_X
        self.gameover = False
        self.winner = None
        self.win_pos = None
        self.direction = None
        self.game_draw = False
        self.board.reset()

    def restart(self):
        self.reset_board()
        self.match_over = False
        self.x_wins = 0
        self.o_wins = 0


def draw_top_panel(game):
    x_image = pygame.transform.scale(X_IMAGE, (50, 50))
    o_image = pygame.transform.scale(O_IMAGE, (50, 50))

    font = pygame.font.Font('Nunito-Black.ttf', 60)

    x_label = font.render(str(game.x_wins), 1, BLACK)
    o_label = font.render(str(game.o_wins), 1, BLACK)

    WIN.blit(x_label, (x_image.get_width() + 40,
             TOP_PANEL//2 - x_label.get_height()//2))
    WIN.blit(o_label, (WIDTH - o_label.get_width() -
             o_image.get_width() - 40, TOP_PANEL//2 - o_label.get_height()//2))

    WIN.blit(x_image, (20, TOP_PANEL//2 - x_image.get_height()//2))
    WIN.blit(o_image, (WIDTH - o_image.get_width() - 20,
             TOP_PANEL//2 - o_image.get_height()//2))

    pygame.draw.rect(WIN, BLACK, (3, 3, WIDTH - 5, TOP_PANEL - 5), 3, 20)
    pygame.draw.rect(WIN, BLACK, (140, 3, WIDTH - 285, TOP_PANEL - 5), 3)

    text_font = pygame.font.Font('Nunito-Black.ttf', 30)
    text = ''

    if game.gameover:
        if game.game_draw:
            text = "GAME DRAW"
        else:
            text = f"{game.winner} WINS!"
    else:
        text = f"{game.turn}'s TURN"

    label = text_font.render(text, 1, BLACK)
    WIN.blit(label, (WIDTH//2 - label.get_width()//2,
             TOP_PANEL//2 - label.get_height()//2))


def draw(game, board, buttons):
    WIN.fill(BG_COLOR)
    if not game.match_over:
        board.draw(WIN)
    game.draw_gameover(WIN)

    for button in buttons:
        button.draw(WIN)

    draw_top_panel(game)

    pygame.display.update()


def calc_pos(pos):
    col, row = -1, -1
    x, y = pos

    if x >= GAMEBOARD_X and x <= GAMEBOARD_X + GAMEBOARD_HEIGHT:
        col = (x - GAMEBOARD_X)//CELL_SIZE

    if y >= GAMEBOARD_Y and y <= GAMEBOARD_Y + GAMEBOARD_WIDTH:
        row = (y - GAMEBOARD_Y)//CELL_SIZE

    return col, row


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()
    close_window = False

    reset_button = Text_Button((0, HEIGHT - BOTTOM_PANEL), WIDTH//2 -
                               BOTTOM_PANEL//2 - 1, BOTTOM_PANEL, 'RESET BOARD', WHITE, BLACK, 15)
    new_game_button = Text_Button((WIDTH//2 + BOTTOM_PANEL//2 + 1, HEIGHT - BOTTOM_PANEL),
                                  WIDTH//2 - BOTTOM_PANEL//2 - 1, BOTTOM_PANEL, 'NEW GAME', WHITE, BLACK, 15)
    home_button = Image_Button((WIDTH//2 - BOTTOM_PANEL//2, HEIGHT - BOTTOM_PANEL),
                               BOTTOM_PANEL, BOTTOM_PANEL, BLACK, HOME_IMAGE_WHITE)
    buttons = [reset_button, new_game_button, home_button]

    while run:
        clock.tick(FPS)
        draw(game, game.board, buttons)

        for button in buttons:
            if button.is_hovering():
                button.bg_color = WHITE
                button.text_color = BLACK
                button.image = HOME_IMAGE_BLACK
            else:
                button.bg_color = BLACK
                button.text_color = WHITE
                button.image = HOME_IMAGE_WHITE

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                close_window = True
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col, row = calc_pos(pos)

                if col != -1 and row != -1:
                    game.place_piece((col, row))

                if home_button.is_hovering():
                    run = False

                if reset_button.is_hovering():
                    game.reset_board()

                if new_game_button.is_hovering():
                    game.reset_board()
                    game.restart()

    if not close_window:
        main_menu()


def main_menu():
    run = True
    close_window = False
    clock = pygame.time.Clock()

    play_button = Text_Button(
        (WIDTH//2 - 400//2, HEIGHT - 200), 400, 60, 'PLAY', WHITE, BLACK, 30, 10)

    quit_button = Text_Button(
        (WIDTH//2 - 400//2, HEIGHT - 120), 400, 60, 'QUIT', WHITE, RED, 30, 10)

    font = pygame.sysfont.Font('Nunito-Black.ttf', 20)
    text = font.render('FIRST ONE TO SCORE 3 POINTS WINS!', 1, BLACK)

    title_font = pygame.sysfont.Font('Nunito-Black.ttf', 50)
    title = title_font.render('TIC TAC TOE', 1, BLACK)

    while run:
        clock.tick(FPS)
        WIN.fill(BG_COLOR)
        play_button.draw(WIN)
        quit_button.draw(WIN)

        if play_button.is_hovering():
            play_button.bg_color = WHITE
            play_button.text_color = BLACK
        else:
            play_button.bg_color = BLACK
            play_button.text_color = WHITE

        if quit_button.is_hovering():
            quit_button.bg_color = WHITE
            quit_button.text_color = RED
        else:
            quit_button.bg_color = RED
            quit_button.text_color = WHITE

        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 20))

        WIN.blit(TITLE_SCREEN_IMAGE, (WIDTH//2 -
                 TITLE_SCREEN_IMAGE.get_width()//2, 100))

        WIN.blit(text, (WIDTH//2 - text.get_width()//2, 320))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                close_window = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.is_hovering():
                    run = False
                    close_window = True
                if play_button.is_hovering():
                    run = False
        pygame.display.update()

    if not close_window:
        main()

    pygame.quit()


main_menu()
