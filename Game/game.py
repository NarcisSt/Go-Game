from graphics import *
from UtilFunctions import functions as utils
from Menu import menu
import random

"""Constants containing coordinates and sizes for drawing items on window"""
DC = [0, 1, 0, -1]
DL = [-1, 0, 1, 0]
WINDOW_LENGTH = 1000
WINDOW_WIDTH = 700
CELL_DIMENSION = 30
BOARD_MARGIN = 50
X_AXYS_BACK_TO_MENU = 150
Y_AXYS_BACK_TO_MENU = 650
X_AXYS_PLAYER_TURN = 810
Y_AXYS_PLAYER_TURN = 150
X_AXYS_SKIP_TURN = 490
Y_AXYS_SKIP_TURN = 650
X_AXYS_SCORE = 810
Y_AXYS_SCORE = 300
X_AXYS_WHITE = 685
Y_AXYS_WHITE = 360
X_AXYS_BLACK = 935
Y_AXYS_BLACK = 360
X_AXYS_WHITE_SCORE = 685
Y_AXYS_WHITE_SCORE = 420
X_AXYS_BLACK_SCORE = 935
Y_AXYS_BLACK_SCORE = 420
X_AXYS_OFFSET = 100
Y_AXYS_OFFSET = 20
PIECE_RADIUS = 10
X_AXYS_SCOREBOARD_MARGIN = 29
Y_AXYS_SCOREBOARD_MARGIN = 19
X1_AXYS_GAME_OVER_MSG = 190
X2_AXYS_GAME_OVER_MSG = 750
Y1_AXYS_GAME_OVER_MSG = 200
Y2_AXYS_GAME_OVER_MSG = 400
X1_AXYS_WHITE_SCORE = X_AXYS_WHITE_SCORE - X_AXYS_SCOREBOARD_MARGIN
Y1_AXYS_WHITE_SCORE = Y_AXYS_WHITE_SCORE - Y_AXYS_SCOREBOARD_MARGIN
X2_AXYS_WHITE_SCORE = X_AXYS_WHITE_SCORE + X_AXYS_SCOREBOARD_MARGIN
Y2_AXYS_WHITE_SCORE = Y_AXYS_WHITE_SCORE + Y_AXYS_SCOREBOARD_MARGIN
X1_AXYS_BLACK_SCORE = X_AXYS_BLACK_SCORE - X_AXYS_SCOREBOARD_MARGIN
Y1_AXYS_BLACK_SCORE = Y_AXYS_BLACK_SCORE - Y_AXYS_SCOREBOARD_MARGIN
X2_AXYS_BLACK_SCORE = X_AXYS_BLACK_SCORE + X_AXYS_SCOREBOARD_MARGIN
Y2_AXYS_BLACK_SCORE = Y_AXYS_BLACK_SCORE + Y_AXYS_SCOREBOARD_MARGIN


