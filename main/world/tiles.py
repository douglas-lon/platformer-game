import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pg.Surface((size, size))
        self.image.fill('black')
        self.rect = self.image.get_rect(topleft=(x,y))
    
    def update(self, shift):
        self.rect.x += shift
    
    def __str__(self) :
        return f'{self.rect}'