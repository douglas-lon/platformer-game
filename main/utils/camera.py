from main.utils.settings import SCREEN_HEIGTH, SCREEN_WIDTH
from pygame.math import Vector2

class Camera:
    def __init__(self):
        self.offset = Vector2(0,0)
    
    def update(self, target, limit_left, limit_right):
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

        # Define limite de baixo
        if offset_y > 0:
            offset_y = 0
        
        self.offset.update(offset_x, offset_y)
        
        


    
        
