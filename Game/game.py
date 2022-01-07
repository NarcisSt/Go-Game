from graphics import Rectangle, Circle, GraphWin, Point, Line, color_rgb
from UtilStuff import functions as fun
from UtilStuff import constants as consts
from Menu import menu
import random

"""
Global variables 
"""
aux_game_board = []
game_board = []
turn = ''
actual_game_started = True
queue = []
window: GraphWin


class Game:

    def __init__(self):
        """
        This method initialize the scores and skipped turns with 0 and the type of the player as CPU (that's what i
            picked as default player in the game logic)
        """
        self.black_score = 0
        self.white_score = 0
        self.player_type = 'CPU'
        self.skipped_turns = 0

    def set_player_type(self, player_type):
        """
        This method is a setter for the player type(CPU is default)
        :param player_type: the type of the player
        :return:
        """
        self.player_type = player_type
        if self.player_type != 'CPU' and self.player_type != 'Human':
            self.player_type = 'CPU'

    def get_player_type(self):
        """
        This method is a getter for the player type
        :return: the type of the player
        """
        return self.player_type

    def game_buttons_actions(self, game_window, player_turn):
        """
        This method is used to draw the game window, the table, buttons and scores
        :param game_window: the window where all of this will be drawn
        :param player_turn: which player has to move when the window is created
        :return: a tuple consisting in (will the game continue?, in which state?), based on what button the player is
        clicking
        """
        move_is_valid = False
        while move_is_valid is False:
            mouse_coordinates = game_window.getMouse()
            if determine_the_winner() != "no winner":
                self.skipped_turns = 0
                show_finished_game_message(game_window, determine_the_winner().capitalize() + " wins!")
            if self.skipped_turns < 2 and determine_the_winner() == "no winner":
                if fun.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y,
                                        consts.X_AXYS_BACK_TO_MENU - consts.X_AXYS_OFFSET,
                                        consts.Y_AXYS_BACK_TO_MENU - consts.Y_AXYS_OFFSET,
                                        consts.X_AXYS_BACK_TO_MENU + consts.X_AXYS_OFFSET,
                                        consts.Y_AXYS_BACK_TO_MENU + consts.Y_AXYS_OFFSET):
                    return True, "Menu"
                elif fun.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y,
                                          consts.X_AXYS_SKIP_TURN - consts.X_AXYS_OFFSET,
                                          consts.Y_AXYS_SKIP_TURN - consts.Y_AXYS_OFFSET,
                                          consts.X_AXYS_SKIP_TURN + consts.X_AXYS_OFFSET,
                                          consts.Y_AXYS_SKIP_TURN + consts.Y_AXYS_OFFSET):
                    return self.player_clicked_skip_turn(game_window)
                else:
                    for i in range(consts.BOARD_MATRIX_LINE_SIZE):
                        for j in range(consts.BOARD_MATRIX_COLUMN_SIZE):
                            if check_inside_piece_spot(i, j, mouse_coordinates.x, mouse_coordinates.y) is True:
                                return self.player_placed_a_piece_on_board(i, j, player_turn, game_window)
            else:
                if fun.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y, consts.X1_AXYS_BACK_TO_MENU_OVER,
                                        consts.Y1_AXYS_BACK_TO_MENU_OVER, consts.X2_AXYS_BACK_TO_MENU_OVER,
                                        consts.Y2_AXYS_BACK_TO_MENU_OVER):
                    self.skipped_turns = 0
                    return True, "Menu"
        return True, "Game"

    def perform_CPU_moves(self, game_window):
        """
        This method takes care of CPU's random strategy
        :param game_window: the window where the CPU places the piece
        :return: the state after the CPU made his move
        """
        self.skipped_turns = 0
        move_is_valid = False
        while move_is_valid is False:
            CPU_move = random.randint(0, consts.BOARD_MATRIX_LINE_SIZE * consts.BOARD_MATRIX_COLUMN_SIZE - 1)
            line = CPU_move % consts.BOARD_MATRIX_LINE_SIZE
            column = CPU_move // consts.BOARD_MATRIX_COLUMN_SIZE
            if intersection_is_empty(column, line):
                piece = Circle(Point(consts.BOARD_MARGIN + line * consts.CELL_DIMENSION,
                                     consts.BOARD_MARGIN + column * consts.CELL_DIMENSION), consts.PIECE_RADIUS)

                piece.setFill('white')
                piece.draw(game_window)
                self.perform_backend_side(game_window, column, line, 'white')
                self.update_players_scores(game_window)
                return True, "Game"

    def player_clicked_skip_turn(self, game_window):
        """
        This method checks if the consecutive skipped turns are maximum 1 and handles the situation
        :param game_window: the window the message will appear
        :return: the state depending on the number of consecutive skipped turns(including this one)
        """
        if self.skipped_turns != 1:
            self.skipped_turns = 1
        elif self.skipped_turns == 1:
            self.skipped_turns += 1
        if self.skipped_turns == 2:
            show_finished_game_message(game_window, 'Draw')
            return True, "Game"
        return True, "PutPiece"

    def player_placed_a_piece_on_board(self, i, j, player_turn, game_window):
        """
        This method puts a piece on the board if the intersection is not occupied
        :param i: the line in the board matrix
        :param j: the column in the board matrix
        :param player_turn:
        :param game_window:
        :return: the state depending on the place the player clicked
        """
        if intersection_is_empty(j, i) is True:
            self.skipped_turns = 0
            piece = Circle(
                Point(consts.BOARD_MARGIN + i * consts.CELL_DIMENSION, consts.BOARD_MARGIN + j * consts.CELL_DIMENSION),
                consts.PIECE_RADIUS)
            piece.setFill(player_turn)
            piece.draw(game_window)
            self.perform_backend_side(game_window, j, i, player_turn)
            self.update_players_scores(game_window)
            return True, "PutPiece"
        else:
            return True, "Game"

    def update_players_scores(self, game_window):
        """
         This method makes sure the player scores are updated in real time
        :param game_window: the window when the scores will be updated
        :return:
        """
        fun.clear_part_window(game_window, consts.X1_AXYS_WHITE_SCORE, consts.Y1_AXYS_WHITE_SCORE,
                              consts.X2_AXYS_WHITE_SCORE, consts.Y2_AXYS_WHITE_SCORE)

        fun.clear_part_window(game_window, consts.X1_AXYS_BLACK_SCORE, consts.Y1_AXYS_BLACK_SCORE,
                              consts.X2_AXYS_BLACK_SCORE, consts.Y2_AXYS_BLACK_SCORE)

        fun.draw_small_text_box(game_window, str(self.white_score), consts.X_AXYS_WHITE_SCORE,
                                consts.Y_AXYS_WHITE_SCORE)
        fun.draw_small_text_box(game_window, str(self.black_score), consts.X_AXYS_BLACK_SCORE,
                                consts.Y_AXYS_BLACK_SCORE)

    def perform_backend_side(self, game_window, i, j, player_turn):
        """
        This method does the main tasks in the app's logic, puts the pieces on the matrix, eliminate those pieces
        that are surrounded and at the end marks them with a red line on the screen
        :param game_window: the window the piece will be drawn on, along with the scores and red lines
        :param i: the line in the board matrix
        :param j: the column in the board matrix
        :param player_turn: the player that placed the piece on board
        :return:
        """
        (self.white_score, self.black_score) = add_piece_on_matrix(i, j, player_turn, self.white_score,
                                                                   self.black_score)
        (self.white_score, self.black_score) = get_scores_depending_on_trapped_pieces()
        cross_trapped_pieces(game_window)


