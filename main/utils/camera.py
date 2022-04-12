from main.utils.settings import SCREEN_HEIGTH, SCREEN_WIDTH, TILE_SIZE
from pygame.math import Vector2

class Camera:
    def __init__(self):
        self.offset = Vector2(0,0)
    
    def update(self, target, limit_left, limit_right, limit_top, limit_bottom):
        # Usa outras variáveis em vez de alterar o valor atual do 
        # self.offset para ter dois valores o antigo e o atual

        offset_x = target.centerx - SCREEN_WIDTH // 2
        offset_y = target.centery - SCREEN_HEIGTH // 2
        
        # Define Limite da Esquerda
        if  offset_x < limit_left:
            offset_x = limit_left
        
        # Define Limite da Direita
        if target.x + SCREEN_WIDTH // 2 >= limit_right:
            offset_x = self.offset.x
        
        if  target.centery + SCREEN_WIDTH // 3 >= limit_bottom:
            offset_y = self.offset.y


        if  offset_y < limit_top:
            offset_y = limit_top
            
        self.offset.update(offset_x, offset_y)

    def find_limits(self, terrain):
        left_limit = 100
        right_limit = 100
        top_limit = 100
        bottom_limit = 100

        for spr in terrain:
            if spr.rect.x <= left_limit:
                left_limit = spr.rect.left
            
            if spr.rect.x >= right_limit:
                right_limit = spr.rect.right

            if spr.rect.y <= top_limit:
                top_limit = spr.rect.top

            if spr.rect.y >= bottom_limit:
                bottom_limit = spr.rect.bottom

        return (
            left_limit,
            right_limit,
            top_limit,
            bottom_limit
        )
        
        
        


    
        