class GameManager:
    """Defines constants for buttons, text, pieces, etc."""

    def __init__(self):
        self.black_score = 0
        self.white_score = 0
        self.player_type = 'CPU'
        self.skipped_turns = 0

    def draw_game(self, window):

        reset_board()
        utils.clear_window(window)
        for i in range(0, 18):
            for j in range(0, 18):
                cell_x1 = BOARD_MARGIN + i * CELL_DIMENSION
                cell_y1 = BOARD_MARGIN + j * CELL_DIMENSION
                cell_x2 = BOARD_MARGIN + (i + 1) * CELL_DIMENSION
                cell_y2 = BOARD_MARGIN + (j + 1) * CELL_DIMENSION
                cell = Rectangle(Point(cell_x1, cell_y1),
                                 Point(cell_x2, cell_y2))
                cell.setOutline('black')
                cell.draw(window)
        utils.draw_big_text_box(window, "Back to menu", X_AXYS_BACK_TO_MENU, Y_AXYS_BACK_TO_MENU)
        utils.draw_simple_text(window, "Player's Turn", X_AXYS_PLAYER_TURN, Y_AXYS_PLAYER_TURN, 30)
        utils.draw_big_text_box(window, "Skip move", X_AXYS_SKIP_TURN, Y_AXYS_SKIP_TURN)
        utils.draw_simple_text(window, "Scoreboard", X_AXYS_SCORE, Y_AXYS_SCORE, 30)
        utils.draw_simple_text(window, "White", X_AXYS_WHITE, Y_AXYS_WHITE, 30)
        utils.draw_simple_text(window, "Black", X_AXYS_BLACK, Y_AXYS_BLACK, 30)
        utils.draw_small_text_box(window, str(self.white_score),
                                  X_AXYS_WHITE_SCORE, Y_AXYS_WHITE_SCORE)
        utils.draw_small_text_box(window, str(self.black_score),
                                  X_AXYS_BLACK_SCORE, Y_AXYS_BLACK_SCORE)

    def handle_mouse_click_game(self, window, turn):
        valid_move_flag = False
        while valid_move_flag is False:
            mouse_data = window.getMouse()
            if get_winner() != 'no winner':
                self.skipped_turns = 0
                self.show_finished_game_message(window, get_winner() + " wins")
            if self.skipped_turns < 2 and get_winner() == 'no winner':
                if utils.mouse_inside_box(mouse_data.x, mouse_data.y,
                                          X_AXYS_BACK_TO_MENU - X_AXYS_OFFSET,
                                          Y_AXYS_BACK_TO_MENU - Y_AXYS_OFFSET,
                                          X_AXYS_BACK_TO_MENU + X_AXYS_OFFSET,
                                          Y_AXYS_BACK_TO_MENU + Y_AXYS_OFFSET):
                    return True, "Menu"
                elif utils.mouse_inside_box(mouse_data.x, mouse_data.y,
                                            X_AXYS_SKIP_TURN - X_AXYS_OFFSET,
                                            Y_AXYS_SKIP_TURN - Y_AXYS_OFFSET,
                                            X_AXYS_SKIP_TURN + X_AXYS_OFFSET,
                                            Y_AXYS_SKIP_TURN + Y_AXYS_OFFSET):
                    return self.handle_pressed_on_passed(window)
                else:
                    for i in range(0, 19):
                        for j in range(0, 19):
                            if self.check_inside_piece_spot(i, j, mouse_data.x, mouse_data.y) is True:
                                return self.handle_placed_a_piece(i, j, turn, window)
            else:
                if utils.mouse_inside_box(mouse_data.x, mouse_data.y,
                                          600 - 100, 300 - 20,
                                          600 + 100, 300 + 20):
                    self.skipped_turns = 0
                    return True, "Menu"
        return True, "Game"

    def make_random_move(self, window):
        self.skipped_turns = 0
        valid_move_flag = False
        while valid_move_flag is False:
            random_move = random.randint(0, 19 * 19 - 1)
            line = random_move % 19
            col = random_move // 19
            if check_valid_position(col, line) is True:
                cell_x = BOARD_MARGIN + line * CELL_DIMENSION
                cell_y = BOARD_MARGIN + col * CELL_DIMENSION
                piece = Circle(Point(cell_x, cell_y), 10)
                piece.setFill('white')
                piece.draw(window)
                self.perform_game_logic(window, col, line, 'white')

                self.reset_scores_on_screen(window)
                return True, "Game"

    def handle_pressed_on_passed(self, window):
        if self.skipped_turns != 1:
            self.skipped_turns = 1
        elif self.skipped_turns == 1:
            self.skipped_turns += 1
        if self.skipped_turns == 2:
            self.show_finished_game_message(window, 'Draw')
            return True, "Game"
        else:
            return True, "PutPiece"

    def handle_placed_a_piece(self, i, j, turn, window):
        if check_valid_position(j, i) is True:
            self.skipped_turns = 0
            piece_x = BOARD_MARGIN + i * CELL_DIMENSION
            piece_y = BOARD_MARGIN + j * CELL_DIMENSION
            piece = Circle(Point(piece_x, piece_y), PIECE_RADIUS)

            piece.setFill(turn)
            piece.draw(window)

            self.perform_game_logic(window, j, i, turn)
            self.reset_scores_on_screen(window)

            return True, "PutPiece"
        else:
            return True, "Game"

    def check_inside_piece_spot(self, i, j, mouse_x, mouse_y):
        return utils.mouse_inside_box(mouse_x, mouse_y,
                                      BOARD_MARGIN + i * CELL_DIMENSION - 10,
                                      BOARD_MARGIN + j * CELL_DIMENSION - 10,
                                      BOARD_MARGIN + i * CELL_DIMENSION + 10,
                                      BOARD_MARGIN + j * CELL_DIMENSION + 10
                                      )

    def reset_scores_on_screen(self, window):
        utils.clear_part_window(window,
                                X1_AXYS_WHITE_SCORE, Y1_AXYS_WHITE_SCORE,
                                X2_AXYS_WHITE_SCORE, Y2_AXYS_WHITE_SCORE)

        utils.clear_part_window(window,
                                X1_AXYS_BLACK_SCORE, Y1_AXYS_BLACK_SCORE,
                                X2_AXYS_BLACK_SCORE, Y2_AXYS_BLACK_SCORE)

        utils.draw_small_text_box(window, str(self.white_score),
                                  X_AXYS_WHITE_SCORE, Y_AXYS_WHITE_SCORE)
        utils.draw_small_text_box(window, str(self.black_score),
                                  X_AXYS_BLACK_SCORE, Y_AXYS_BLACK_SCORE)

    def show_finished_game_message(self, window, message):
        utils.clear_part_window(window,
                                X1_AXYS_GAME_OVER_MSG, Y1_AXYS_GAME_OVER_MSG,
                                X2_AXYS_GAME_OVER_MSG, Y2_AXYS_GAME_OVER_MSG)
        utils.draw_simple_text(window, message, 300, 300, 30)
        utils.draw_big_text_box(window, "Back to menu", 600, 300)

    def perform_game_logic(self, window, i, j, turn):
        (self.white_score, self.black_score) = add_piece(i, j, turn, self.white_score, self.black_score)
        (self.white_score, self.black_score) = eliminate_surrounded_pieces()
        mark_eliminated_pieces(window)

    def set_player_type(self, player_type):
        self.player_type = player_type
        if self.player_type != 'CPU' and self.player_type != 'Human':
            self.player_type = 'CPU'

    def get_player_type(self):
        return self.player_type