def draw_game_window(game_window):
    """
    This function handles all the clicked buttons on the game window, and returns a tuple which consist in a boolean
    that says weather to continue the game or not, to go to menu or a piece was placed, etc...
    :param game_window: the window where this items will be drown
    :return:
    """
    reset_the_board()
    fun.clear_window(game_window)
    for i in range(0, consts.BOARD_MATRIX_LINE_SIZE - 1):
        for j in range(0, consts.BOARD_MATRIX_COLUMN_SIZE - 1):
            cell = Rectangle(Point(consts.BOARD_MARGIN + i * consts.CELL_DIMENSION,
                                   consts.BOARD_MARGIN + j * consts.CELL_DIMENSION),
                             Point(consts.BOARD_MARGIN + (i + 1) * consts.CELL_DIMENSION,
                                   consts.BOARD_MARGIN + (j + 1) * consts.CELL_DIMENSION))
            cell.setOutline(color_rgb(109, 61, 20))
            cell.draw(game_window)
    fun.draw_simple_text(game_window, "Player's Turn", consts.X_AXYS_PLAYER_TURN, consts.Y_AXYS_PLAYER_TURN, 30)
    fun.draw_simple_text(game_window, "Scoreboard", consts.X_AXYS_SCORE, consts.Y_AXYS_SCORE, 30)
    fun.draw_simple_text(game_window, "White", consts.X_AXYS_WHITE, consts.Y_AXYS_WHITE, 30)
    fun.draw_simple_text(game_window, "Black", consts.X_AXYS_BLACK, consts.Y_AXYS_BLACK, 30)
    fun.draw_big_text_box(game_window, "Skip move", consts.X_AXYS_SKIP_TURN, consts.Y_AXYS_SKIP_TURN)
    fun.draw_big_text_box(game_window, "Back to menu", consts.X_AXYS_BACK_TO_MENU, consts.Y_AXYS_BACK_TO_MENU)
    fun.draw_small_text_box(game_window, 0, consts.X_AXYS_WHITE_SCORE, consts.Y_AXYS_WHITE_SCORE)
    fun.draw_small_text_box(game_window, 0, consts.X_AXYS_BLACK_SCORE, consts.Y_AXYS_BLACK_SCORE)


