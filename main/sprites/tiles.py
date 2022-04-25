import pygame as pg
from main.utils.import_functions import import_sprites

class Tile(pg.sprite.Sprite):
    def __init__(self, x, y, size, surface):
        # Cria uma surface com o tamanho determinado
        # e coloca ela na posição
        super().__init__()
        self.image = surface
        #self.image.fill('black')
        self.rect = self.image.get_rect(topleft=(x,y))
    
    def update(self):
        pass

    def draw(self, surface, offset):
        # Desenha a imagem na posição predeterminada pelo offset
        # Como só o desenho na tela é mudado 
        # a posição básica da imagem é a mesma
        self.offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )
        surface.blit(self.image, self.offset_rect)


    def __str__(self) :
        return f'{self.rect}'

class AnimatedTile(pg.sprite.Sprite):
    def __init__(self, x, y, surface_list):
        super().__init__()
        self.frames = surface_list
        self.frame_num = 0

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x,y))

    def animate(self):
        self.frame_num += 0.12

        if self.frame_num > len(self.frames):
            self.frame_num = 0
        
        self.image = self.frames[int(self.frame_num)]
        #self.rect = self.image.get_rect(topleft=(x,y))
    
    def update(self):
        self.animate()

    def draw(self, surface, offset):
        # Desenha a imagem na posição predeterminada pelo offset
        # Como só o desenho na tela é mudado 
        # a posição básica da imagem é a mesma
        self.offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )
        surface.blit(self.image, self.offset_rect)