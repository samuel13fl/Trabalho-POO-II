import pygame as pg
import settings
from os import path 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)
FPS = 60
WIDTH = 1024
HEIGHT = 768

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption('1')
        self.load_menu()
        self.clock = pg.time.Clock()
    
    def load_menu(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')

        self.mainscreen = pg.image.load(path.join(img_folder, settings.mainscreen)).convert_alpha()
        self.gameoverscreen = pg.image.load(path.join(img_folder, settings.gameoverscreen)).convert_alpha()
        self.optionscreen = pg.image.load(path.join(img_folder, settings.optionscreen)).convert_alpha()
        self.pausescreen = pg.image.load(path.join(img_folder, settings.pausescreen)).convert_alpha()
    
    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
        
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
               
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 0:
                    self.click = True
                if event.button == 1:
                    self.click = False
            

    # def pause(self):
    #     self.current_screen = "Pause"
    #     self.screen.blit(self.pausescreen, (0, 0))
    #     self.button_pause_back = pg.Rect(400, 300, 200, 50)
    #     self.button_pause_save = pg.Rect(400, 400, 200, 50)
    #     self.button_pause_quit = pg.Rect(400, 500, 200, 50)
    #     pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_back,1)
    #     pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_save,1)
    #     pg.draw.rect(self.screen, (255, 0, 0), self.button_pause_quit,1)
    #     pg.display.flip()
    #     self.wait_for_key()

    def show_start_screen(self):
        self.current_screen = "Start Screen"
        self.screen.blit(self.mainscreen,(0,0))
        self.button_start_start = pg.Rect(68, 204, 220, 30)
        self.button_start_option = pg.Rect(64, 340, 190, 35)
        self.button_start_load = pg.Rect(68, 465, 125, 30)
        self.button_start_quit = pg.Rect(63, 596, 130, 30)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_start,-1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_load,-1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_option,-1)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_start_quit,-1)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.current_screen = "Game Over Screen"
        self.screen.blit(self.gameoverscreen,(0,0))
        self.button_go_restart = pg.Rect(156, 666, 289, 32 )
        self.button_go_quit = pg.Rect(694, 666, 192, 29)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_restart,-1)
        pg.draw.rect(self.screen, (255, 0, 0), self.button_go_quit,-1)
        pg.display.flip()
        self.wait_for_key()

    def options(self):
        self.current_screen = "Options Screen"
        self.screen.blit(self.optionscreen,(0,0))
        self.button_options_return = pg.Rect(336, 480, 385, 57)
        pg.draw.rect(self.screen, (0, 0, 0), self.button_options_return,-1)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        self.click_test = False
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.click_test = True
            mx, my = pg.mouse.get_pos()

            #  if self.current_screen == "Pause" and self.button_pause_back.collidepoint((mx, my)):
            #      if self.click_test:
            #          pass

            #  if self.current_screen == "Pause" and self.button_pause_save.collidepoint((mx, my)):
            #      if self.click_test:
            #          pass 

            #  if self.current_screen == "Pause" and self.button_pause_quit.collidepoint((mx, my)):
            #      if self.click_test:
            #          g.show_go_screen()

            if self.current_screen == "Game Over Screen" and self.button_go_restart.collidepoint((mx, my)):
                if self.click_test:
                    g.new()
                    g.run()
                    g.show_go_screen()

            if self.current_screen == "Game Over Screen" and self.button_go_quit.collidepoint((mx, my)):
                if self.click_test:
                    g.show_start_screen()

            if self.current_screen == "Start Screen" and self.button_start_start.collidepoint((mx, my)):
                if self.click_test:
                    g.new()
                    g.run()
                    g.show_go_screen()

            if self.current_screen == "Start Screen" and self.button_start_option.collidepoint((mx, my)):
                if self.click_test:
                    g.options()

            if self.current_screen == "Start Screen" and self.button_start_quit.collidepoint((mx, my)):
                if self.click_test:
                    self.quit()
        
            if self.current_screen == "Options Screen" and self.button_options_return.collidepoint((mx, my)):
                if self.click_test:
                    g.show_start_screen() 


# create the game object
g = Game()
g.show_start_screen()

g = Game()