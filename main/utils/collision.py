import pygame as pg
from main.utils.settings import TILE_SIZE

class AmbientCollision:
    @staticmethod
    def vertical_collision(main, secondary, callback):
        collidable_rect = main.copy()
        #collidable_rect.inflate_ip(0,1)
        #collidable_rect = collidable_rect.inflate(0,1)
        collidable_rect.size = (collidable_rect.size[0],collidable_rect.size[1] + 1)

        for sprite in secondary:
            if sprite.rect.colliderect(collidable_rect):
                #print(collidable_rect.bottom, sprite.rect.top, main.bottom)
                if sprite.rect.left - TILE_SIZE//2 <= collidable_rect.centerx <= sprite.rect.right + TILE_SIZE//2:

                    if collidable_rect.centery < sprite.rect.top:
                        callback[0](sprite.rect)
                        break
                    
                    if collidable_rect.centery > sprite.rect.bottom:
                        callback[1](sprite.rect)
                        break

    
    @staticmethod
    def horizontal_collision(main, secondary, callback, direction):

        if direction < 0:
            collidable_rect = main.copy()
            collidable_rect.left = main.left - 1

            for sprite in secondary:
                if sprite.rect.colliderect(collidable_rect):
                    #print(collidable_rect.right, sprite.rect.left, main.right)
                    if  sprite.rect.centerx <= collidable_rect.left <= sprite.rect.right:
                        #print(collidable_rect.left, sprite.rect.right, main.left)
                        callback[0](sprite.rect)
                        break
                
        if direction > 0:
            collidable_rect = main.copy()
            collidable_rect.size = (collidable_rect.size[0] + 1, collidable_rect.size[1])
            for sprite in secondary:
                if sprite.rect.colliderect(collidable_rect):
                    print(collidable_rect.right, sprite.rect.left, main.right)
                    if sprite.rect.centerx >= collidable_rect.right >= sprite.rect.left:
                        #print(collidable_rect.right, sprite.rect.left, main.right)
                        callback[1](sprite.rect)
                        break
