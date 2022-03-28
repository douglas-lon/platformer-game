import pygame as pg
from main.utils.import_functions import import_csv, import_sprites
from main.utils.settings import *
from main.utils.collision import AmbientCollision
from main.utils.camera import Camera
from main.world.game_data import levels
from main.sprites.tiles import Tile 
from main.sprites.player import Player, TestPlayer

class Level:
    def __init__(self, level_index):
        # Inicializa Player e Camera
        #self.player = Player((200, 64), TILE_SIZE)
        self.player = TestPlayer((200, 64), 60)
        self.camera = Camera()
        # Cria variavel para definir o limite da esquerda do mapa
        self.min_x = ''

        self.level_index = level_index
        # Carrega o mapa baseado no index passado
        # Cria sprite group e layout
        self.t_sprites = import_sprites('./main/assets/imgs/terrain_tileset.png')
        self.level_data = levels[self.level_index]
        self.terrain = import_csv(self.level_data['terrain'])
        self.terrain_sprite = self.create_terrain()


    def create_terrain(self):
        sprite_group = pg.sprite.Group()

        # Percorre as linhas das coordenadas
        for row_i, row in enumerate(self.terrain):
            # Percorre as colunas das coordenadas
            for col_i, col in enumerate(row):
                # Testa se não é um espaço em branco
                if col != '-1':
                    # Define uma cordenada baseada na posição 
                    # na lista e no tamanho do Tile
                    x = col_i * TILE_SIZE
                    y = row_i * TILE_SIZE

                    # Checagem para descobrir o menor 
                    # valor da esquerda(Limite)
                    if self.min_x == '':
                        self.min_x = x
                    if x < self.min_x:
                        self.min_x = x
                    tile = Tile(x,y,TILE_SIZE, self.t_sprites[int(col)])
                    sprite_group.add(tile)

        return sprite_group
    
    def collision_handler(self):
        AmbientCollision.vertical_collision(
            self.player.rect, 
            self.terrain_sprite.sprites(), 
            [self.player.on_bottom_collision, self.player.on_top_collision]
            )
        AmbientCollision.horizontal_collision(
            self.player.rect,
            self.terrain_sprite.sprites(),
            [self.player.on_left_collision, self.player.on_right_collision],
            self.player.velocity.x
            )


    def bew_collision(self):
        new_rect = self.player.rect.copy()
        new_rect.size = (new_rect.size[0],new_rect.size[1] + 1)
        for sprite in self.terrain_sprite.sprites():
            if sprite.rect.colliderect(new_rect):
                if sprite.rect.left - TILE_SIZE//2 <= new_rect.centerx <= sprite.rect.right + TILE_SIZE//2:
                    if new_rect.centery < sprite.rect.top:
                        self.player.rect.bottom = sprite.rect.top
                        self.player.position.y = sprite.rect.top
                        self.player.velocity.y = 0
                        self.player.on_ground = True
                        break


    def vertical_collision(self):
        # Necessário criar um rect maior para colisão para impedir o 
        # player de ficar 'flicando'
        new_rect = self.player.rect.copy()
        new_rect.size = (new_rect.size[0],new_rect.size[1] + 2)
        for sprite in self.terrain_sprite.sprites():

            if not self.player.velocity.y < -1:
                # O motivo de fazer a colisão de baixo só quando o player
                # não estiver indo para cima e para evitar alguns bugs com plataformas acima do player
                """if self.player.rect.top <= sprite.rect.top - (self.player.velocity.y +1) <= self.player.rect.bottom and sprite.rect.x - TILE_SIZE < self.player.rect.x < sprite.rect.x + TILE_SIZE:
                    
                    self.player.position.y = sprite.rect.top
                    self.player.velocity.y = 0
                    self.player.on_ground = True
                    break"""
                if sprite.rect.colliderect(new_rect):
                    if sprite.rect.top + self.player.velocity.y * 2 > new_rect.bottom > sprite.rect.top:
                        self.player.rect.bottom = sprite.rect.top
                        self.player.position.y = sprite.rect.top - 1
                        self.player.velocity.y = 0
                        self.player.on_ground = True
                        break
            else:
                # self.player.rect.top >= sprite.rect.bottom + ((self.player.velocity.y * -1) +1) <= self.player.rect.bottom
                if self.player.rect.centery >= sprite.rect.bottom >= self.player.rect.top and sprite.rect.x - TILE_SIZE < self.player.rect.x < sprite.rect.x + TILE_SIZE:
                    self.player.rect.top = sprite.rect.bottom
                    self.player.position.y = (sprite.rect.bottom + self.player.rect.width)
                    self.player.velocity.y = 0
                    self.player.jump_counter = self.player.max_jump_counter + 1 
                    break

    def horizontal_collision(self):
        for sprite in self.terrain_sprite.sprites():
            
            if sprite.rect.colliderect(self.player.rect):
                if self.player.velocity.x < 0:
                    x = (sprite.rect.right + self.player.rect.width / 2) 
                    self.player.position.x = x
                    self.player.velocity.x = 0
                    self.player.collided_side = pg.K_LEFT
                    self.player.collided_rect = sprite.rect
                    break

                if self.player.velocity.x > 0:
                    x = (sprite.rect.left - self.player.rect.width / 2)
                    self.player.position.x = x
                    self.player.velocity.x = 0
                    self.player.collided_side = pg.K_RIGHT
                    self.player.collided_rect = sprite.rect
                    break
    
    def change_level(self):
        level_index = ''
        if self.player.rect.x > self.terrain_sprite.sprites()[-1].rect.x and level_index != 0:
            level_index = self.level_index + 1
        
        return level_index
    
    def update(self, dt):
        self.terrain_sprite.update()
        self.player.update(dt)
        self.collision_handler()
        self.camera.update(
            self.player.rect, 
            self.min_x, 
            self.terrain_sprite.sprites()[-1].rect.x
            )
        #print(self.player.on_ground)
        #print(self.player.velocity.y)

    def draw(self, surface):
        
        # Usa draw da classe Tile para poder implementar a camera
        for tile in self.terrain_sprite.sprites():
            tile.draw(surface, self.camera.offset)
        
        self.player.draw(surface, self.camera.offset)