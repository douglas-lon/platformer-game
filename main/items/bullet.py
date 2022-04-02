import pygame as pg

class Bullet:
    def __init__(self, init_pos, vel):
        self.rect = pg.Rect((init_pos), (10, 10))
        self.velocity = vel
    
    def update(self):
        self.rect.x += self.velocity

    
    def draw(self, screen, offset):
        offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.rect.size
            )
        pg.draw.circle(screen, 'pink', offset_rect.center, 5)