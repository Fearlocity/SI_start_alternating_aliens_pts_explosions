import pygame as pg
import pickle as pk
from settings import Settings
from laser import Lasers, LaserType
from alien import Aliens
from alien import Mystery
from ship import Ship
from sound import Sound
from scoreboard import Scoreboard
from vector import Vector
from barrier import Barriers
from text import Text
import sys 


class Game:
    def __init__(self):
        pg.init()
        self.settings = Settings()
        size = self.settings.screen_width, self.settings.screen_height   # tuple
        self.screen = pg.display.set_mode(size=size)
        pg.display.set_caption("Alien Invasion")
        self.mainscreen = True
        self.startgame = False
        WHITE = (255, 255, 255)
        GREEN = (78, 255, 87)
        BLUE = (80, 255, 239)
        PURPLE = (203, 0, 255)
        FONT = 'font/font.ttf'
        self.titleText = Text(FONT, 50, 'Space Invaders', WHITE, 364, 355, game=self)
        self.titleText2 = Text(FONT, 25, 'Press any key to continue', WHITE,
                               401, 425, game=self)
        self.alien1Text = Text(FONT, 25, '   =   10 pts', GREEN, 568, 470, game=self)
        self.alien2Text = Text(FONT, 25, '   =  20 pts', BLUE, 568, 520, game=self)
        self.alien3Text = Text(FONT, 25, '   =  30 pts', PURPLE, 568, 570, game=self)

        self.sound = Sound(bg_music="sounds/startrek.wav")
        self.scoreboard = Scoreboard(game=self) 

        self.ship_lasers = Lasers(settings=self.settings, type=LaserType.SHIP)
        self.alien_lasers = Lasers(settings=self.settings, type=LaserType.ALIEN)
        
        self.barriers = Barriers(game=self)
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.mystery = Mystery(game=self)
        self.settings.initialize_speed_settings()

    def handle_events(self):
        keys_dir = {pg.K_w: Vector(0, -1), pg.K_UP: Vector(0, -1), 
                    pg.K_s: Vector(0, 1), pg.K_DOWN: Vector(0, 1),
                    pg.K_a: Vector(-1, 0), pg.K_LEFT: Vector(-1, 0),
                    pg.K_d: Vector(1, 0), pg.K_RIGHT: Vector(1, 0)}
        
        for event in pg.event.get():
            if event.type == pg.QUIT: self.game_over()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v += self.settings.ship_speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()

    def reset(self):
        print('Resetting game...')
        # self.lasers.reset()    # handled by ship for ship_lasers and by aliens for alien_lasers
        self.aliens.reset()
        self.barriers.reset()
        self.ship.reset()
    
    def create_main_menu(self):
        self.alien1 = pg.image.load('images/alien__20.png')
        self.alien1 = pg.transform.scale(self.alien1, (40, 40))
        self.alien2 = pg.image.load('images/alien__10.png')
        self.alien2 = pg.transform.scale(self.alien2, (40, 40))
        self.alien3 = pg.image.load('images/alien_03-0.png')
        self.alien3 = pg.transform.scale(self.alien3, (40, 40))
        self.screen.blit(self.alien1, (518, 470))
        self.screen.blit(self.alien2, (518, 520))
        self.screen.blit(self.alien3, (518, 570))

    def game_over(self):
        print('All ships gone: game over!')
        self.sound.gameover()
        with open('score.dat', 'wb') as file:
            pk.dump(self.scoreboard.high_score, file)
        pg.quit()
        sys.exit()

    def play(self):
        self.sound.play_bg()
        while True:
            if self.mainscreen:
                self.screen.fill(self.settings.bg_color)
                self.titleText.draw()
                self.titleText2.draw()
                self.alien1Text.draw()
                self.alien2Text.draw()
                self.alien3Text.draw()
                self.create_main_menu()
                pg.display.flip()
                for e in pg.event.get():
                    if e.type == pg.QUIT: self.game_over()
                    if e.type == pg.KEYUP:
                        self.startgame = True
                        self.mainscreen = False
            if self.startgame:
                self.currentTime = pg.time.get_ticks()
                self.handle_events() 
                self.screen.fill(self.settings.bg_color)
                self.ship.update()
                self.aliens.update()
                self.barriers.update()
                self.mystery.update(self.currentTime)
                # self.lasers.update()    # handled by ship for ship_lasers and by alien for alien_lasers
                self.scoreboard.update()
                pg.display.flip()


def main():
    g = Game()
    g.play()

if __name__ == '__main__':
    main()
