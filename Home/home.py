from UtilFunctions import functions as util


class HomeManager:
    def __init__(self):
        self.choose_oponent_flag = False
        self.titleX = 500
        self.titleY = 60
        self.playButtonX = 500
        self.playButtonY = 200
        self.quitButtonX = 500
        self.quitButtonY = 280
        self.imageX = 850
        self.imageY = 600
        self.computerButtonX = 800
        self.computerButtonY = 200
        self.player2ButtonX = 200
        self.player2ButtonY = 200
        self.offsetX = 100
        self.offsetY = 20

    def draw_home(self, window):
        util.reset_screen(window)
        util.draw_un_bordered_text(window, "Go Game", self.titleX, self.titleY)
        util.draw_bordered_text(window, "Play", self.playButtonX, self.playButtonY)
        util.draw_bordered_text(window, "Quit", self.quitButtonX, self.quitButtonY)
        util.draw_image(window, "../Images/GoTable.png", self.imageX, self.imageY)

    def handle_mouse_click_home(self, window):
        mouse_data = window.getMouse()
        if util.check_inside(mouse_data.x, mouse_data.y, self.playButtonX - self.offsetX,
                             self.playButtonY - self.offsetY, self.playButtonX + self.offsetX,
                             self.playButtonY + self.offsetY):
            if not self.choose_oponent_flag:
                util.draw_bordered_text(window, "Computer", self.computerButtonX, self.computerButtonY)
                util.draw_bordered_text(window, "Player 2", self.player2ButtonX, self.player2ButtonY)
                self.choose_oponent_flag = True
                return (True, "Pressed play")
            else:
                self.choose_oponent_flag = False
                return (True, "Home")

        if util.check_inside(mouse_data.x, mouse_data.y, self.quitButtonX - self.offsetX,
                             self.quitButtonY - self.offsetY, self.quitButtonX + self.offsetX,
                             self.quitButtonY + self.offsetY):
            return (False, "Home")

        if util.check_inside(mouse_data.x, mouse_data.y, self.computerButtonX - self.offsetX,
                             self.computerButtonY - self.offsetY, self.computerButtonX + self.offsetX,
                             self.computerButtonY + self.offsetY):
            self.choose_oponent_flag = False
            return (True, "Pressed computer")

        if util.check_inside(mouse_data.x, mouse_data.y, self.player2ButtonX - self.offsetX,
                             self.player2ButtonY - self.offsetY, self.player2ButtonX + self.offsetX,
                             self.player2ButtonY + self.offsetY):
            self.choose_oponent_flag = False
            return (True, "Pressed player")

        if not self.choose_oponent_flag:
            return (True, "Home")
        else:
            return (True, "Pressed play")

    def clear(self, window):
        for item in window.items[:]:
            item.undraw()
