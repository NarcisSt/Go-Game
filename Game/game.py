from graphics import *
from UtilFunctions import functions as util
from Game import gameLogic as gameLogic
import random


class GameManager:
    def __init__(self):
        self.playerType = 'computer'
        self.countPassed = 0
        self.cell_pixel_dimension = 30
        self.offset_board = 50
        self.imageX = 850
        self.imageY = 600
        self.backToMenuX = 150
        self.backToMenuY = 650
        self.toMoveX = 810
        self.toMoveY = 150
        self.passX = 490
        self.passY = 650
        self.scoreX = 810
        self.scoreY = 300
        self.whiteX = 685
        self.whiteY = 360
        self.blackX = 935
        self.blackY = 360
        self.scoreWhiteX = 685
        self.scoreWhiteY = 420
        self.scoreBlackX = 935
        self.scoreBlackY = 420
        self.offsetX = 100
        self.offsetY = 20

    def draw_game(self, window):
        self.score_white = 0
        self.score_black = 0
        gameLogic.reset_board()
        util.reset_screen(window)
        for i in range(0, 18):
            for j in range(0, 18):
                cell = Rectangle(Point(self.offset_board + i * self.cell_pixel_dimension,
                                       self.offset_board + j * self.cell_pixel_dimension),
                                 Point(self.offset_board + (i + 1) * self.cell_pixel_dimension,
                                       self.offset_board + (j + 1) * self.cell_pixel_dimension))
                cell.setOutline(color_rgb(15, 18, 14))
                cell.draw(window)
        util.draw_image(window, "../Images/GoTable.png", self.imageX, self.imageY)
        util.draw_bordered_text(window, "Back to menu", self.backToMenuX, self.backToMenuY)
        util.draw_un_bordered_text(window, "Player to move", self.toMoveX, self.toMoveY)
        util.draw_bordered_text(window, "Pass turn", self.passX, self.passY)
        util.draw_un_bordered_text(window, "Score", self.scoreX, self.scoreY)
        util.draw_un_bordered_text(window, "White", self.whiteX, self.whiteY)
        util.draw_un_bordered_text(window, "Black", self.blackX, self.blackY)
        util.draw_small_bordered_text(window, str(self.score_white), self.scoreWhiteX, self.scoreWhiteY)
        util.draw_small_bordered_text(window, str(self.score_black), self.scoreBlackX, self.scoreBlackY)

    def handle_mouse_click_game(self, window, turn):
        valid_move_flag = False
        while not valid_move_flag:
            mouse_data = window.getMouse()
            if util.check_inside(mouse_data.x, mouse_data.y, self.backToMenuX - self.offsetX,
                                 self.backToMenuY - self.offsetY, self.backToMenuX + self.offsetX,
                                 self.backToMenuY + self.offsetY):
                return (True, "Home")
            elif util.check_inside(mouse_data.x, mouse_data.y, self.passX - self.offsetX, self.passY - self.offsetY,
                                   self.passX + self.offsetX, self.passY + self.offsetY):
                if self.countPassed != 1:
                    self.countPassed = 1
                elif self.countPassed == 1:
                    self.countPassed += 1
                if self.countPassed == 2:
                    return (True, "Home")
                else:
                    return (True, "PutPiece")
            else:
                for i in range(0, 19):
                    for j in range(0, 19):
                        if util.check_inside(mouse_data.x, mouse_data.y,
                                             self.offset_board + i * self.cell_pixel_dimension - 10,
                                             self.offset_board + j * self.cell_pixel_dimension - 10,
                                             self.offset_board + i * self.cell_pixel_dimension + 10,
                                             self.offset_board + j * self.cell_pixel_dimension + 10):
                            if gameLogic.check_valid_position(j, i):
                                self.countPassed = 0
                                piece = Circle(Point(self.offset_board + i * self.cell_pixel_dimension,
                                                     self.offset_board + j * self.cell_pixel_dimension), 10)
                                piece.setFill(turn)
                                piece.draw(window)
                                self.perform_game_logic(window, j, i, turn)
                                util.reset_part_screen(window, self.scoreWhiteX - 29, self.scoreWhiteY - 19,
                                                       self.scoreWhiteX + 29, self.scoreWhiteY + 19)
                                util.reset_part_screen(window, self.scoreBlackX - 29, self.scoreBlackY - 19,
                                                       self.scoreBlackX + 29, self.scoreBlackY + 19)
                                util.draw_small_bordered_text(window, str(self.score_white), self.scoreWhiteX,
                                                              self.scoreWhiteY)
                                util.draw_small_bordered_text(window, str(self.score_black), self.scoreBlackX,
                                                              self.scoreBlackY)
                                return (True, "PutPiece")
                            else:
                                valid_move_flag = False

        return (True, "Game")

    def make_random_move(self, window):
        self.countPassed = 0
        valid_move_flag = False
        while not valid_move_flag:
            random_move = random.randint(0, 19 * 19 - 1)
            line = random_move % 19
            col = random_move // 19
            if gameLogic.check_valid_position(col, line):
                valid_move_flag = True
                piece = Circle(Point(self.offset_board + line * self.cell_pixel_dimension,
                                     self.offset_board + col * self.cell_pixel_dimension), 10)
                piece.setFill('white')
                piece.draw(window)
                self.perform_game_logic(window, col, line, 'white')
                util.reset_part_screen(window, self.scoreWhiteX - 29, self.scoreWhiteY - 19,
                                       self.scoreWhiteX + 29, self.scoreWhiteY + 19)
                util.reset_part_screen(window, self.scoreBlackX - 29, self.scoreBlackY - 19,
                                       self.scoreBlackX + 29, self.scoreBlackY + 19)
                util.draw_small_bordered_text(window, str(self.score_white), self.scoreWhiteX, self.scoreWhiteY)
                util.draw_small_bordered_text(window, str(self.score_black), self.scoreBlackX, self.scoreBlackY)
                return (True, "Game")

    def perform_game_logic(self, window, i, j, turn):
        (self.score_white, self.score_black) = gameLogic.add_piece(i, j, turn, self.score_white, self.score_black)
        (self.score_white, self.score_black) = gameLogic.eliminate_surrounded_pieces(self.score_white, self.score_black)
        gameLogic.mark_eliminated_pieces(window)

    def set_player_type(self, player_type):
        self.playerType = player_type
        if self.playerType != 'computer' and self.playerType != 'player':
            self.playerType = 'computer'

    def get_player_type(self):
        return self.playerType
