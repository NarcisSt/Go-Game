from UtilFunctions import functions as utils

"""Constants containing coordinates for drawing items on window"""
X_AXIS_TITLE = 500
Y_AXIS_TITLE = 60
X_AXIS_START = 500
Y_AXIS_START = 200
X_AXIS_EXIT = 500
Y_AXIS_EXIT = 280
X_AXIS_CPU = 800
Y_AXIS_CPU = 200
X_AXIS_PLAYER = 200
Y_AXIS_PLAYER = 200
X_AXIS_OFFSET = 100
Y_AXIS_OFFSET = 20

"""This methods is used to draw the main menu of the game which contain the title, and two buttons(Play or Exit)"""


def draw_main_menu(window):
    utils.clear_window(window)
    utils.draw_simple_text(window, "Go Game", X_AXIS_TITLE, Y_AXIS_TITLE, 35)
    utils.draw_big_text_box(window, "Play", X_AXIS_START, Y_AXIS_START)
    utils.draw_big_text_box(window, "Exit", X_AXIS_EXIT, Y_AXIS_EXIT)


"""This method handles all the clicked buttons on the main menu, and returns a tuple which consist in a boolean
    that says weather to continue the game or not, and the future state of tha app"""


def menu_buttons_actions(window):
    PLAY_BUTTON_PRESSED = False
    mouse_coordinates = window.getMouse()
    if utils.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y,
                              X_AXIS_START - X_AXIS_OFFSET, Y_AXIS_START - Y_AXIS_OFFSET,
                              X_AXIS_START + X_AXIS_OFFSET, Y_AXIS_START + Y_AXIS_OFFSET):
        if not PLAY_BUTTON_PRESSED:
            utils.draw_big_text_box(window, "Against CPU", X_AXIS_CPU, Y_AXIS_CPU)
            utils.draw_big_text_box(window, "Player 2", X_AXIS_PLAYER, Y_AXIS_PLAYER)
            return True, "Play"
        else:
            return True, "Menu"
    if utils.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y, X_AXIS_EXIT - X_AXIS_OFFSET,
                              Y_AXIS_EXIT - Y_AXIS_OFFSET, X_AXIS_EXIT + X_AXIS_OFFSET,
                              Y_AXIS_EXIT + Y_AXIS_OFFSET):
        return False, "Menu"
    if utils.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y, X_AXIS_CPU - X_AXIS_OFFSET,
                              Y_AXIS_CPU - Y_AXIS_OFFSET, X_AXIS_CPU + X_AXIS_OFFSET,
                              Y_AXIS_CPU + Y_AXIS_OFFSET):
        return True, "CPU"
    if utils.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y, X_AXIS_PLAYER - X_AXIS_OFFSET,
                              Y_AXIS_PLAYER - Y_AXIS_OFFSET, X_AXIS_PLAYER + X_AXIS_OFFSET,
                              Y_AXIS_PLAYER + Y_AXIS_OFFSET):
        return True, "Player 2"
    else:
        return True, "Menu"
