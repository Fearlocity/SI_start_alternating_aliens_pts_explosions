from pygame import *
class Text(object):
    def __init__(self, textFont, size, message, color, xpos, ypos, game):
        self.screen = game.screen
        self.font = font.Font(textFont, size)
        self.surface = self.font.render(message, True, color)
        self.rect = self.surface.get_rect(topleft=(xpos, ypos))
        

    def draw(self):
        self.screen.blit(self.surface, self.rect)
