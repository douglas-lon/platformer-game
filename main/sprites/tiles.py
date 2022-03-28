import pygame as pg

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