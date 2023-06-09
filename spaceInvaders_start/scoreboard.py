import pygame as pg 
# import pygame.font
from pygame.sprite import Group
from ship import Ship
import pickle as pk

class Scoreboard:
    def __init__(self, game): 
        self.score = 0
        self.level = 1
        try:
            with open('score.dat', 'rb') as file:
                self.high_score = pk.load(file)
        except:
                self.high_score = 0
        
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (255, 255, 255)
        self.font = pg.font.SysFont(None, 48)

        self.score_image = None 
        self.score_rect = None
        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def calculate_score(self, row):
        scores = {0: 30,
                  1: 20,
                  2: 10
                  }

        score = scores[row]
        self.score += score
        self.prep_score()

    def prep_score(self): 
        rounded_score = int(round(self.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score = int(round(self.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.prep_high_score()
    
    def prep_level(self):
        self.level_image = self.font.render(str(self.level), True, self.text_color, self.settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def reset(self): 
        self.score = 0
        self.level = 1
        self.update()

    def update(self): 
        # TODO: other stuff
        self.draw()

    def draw(self): 
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)