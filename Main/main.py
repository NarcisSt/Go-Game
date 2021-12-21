from graphics import *
from Home import home
from Game import game
from Game import gameLogic as gameLogic


def adjust_window(length, width):
    global window
    window = GraphWin("Go Game", length, width)


def start_game():
    global window
    game_run_flag = True
    game_state = "Home"
    home_manager = home.HomeManager()
    game_manager = game.GameManager()

    while game_run_flag:
        if game_state == "Home":
            game_drawn_flag = False
            home_manager.draw_home(window)
            (game_run_flag, game_state) = home_manager.handle_mouse_click_home(window)
        elif game_state == "Pressed play":
            game_drawn_flag = False
            (game_run_flag, game_state) = home_manager.handle_mouse_click_home(window)
        elif game_state == "Pressed computer":
            game_manager.set_player_type('computer')
            game_state = "Game"
        elif game_state == "Pressed player":
            game_manager.set_player_type('player')
            game_state = "Game"
        elif game_state == "Game":
            if not game_drawn_flag:
                turn = 'black'
                game_manager.draw_game(window)
                game_drawn_flag = True

            piece = Circle(Point(810, 200), 20)
            piece.setFill(turn)
            piece.draw(window)
            if game_manager.playerType == "player":
                (game_run_flag, game_state) = game_manager.handle_mouse_click_game(window, turn)

                if game_state == "PutPiece":
                    game_state = "Game"
                    if turn == 'white':
                        turn = 'black'
                    else:
                        turn = 'white'
            else:
                (game_run_flag, game_state) = game_manager.handle_mouse_click_game(window, turn)
                if game_state == "PutPiece":
                    game_state = 'Game'
                game_manager.make_random_move(window)

            if gameLogic.get_pieces_count() == 19 * 19:
                game_state = "Home"

    window.close()


adjust_window(1000, 700)
start_game()
