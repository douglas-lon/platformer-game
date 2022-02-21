import pygame as pg
from main.utils.import_functions import import_csv
from main.world.game_data import levels
from main.utils.settings import *
from main.world.tiles import Tile 
from main.world.camera import Camera
from main.entities.player import Player

class Level:
    def __init__(self, level_index):
        self.player = Player((64,64), TILE_SIZE)
        self.camera = Camera()

        self.min_x = ''
        self.level_data = levels[level_index]
        self.terrain = import_csv(self.level_data['terrain'])
        self.terrain_sprite = self.create_terrain()


    def create_terrain(self):
        sprite_group = pg.sprite.Group()
        for row_i, row in enumerate(self.terrain):
            for col_i, col in enumerate(row):
                if col != '-1':
                    x = col_i * TILE_SIZE
                    y = row_i * TILE_SIZE

                    if self.min_x == '':
                        self.min_x = x

                    if x < self.min_x:
                        self.min_x = x

                    tile = Tile(x,y,TILE_SIZE)
                    sprite_group.add(tile)

        return sprite_group
    
    def ambient_collision(self):
        self.horizontal_collision()
        self.vertical_collision()
    
    def vertical_collision(self):
        for sprite in self.terrain_sprite.sprites():
            if sprite.rect.colliderect(self.player.rect):

                if sprite.rect.top + self.player.velocity.y * 2 > self.player.rect.bottom > sprite.rect.top:
                    self.player.position.y = sprite.rect.top +1
                    self.player.velocity.y = 0
                    self.player.on_ground = True
                    sprite.image.fill('white')
                    break
    
    def horizontal_collision(self):
        for sprite in self.terrain_sprite.sprites():
            sprite.image.fill('black')
            if sprite.rect.colliderect(self.player.rect):

                if  (sprite.rect.right + self.player.velocity.x * 1.1 < self.player.rect.left < sprite.rect.right) and sprite.rect.top < self.player.rect.bottom - 2 < sprite.rect.bottom:
                    self.player.position.x = (sprite.rect.right + self.player.rect.width / 2) + 1
                    self.player.velocity.x = 0
                    sprite.image.fill('blue')
                    break
                
                if  (sprite.rect.left + self.player.velocity.x * 1.1 > self.player.rect.right > sprite.rect.left) and sprite.rect.top < self.player.rect.bottom - 2 < sprite.rect.bottom:
                    print('true')
                    self.player.position.x = (sprite.rect.left - self.player.rect.width / 2) -1
                    self.player.velocity.x = 0
                    sprite.image.fill('red')
                    break
    

    def update(self, dt):
        self.terrain_sprite.update()
        self.player.update(dt)
        self.ambient_collision()
        self.camera.update(self.player.rect, self.min_x, self.terrain_sprite.sprites()[-1].rect.x)

    def draw(self, surface):
        for tile in self.terrain_sprite.sprites():

            tile.draw(surface, self.camera.offset)
        
        

        self.player.draw(surface, self.camera.offset)