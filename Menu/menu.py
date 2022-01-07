from UtilStuff import functions as fun
from UtilStuff import constants as consts


def draw_main_menu(window):
    """
    This function is used to draw the main menu of the game which contain the title, and two buttons(Play or Exit)
    :param window: the window where the main menu will be drown on
    :return:
    """
    fun.clear_window(window)
    fun.draw_simple_text(window, "Game of Go", consts.X_AXYS_TITLE, consts.Y_AXYS_TITLE, 35)
    fun.draw_big_text_box(window, "Play", consts.X_AXYS_START, consts.Y_AXYS_START)
    fun.draw_big_text_box(window, "Exit", consts.X_AXYS_EXIT, consts.Y_AXYS_EXIT)


def menu_buttons_actions(window):
    """
    This function handles all the clicked buttons on the main menu, and returns a tuple which consist in a boolean
    that says weather to continue the game or not, and the future state of tha app
    :param window: the window all the action happens
    :return: a tuple consisting in (will the game continue?, in which state?), based on what button the player is
    clicking
    """
    PLAY_BUTTON_PRESSED = False
    mouse_coordinates = window.getMouse()
    if fun.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y,
                            consts.X_AXYS_START - consts.X_AXYS_OFFSET, consts.Y_AXYS_START - consts.Y_AXYS_OFFSET,
                            consts.X_AXYS_START + consts.X_AXYS_OFFSET, consts.Y_AXYS_START + consts.Y_AXYS_OFFSET):
        if not PLAY_BUTTON_PRESSED:
            fun.draw_big_text_box(window, "Against CPU", consts.X_AXYS_CPU, consts.Y_AXYS_CPU)
            fun.draw_big_text_box(window, "Player 2", consts.X_AXYS_PLAYER, consts.Y_AXYS_PLAYER)
            return True, "Play"
        else:
            return True, "Menu"
    if fun.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y, consts.X_AXYS_EXIT - consts.X_AXYS_OFFSET,
                            consts.Y_AXYS_EXIT - consts.Y_AXYS_OFFSET, consts.X_AXYS_EXIT + consts.X_AXYS_OFFSET,
                            consts.Y_AXYS_EXIT + consts.Y_AXYS_OFFSET):
        return False, "Menu"
    if fun.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y, consts.X_AXYS_CPU - consts.X_AXYS_OFFSET,
                            consts.Y_AXYS_CPU - consts.Y_AXYS_OFFSET, consts.X_AXYS_CPU + consts.X_AXYS_OFFSET,
                            consts.Y_AXYS_CPU + consts.Y_AXYS_OFFSET):
        return True, "CPU"
    if fun.mouse_inside_box(mouse_coordinates.x, mouse_coordinates.y, consts.X_AXYS_PLAYER - consts.X_AXYS_OFFSET,
                            consts.Y_AXYS_PLAYER - consts.Y_AXYS_OFFSET, consts.X_AXYS_PLAYER + consts.X_AXYS_OFFSET,
                            consts.Y_AXYS_PLAYER + consts.Y_AXYS_OFFSET):
        return True, "Player 2"
    else:
        return True, "Menu"
