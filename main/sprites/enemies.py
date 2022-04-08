import pygame as pg
from random import randint
from main.utils.support import distance_betwewn_rects

class Enemy(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pg.Surface((size,size))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        self.velocity_x = randint(4, 6)
        self.direction = 1

    def move(self, direction):
        self.rect.x += (self.velocity_x * direction)    

    def update(self, player_rect):
        self.state_controller(player_rect)

    def find_player(self, player_rect):
        #self.direction = 0

        if player_rect.right - 10 >= self.rect.right:
            self.direction = 1
        elif player_rect.left + 10 <= self.rect.left:
            self.direction = -1

        return self.direction

    def chase_player(self, player_rect):
        direction = self.find_player(player_rect)
        self.move(direction)
    
    def idle(self):
        self.move(self.direction)
    
    def state_controller(self,  player_rect):
        if abs(distance_betwewn_rects(self.rect, player_rect)) <= 300:
            self.chase_player(player_rect)
        else:
            self.idle()

    def on_boundarie_collision(self, rect):
        if self.rect.right <= rect.right:
            self.rect.right = rect.left
        elif rect.left <= self.rect.left:
            self.rect.left = rect.right
            
        self.direction *= -1

    def draw(self, surface, offset):
        
        offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )
        surface.blit(self.image, offset_rect)