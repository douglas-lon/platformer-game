import pygame as pg
from main.utils.settings import SCREEN_HEIGTH, SCREEN_WIDTH

class SimpleMenu:
    def __init__(self, font_size, surface):
        self.font = pg.font.SysFont('verdana', font_size)
        self.surface = surface

    def menu(self, title, sub_title , title_color, surface_color):
        title = self.font.render(title, True, title_color)
        key = self.font.render(sub_title, True, title_color)

        title_rect = title.get_rect()
        title_rect.center = (SCREEN_WIDTH // 2, (SCREEN_HEIGTH // 2) -100)

        key_rect = key.get_rect()
        key_rect.center = (title_rect.center[0], title_rect.center[1] + 100)

        in_menu = True
        
        while in_menu:
            self.surface.fill(surface_color)
            
            self.surface.blit(title, title_rect)
            self.surface.blit(key, key_rect)
            
            #self.events()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                
                if event.type == pg.KEYDOWN:
                    in_menu = False
            
            pg.display.update()
