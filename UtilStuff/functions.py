from graphics import Text, Point, Rectangle
from UtilStuff import constants as consts


def clear_window(window):
    """
    This function is used to delete the elements from the entire screen and clear the game window
    :param window: the window that will be cleared
    :return:
    """
    reset = Rectangle(Point(0, 0), Point(consts.WINDOW_LENGTH, consts.WINDOW_WIDTH))
    reset.setFill(consts.GAME_COLOR)
    reset.draw(window)


def mouse_inside_box(x_axis_mouse, y_axis_mouse, x_axis_box1, y_axis_box1, x_axis_box2, y_axis_box2):
    """
    This function is used to check if the mouse coordinates are inside a box when a click action happens
    :param x_axis_mouse: the x coordinate of mouse position
    :param y_axis_mouse: the y coordinate of mouse position
    :param x_axis_box1: the x coordinate of the lower left corner of the box
    :param y_axis_box1: the y coordinate of the lower left corner of the box
    :param x_axis_box2: the x coordinate of the upper right corner of the box
    :param y_axis_box2: the y coordinate of the upper right corner of the box
    :return: True if the mouse is inside the box created with given coordinates, False otherwise
    """
    if x_axis_box1 <= x_axis_mouse <= x_axis_box2:
        if y_axis_box1 <= y_axis_mouse <= y_axis_box2:
            return True
    return False


def clear_part_window(window, x1_axis, y1_axis, x2_axis, y2_axis):
    """
    This function is used to delete the elements from a part of the screen and clear that part (will be used for
    score updates in real time)
    :param window: the window that will be cleared
    :param x1_axis: the x coordinate of the lower left corner of the area to be cleared
    :param y1_axis: the y coordinate of the lower left corner of the area to be cleared
    :param x2_axis: the x coordinate of the upper right corner of the area to be cleared
    :param y2_axis: the y coordinate of the upper right corner of the area to be cleared
    :return:
    """
    reset = Rectangle(Point(x1_axis, y1_axis), Point(x2_axis, y2_axis))
    reset.setFill(consts.GAME_COLOR)
    reset.draw(window)


def draw_simple_text(window, text, x_axis, y_axis, font_size):
    """
    This function is used to draw the "text" in the given "window" at the position given by "x_axis" and "b_axis"
    parameters
    :param window: the window where the simple text will be drawn
    :param text: the actual text content
    :param x_axis: x coordinate of the position of the text
    :param y_axis: y coordinate of the position of the text
    :param font_size: the text size
    :return:
    """
    content = Text(Point(x_axis, y_axis), text)
    content.setTextColor('white')
    content.setSize(font_size)
    content.setFace('arial')
    content.draw(window)


def draw_big_text_box(window, text, x_axis, y_axis):
    """
    This function is used to draw a big rectangle containing the "text", using "draw_simple_text" method from above
    :param window: the window where the big text box be drawn
    :param text: the actual text content
    :param x_axis: x coordinate of the position of the box
    :param y_axis: y coordinate of the position of the box
    :return:
    """
    big_re = Rectangle(Point(x_axis - consts.X_AXYS_OFFSET, y_axis - consts.Y_AXYS_OFFSET),
                       Point(x_axis + consts.X_AXYS_OFFSET, y_axis + consts.Y_AXYS_OFFSET))
    big_re.setOutline('white')
    big_re.draw(window)
    draw_simple_text(window, text, x_axis, y_axis, 20)


def draw_small_text_box(window, text, x_axis, y_axis):
    """
    This function is used to draw a small rectangle containing the "text", using "draw_simple_text" method from
    above
    :param window: the window where the small text box be drawn
    :param text: the actual text content
    :param x_axis: x coordinate of the position of the box
    :param y_axis: y coordinate of the position of the box
    :return:
    """
    small_re = Rectangle(Point(x_axis - 30, y_axis - consts.Y_AXYS_OFFSET),
                         Point(x_axis + 30, y_axis + consts.Y_AXYS_OFFSET))
    small_re.setOutline('white')
    small_re.draw(window)
    draw_simple_text(window, text, x_axis, y_axis, 20)