def reset_the_board():
    """
    This function will remove all the pieces from the board and resets it
    :return:
    """
    global game_board
    game_board = []
    for i in range(consts.BOARD_MATRIX_LINE_SIZE):
        row = []
        for j in range(consts.BOARD_MATRIX_COLUMN_SIZE):
            row.append(0)
        game_board.append(row)


def check_inside_piece_spot(i, j, mouse_x, mouse_y):
    """
    This function checks and returns true if the player clicked on an intersection of the game board
    :param i: the line in the board matrix
    :param j: the column in the board matrix
    :param mouse_x: x coordinate of the mouse position
    :param mouse_y: y coordinate of the mouse position
    :return: True if the the player clicked on the intersection, False otherwise
    """
    return fun.mouse_inside_box(mouse_x, mouse_y,
                                consts.BOARD_MARGIN + i * consts.CELL_DIMENSION - consts.PIECE_RADIUS,
                                consts.BOARD_MARGIN + j * consts.CELL_DIMENSION - consts.PIECE_RADIUS,
                                consts.BOARD_MARGIN + i * consts.CELL_DIMENSION + consts.PIECE_RADIUS,
                                consts.BOARD_MARGIN + j * consts.CELL_DIMENSION + consts.PIECE_RADIUS)


def intersection_is_empty(x, y):
    """
    This function checks if the intersection wanted to put a piece on it is already occupied
    :param x: piece coordinate x
    :param y: piece coordinate y
    :return: True if the intersection is empty, False otherwise
    """
    global game_board
    if game_board[x][y] == 0:
        return True
    return False


