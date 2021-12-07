from graphics import *


def check_inside(x_click, y_click, x_box, y_box, x_box2, y_box2):
    if x_box <= x_click <= x_box2:
        if y_box <= y_click <= y_box2:
            return True
    return False


def reset_screen(window):
    reset_blue = Rectangle(Point(0, 0), Point(1000, 700))
    reset_blue.setFill(color_rgb(0, 100, 0))
    reset_blue.draw(window)


def draw_un_bordered_text(window, text, x, y):
    text_box = Text(Point(x, y), text)
    text_box.setTextColor("white")
    text_box.setSize(35)
    text_box.setFace("helvetica")
    text_box.draw(window)


def draw_bordered_text(window, text, x, y):
    text_border = Rectangle(Point(x - 100, y - 20), Point(x + 100, y + 20))
    text_border.setOutline(color_rgb(87, 239, 23))
    text_border.draw(window)

    text_box = Text(Point(x, y), text)
    text_box.setTextColor("white")
    text_box.setSize(20)
    text_box.setFace('helvetica')
    text_box.draw(window)


def draw_image(window, path, x, y):
    image = Image(Point(x, y), path)
    image.draw(window)