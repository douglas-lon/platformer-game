from shutil import move
import pygame as pg
from random import randint

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pg.Surface((size,size))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)
        self.velocity_x = randint(4, 6)

    def move(self):
        self.rect.x += self.velocity_x

    def update(self):
        self.move()

    def draw(self, surface, offset):
        offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )
        surface.blit(self.image, offset_rect)