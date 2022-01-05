from graphics import Text, Point, Rectangle, color_rgb

"""This method is used to delete the elements from the entire screen and clear the game window"""


def clear_window(window):
    reset = Rectangle(Point(0, 0), Point(1000, 700))
    reset.setFill(color_rgb(37, 60, 120))
    reset.draw(window)


"""This method is used to delete the elements from a part of the screen and clear that part (will be used for 
    score updates in real time)"""


def clear_part_window(window, x1_axis, y1_axis, x2_axis, y2_axis):
    reset = Rectangle(Point(x1_axis, y1_axis), Point(x2_axis, y2_axis))
    reset.setFill(color_rgb(37, 60, 120))
    reset.draw(window)


"""This method is used to draw the "text" in the given "window" at the position given by "x_axis" and "b_axis"
    parameters """


def draw_simple_text(window, text, x_axis, y_axis, font_size):
    content = Text(Point(x_axis, y_axis), text)
    content.setTextColor('white')
    content.setSize(font_size)
    content.setFace('helvetica')
    content.draw(window)


"""This method is used to draw a big rectangle containing the "text", using "draw_simple_text" method from above"""


def draw_big_text_box(window, text, x_axis, y_axis):
    big_re = Rectangle(Point(x_axis - 100, y_axis - 20), Point(x_axis + 100, y_axis + 20))
    big_re.setOutline('white')
    big_re.draw(window)
    draw_simple_text(window, text, x_axis, y_axis, 20)


"""This method is used to draw a small rectangle containing the "text", using "draw_simple_text" method from above"""


def draw_small_text_box(window, text, x_axis, y_axis):
    small_re = Rectangle(Point(x_axis - 30, y_axis - 20), Point(x_axis + 30, y_axis + 20))
    small_re.setOutline('white')
    small_re.draw(window)
    draw_simple_text(window, text, x_axis, y_axis, 20)


"""This method is used to check if the mouse coordinates are inside a box when a click action happens"""


def mouse_inside_box(x_axis_mouse, y_axis_mouse, x_axis_box1, y_axis_box1, x_axis_box2, y_axis_box2):
    if x_axis_box1 <= x_axis_mouse <= x_axis_box2:
        if y_axis_box1 <= y_axis_mouse <= y_axis_box2:
            return True
    return False
