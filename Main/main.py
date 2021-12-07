from graphics import *
from Home import home
from Game import game


def adjust_window(length, width):
    global window
    window = GraphWin("Go Game", length, width)


def start_game():
    global window
    game_run_flag = True
    game_state = "Home"

    while game_run_flag:
        if game_state == "Home":
            game_drawn_flag = False
            home.draw_home(window)
            (game_run_flag, game_state) = home.handle_mouse_click_home(window)
        elif game_state == "Game":
            if not game_drawn_flag:
                turn = 'black'
                game.draw_game(window)
                game_drawn_flag = True

            piece = Circle(Point(810, 200), 20)
            piece.setFill(turn)
            piece.draw(window)
            (game_run_flag, game_state) = game.handle_mouse_click_game(window, turn)

            if game_state == "PutPiece":
                game_state = "Game"
                if turn == "white":
                    turn = "black"
                else:
                    turn = "white"

    window.close()


adjust_window(1000, 700)
start_game()