def determine_the_winner():
    """
    This function determines the winner of the game based on points accumulated by each player and the remaining
    possible points
    :return: a string consisting in winner player or a message if the game is not over yet
    """
    global game_board
    remaining_points = 0
    white_points = black_points = 0
    for i in range(consts.BOARD_MATRIX_LINE_SIZE):
        for j in range(consts.BOARD_MATRIX_COLUMN_SIZE):
            if game_board[i][j] == 0:
                remaining_points += 1
            elif game_board[i][j] == 1:
                white_points += 1
            else:
                black_points += 1
    if white_points > remaining_points + black_points:
        return "white"
    elif black_points > remaining_points + white_points:
        return "black"
    return "no winner"


def add_piece_on_matrix(x, y, player_turn, white_score, black_score):
    """
    This function adds a piece in the matrix behind the graphical board and returns the updated score
    :param x: piece coordinate x
    :param y: piece coordinate y
    :param player_turn: the player that placed the piece
    :param white_score: the current score of the white player
    :param black_score: the current score of the black player
    :return: a tuple containing the players scores
    """
    global game_board
    if player_turn == 'white':
        game_board[x][y] = 1
        white_score += 1
    else:
        game_board[x][y] = 2
        black_score += 1
    return white_score, black_score


def cross_trapped_pieces(game_window):
    """
    This function is drawing a red line on the trapped pieces on the game board
    :param game_window: the window the line will appear on
    :return:
    """
    global aux_game_board
    for i in range(consts.BOARD_MATRIX_LINE_SIZE):
        for j in range(consts.BOARD_MATRIX_COLUMN_SIZE):
            if aux_game_board[i][j] == -3:
                redLine = Line(
                    Point(consts.RED_LINE_START_COORDINATE + j * consts.RED_LINE_END_COORDINATE,
                          consts.RED_LINE_START_COORDINATE + i * consts.RED_LINE_END_COORDINATE),
                    Point(consts.RED_LINE_START_COORDINATE + (j + 1) * consts.RED_LINE_END_COORDINATE,
                          consts.RED_LINE_START_COORDINATE + (i + 1) * consts.RED_LINE_END_COORDINATE))
                redLine.setFill('red')
                redLine.draw(game_window)


def get_scores_depending_on_trapped_pieces():
    """
    This function checks if a piece is free and if not, marks it on the board matrix and updates the scores according
    to the situation
    :return: a tuple containing the players scores
    """
    global game_board
    global aux_game_board
    aux_game_board = game_board
    white_score = black_score = 0
    for i in range(consts.BOARD_MATRIX_LINE_SIZE):
        for j in range(consts.BOARD_MATRIX_COLUMN_SIZE):
            if aux_game_board[i][j] == 1 or aux_game_board[i][j] == 2:
                if not check_for_liberty(i, j):
                    mark_trapped_pieces_on_matrix(i, j, -3)
    for i in range(consts.BOARD_MATRIX_LINE_SIZE):
        for j in range(consts.BOARD_MATRIX_COLUMN_SIZE):
            if aux_game_board[i][j] == -1:
                game_board[i][j] = 1
                white_score += 1
            elif aux_game_board[i][j] == -2:
                game_board[i][j] = 2
                black_score += 1
    return white_score, black_score


def show_finished_game_message(game_window, message):
    """
    This function will draw a message with the winner of the game(or if it's a draw) and a button with the option
    to return to the main menu
    :param game_window: the window the message will appear on
    :param message: the message to appear on window
    :return:
    """
    fun.clear_part_window(game_window, consts.X1_AXYS_GAME_OVER_MSG, consts.Y1_AXYS_GAME_OVER_MSG,
                          consts.X2_AXYS_GAME_OVER_MSG, consts.Y2_AXYS_GAME_OVER_MSG)
    fun.draw_simple_text(game_window, message, consts.X_AXYS_FINISHED_MESSAGE, consts.Y_AXYS_FINISHED_MESSAGE, 30)
    fun.draw_big_text_box(game_window, "Back to menu", consts.X_AXYS_BACK_TO_MENU_OVER,
                          consts.Y_AXYS_BACK_TO_MENU_OVER)


