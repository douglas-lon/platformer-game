import pygame as pg
from main.utils.import_functions import import_sprites

class Door(pg.sprite.Sprite):
    def __init__(self, surface_list, pos, entrance=False):
        super().__init__()
        self.frames = surface_list
        self.entrance = entrance
        if not self.entrance:
            self.image = self.frames[0]
        else:
            self.image = self.frames[3]

        self.rect = self.image.get_rect(topleft=pos)
        self.change_level = False

    def draw(self, surface, offset):

        self.offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )

        surface.blit(self.image, self.offset_rect)
        
    def update(self, player_rect, player_items):
        if not self.entrance:
            is_colliding = self.rect.colliderect(player_rect)

            self.get_event(is_colliding, player_items)

    def get_event(self, is_colliding, items):
        keys = pg.key.get_pressed()

        if keys[pg.K_e] and is_colliding:
            self.states(items)
    
    def get_state(self):
        return self.change_level

    def states(self, items):
        if 'key' in items:
            self.image = self.frames[2]
            self.change_level = True
        else:
            self.image = self.frames[1]
        

