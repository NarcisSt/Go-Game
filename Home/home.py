from UtilFunctions import functions as util


def handle_mouse_click_home(window):
    mouse_data = window.getMouse()
    if util.check_inside(mouse_data.x, mouse_data.y, 400, 180, 600, 220):
        return True, 'Game'
    elif util.check_inside(mouse_data.x, mouse_data.y, 400, 260, 600, 300):
        return False, 'Home'
    return True, 'Home'


def draw_home(window):
    util.reset_screen(window)
    util.draw_un_bordered_text(window, "Go Game", 500, 60)
    util.draw_bordered_text(window, "Play", 500, 200)
    util.draw_bordered_text(window, "Quit", 500, 280)
    util.draw_image(window, "../Images/GoTable.png", 860, 600)
