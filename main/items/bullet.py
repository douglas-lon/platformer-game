import pygame as pg

class Bullet(pg.sprite.Sprite):
    def __init__(self, init_pos, vel):
        super().__init__() 
        self.image = pg.image.load('./main/assets/imgs/bullet.png')
        #self.image.fill('pink')
        self.rect = self.image.get_rect(topleft=(init_pos))
        self.velocity = vel
        self.init_pos = init_pos
    
    def update(self):
        self.rect.x += self.velocity
    
    def draw(self, screen, offset):
        offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.rect.size
            )
        screen.blit(self.image, offset_rect)