def reset_board():
    global board
    board = []
    for i in range(0, 19):
        row = []
        for j in range(0, 19):
            row.append(0)
        board.append(row)


def check_valid_position(x, y):
    global board
    if board[x][y] == 0:
        return True
    return False


def get_winner():
    global board
    free = 0
    white = 0
    black = 0
    for i in range(0, 19):
        for j in range(0, 19):
            if board[i][j] == 0:
                free += 1
            elif board[i][j] == 1:
                white += 1
            else:
                black += 1
    if white > free + black:
        return 'white'
    elif black > free + white:
        return 'black'
    else:
        return 'no winner'


def add_piece(x, y, turn, white_score, black_score):
    global board
    if turn == 'white':
        board[x][y] = 1
        white_score += 1
    else:
        board[x][y] = 2
        black_score += 1
    return white_score, black_score


def mark_eliminated_pieces(window):
    global board_aux
    for i in range(0, 19):
        for j in range(0, 19):
            if board_aux[i][j] == -3:
                line1 = Line(Point(35 + j * 30, 35 + i * 30),
                             Point(35 + (j + 1) * 30, 35 + (i + 1) * 30))
                line1.setFill('red')
                line1.draw(window)


def eliminate_surrounded_pieces():
    global board
    global board_aux
    board_aux = []
    board_aux = board
    white_score = 0
    black_score = 0
    for i in range(0, 19):
        for j in range(0, 19):
            if board_aux[i][j] == 1 or board_aux[i][j] == 2:
                if not has_liberty(i, j):
                    fill(i, j, -3)
    for i in range(0, 19):
        for j in range(0, 19):
            if board_aux[i][j] == -1:
                board[i][j] = 1
                white_score += 1
            elif board_aux[i][j] == -2:
                board[i][j] = 2
                black_score += 1
    return white_score, black_score



def has_liberty(x, y):
    global queue
    queue = []
    hasLiberty = False
    color = board_aux[x][y]
    queue.append([x, y])
    while len(queue) > 0:
        curr_pos = queue.pop(0)
        new_pos = curr_pos
        for i in range(0, 4):
            new_pos[0] += DL[i]
            new_pos[1] += DC[i]
            if 0 <= new_pos[0] <= 18 and 0 <= new_pos[1] <= 18:
                if board_aux[new_pos[0]][new_pos[1]] == color:
                    queue.append([new_pos[0], new_pos[1]])
                if board_aux[new_pos[0]][new_pos[1]] == 0:
                    hasLiberty = True
            new_pos[0] -= DL[i]
            new_pos[1] -= DC[i]
        board_aux[curr_pos[0]][curr_pos[1]] = -color
    return hasLiberty



def fill(x, y, new_val):
    color = board_aux[x][y]
    queue.append([x, y])
    while len(queue) > 0:
        curr_pos = queue.pop(0)
        new_pos = curr_pos
        for i in range(0, 4):
            new_pos[0] += DL[i]
            new_pos[1] += DC[i]
            if 0 <= new_pos[0] <= 18 and 0 <= new_pos[1] <= 18:
                if board_aux[new_pos[0]][new_pos[1]] == color:
                    queue.append([new_pos[0], new_pos[1]])
            new_pos[0] -= DL[i]
            new_pos[1] -= DC[i]
        board_aux[curr_pos[0]][curr_pos[1]] = new_val


"""This method is used to initialize the game window, with the constant sizes defined above"""


def initialize_game_window():
    global window
    window = GraphWin("Go Game", WINDOW_LENGTH, WINDOW_WIDTH)



def begin_the_game():
    global window, turn, actual_game_started
    game_running = True
    current_action = "Menu"
    game_manager = GameManager()

    while game_running:
        if current_action == "Menu":
            actual_game_started = False
            menu.draw_main_menu(window)
            (game_running, current_action) = menu.menu_buttons_actions(window)
        elif current_action == "Play":
            actual_game_started = False
            (game_running, current_action) = menu.menu_buttons_actions(window)
        elif current_action == 'CPU':
            game_manager.set_player_type('CPU')
            current_action = 'Game'
        elif current_action == 'Player 2':
            game_manager.set_player_type('Human')
            current_action = 'Game'
        elif current_action == "Game":
            if not actual_game_started:
                turn = 'black'
                game_manager.draw_game(window)
                actual_game_started = True

            piece = Circle(Point(810, 200), 20)
            piece.setFill(turn)
            piece.draw(window)

            if game_manager.player_type == 'Human':
                (game_running, current_action) = game_manager.handle_mouse_click_game(window, turn)

                if current_action == 'PutPiece':
                    current_action = 'Game'
                    if turn == 'white':
                        turn = 'black'
                    else:
                        turn = 'white'
            else:
                (game_running, current_action) = game_manager.handle_mouse_click_game(window, turn)
                if current_action == 'PutPiece':
                    current_action = 'Game'
                game_manager.make_random_move(window)

    window.close()


initialize_game_window()
begin_the_game()
