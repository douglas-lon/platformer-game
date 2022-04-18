import pygame as pg
from main.sprites.enemies import Enemy
from main.utils.import_functions import import_csv, import_sprites
from main.utils.settings import *
from main.utils.collision import(OneToManyCollision, 
                                ManyToManyCollision)
from main.utils.camera import Camera
from main.world.game_data import levels
from main.sprites.tiles import Tile 
from main.sprites.player import Player, TestPlayer


class Level:
    def __init__(self, level_index):
        # Inicializa Player e Camera
        #self.player = Player((200, 64), TILE_SIZE))
        self.player = TestPlayer((200, 64), 60)
        #self.enemie = Enemy((400, 200), 60)
        self.camera = Camera()
        # Cria variavel para definir o limite da esquerda do mapa
        self.min_x = 0
        self.restart = False

        self.level_index = level_index
        # Carrega o mapa baseado no index passado
        # Cria sprite group e layout
        self.level_data = levels[self.level_index]
        self.sprites = {}
        self.create_sprites(self.level_data)
        self.limits = self.camera.find_limits(self.sprites['terrain'].sprites())


    def create_sprites(self, data):
        for key in list(data.keys()):
            if key == 'player' or key == 'imgs' :
                break
            data_csv = import_csv(data.get(key))
            self.sprites[key] = self.create_sprite_groups(
                data_csv, key
                )

    def create_sprite_groups(self, data, sprite_name):
        sprite_group = pg.sprite.Group()
        sprites = import_sprites(self.level_data['imgs'][sprite_name])

        for row_i, row in enumerate(data):
            for col_i, col in enumerate(row):
                # Testa se não é um espaço em branco
                if col != '-1':
                    x = col_i * TILE_SIZE
                    y = row_i * TILE_SIZE

                    if sprite_name == 'enemy':
                        enemy = Enemy((x, y + 4), 60)
                        sprite_group.add(enemy)
                        continue

                    tile = Tile(x,y,TILE_SIZE, sprites[int(col)])
                    sprite_group.add(tile)

        return sprite_group
    
    def collision_handler(self):
        OneToManyCollision.vertical_collision(
            self.player.rect, 
            self.sprites['terrain'].sprites(), 
            [
                self.player.on_bottom_collision, 
                self.player.on_top_collision
            ]
            )
            
        OneToManyCollision.horizontal_collision(
            self.player.rect,
            self.sprites['terrain'].sprites(),
            [
                self.player.on_left_collision, 
                self.player.on_right_collision
            ],
            self.player.velocity.x
            )

        ManyToManyCollision.any_side_collision(
            self.player.gun.bullets, 
            self.sprites['terrain'], 
            [True, False] , print
            )

        for enemy in self.sprites['enemy'].sprites():

            OneToManyCollision.any_side_collision(
                enemy, 
                self.sprites['boundaries'], 
                enemy.on_boundarie_collision
                )

            OneToManyCollision.any_side_collision(
                enemy,
                self.player.gun.bullets,
                enemy.on_bullet_collision,
                True
                )
    
    def define_level_boundaries(self):
        if self.player.rect.left <= self.limits[0]:
            x = (self.limits[0] + self.player.rect.width / 2) 
            self.player.position.x = x + 2
            self.player.velocity.x = 0

        if self.player.rect.right >= self.limits[1]:
            x = (self.limits[1] - self.player.rect.width / 2) 
            self.player.position.x = x - 1
            self.player.velocity.x = 0
        
        if self.player.rect.top <= self.limits[2]:
            self.player.rect.top = self.limits[2]
            self.player.position.y = self.limits[2] + TILE_SIZE
            self.player.velocity.y = 0

        if self.player.rect.top > self.limits[3]:
            self.restart = True
        

    def change_level(self):
        level_index = ''
        if (self.player.rect.x 
                > self.sprites['terrain'].sprites()[-1].rect.x 
                and level_index != 0):
                
            level_index = self.level_index + 1
        
        return level_index
    
    def update(self, dt):
        #self.terrain_sprite.update()
        self.player.update(dt)
        self.define_level_boundaries()
        self.collision_handler()
        for key in list(self.sprites):
            if key == 'enemy':
                for spr in self.sprites[key].sprites():
                    if spr.health <= 0:
                        self.sprites[key].remove(spr)
                    spr.update(self.player.rect)

        self.camera.update(
            self.player.rect, 
            self.limits[0], 
            self.limits[1],
            self.limits[2],
            self.limits[3]
            )

    def draw(self, surface):
        
        # Usa draw da classe Tile para poder implementar a camera
        #for tile in self.terrain_sprite.sprites():
        #    tile.draw(surface, self.camera.offset)
        
        for key in list(self.sprites):
            if key == 'grass' or key == 'boundaries':
                continue
            for sprite in self.sprites.get(key).sprites():
                sprite.draw(surface, self.camera.offset)
        
        #self.enemie.draw(surface, self.camera.offset)
        self.player.draw(surface, self.camera.offset)

        for grass in self.sprites['grass'].sprites():
            grass.draw(surface, self.camera.offset)