def check_for_liberty(x, y):
    """
    This function checks if the piece from the (x, y) position has liberty (if the pieces from North, East, West
    and North are all of the other's player color)
    :param x: piece coordinate x
    :param y: piece coordinate y
    :return: True if the piece has liberty, False otherwise
    """
    global queue
    piece_is_free = False
    player = aux_game_board[x][y]
    queue.append([x, y])
    while len(queue) > 0:
        current_position = queue.pop(0)
        new_position = current_position
        for i in range(0, 4):
            new_position[0] += consts.LINE_SHIFT[i]
            new_position[1] += consts.COLUMN_SHIFT[i]
            if 0 <= new_position[0] <= consts.BOARD_MATRIX_LINE_SIZE - 1 \
                    and 0 <= new_position[1] <= consts.BOARD_MATRIX_COLUMN_SIZE - 1:
                if aux_game_board[new_position[0]][new_position[1]] == player:
                    queue.append([new_position[0], new_position[1]])
                if aux_game_board[new_position[0]][new_position[1]] == 0:
                    piece_is_free = True
            new_position[0] -= consts.LINE_SHIFT[i]
            new_position[1] -= consts.COLUMN_SHIFT[i]
        aux_game_board[new_position[0]][new_position[1]] = -player
    return piece_is_free


def mark_trapped_pieces_on_matrix(x, y, trapped_value):
    """
    This function marks (with -3) the trapped pieces on the matrix of the game board
    :param x: piece coordinate x
    :param y: piece coordinate y
    :param trapped_value: the value to be inserted in the matrix
    :return
    """
    player = aux_game_board[x][y]
    queue.append([x, y])
    while len(queue) > 0:
        current_position = queue.pop(0)
        new_position = current_position
        for i in range(0, 4):
            new_position[0] += consts.LINE_SHIFT[i]
            new_position[1] += consts.COLUMN_SHIFT[i]
            if 0 <= new_position[0] <= consts.BOARD_MATRIX_LINE_SIZE - 1 \
                    and 0 <= new_position[1] <= consts.BOARD_MATRIX_COLUMN_SIZE - 1:
                if aux_game_board[new_position[0]][new_position[1]] == player:
                    queue.append([new_position[0], new_position[1]])
            new_position[0] -= consts.LINE_SHIFT[i]
            new_position[1] -= consts.COLUMN_SHIFT[i]
        aux_game_board[new_position[0]][new_position[1]] = trapped_value


def initialize_game_window():
    """
    This function is used to initialize the game window, with the constant sizes defined in the constants file
    :return:
    """
    global window
    window = GraphWin("Game of Go", consts.WINDOW_LENGTH, consts.WINDOW_WIDTH)


def begin_the_game():
    """
    This function takes care of the game flow from the start to the end of it
    :return:
    """
    global window, turn, actual_game_started
    game_running = True
    current_action = "Menu"
    game_manager = Game()

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
                draw_game_window(window)
                actual_game_started = True

            piece = Circle(Point(810, 200), 20)
            piece.setFill(turn)
            piece.draw(window)

            if game_manager.player_type == 'Human':
                (game_running, current_action) = game_manager.game_buttons_actions(window, turn)

                if current_action == 'PutPiece':
                    current_action = 'Game'
                    if turn == 'white':
                        turn = 'black'
                    else:
                        turn = 'white'
            else:
                (game_running, current_action) = game_manager.game_buttons_actions(window, turn)
                if current_action == 'PutPiece':
                    current_action = 'Game'
                game_manager.perform_CPU_moves(window)

    window.close()


def start_the_application():
    """
    This function is responsabile to the application start
    :return:
    """
    initialize_game_window()
    begin_the_game()


if __name__ == '__main__':
    start_the_application()
