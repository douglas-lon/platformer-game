import pygame as pg
from main.utils.settings import TILE_SIZE

class OneToManyCollision:
    @staticmethod
    def vertical_collision(main, secondary, callback):
        # Cria um rect baseado no main que é um pouco maior para testar colisão
        collidable_rect = main.copy()
        collidable_rect.size = (
            collidable_rect.size[0],
            collidable_rect.size[1] + 1
            )

        for sprite in secondary:
            if sprite.rect.colliderect(collidable_rect):
                if (sprite.rect.left - TILE_SIZE//2 
                        <= collidable_rect.centerx 
                        <= sprite.rect.right + TILE_SIZE//2):
                    
                    if collidable_rect.top < sprite.rect.top:
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
                    if  (sprite.rect.centerx 
                            <= collidable_rect.left 
                            <= sprite.rect.right):

                        callback[0](sprite.rect)
                        break
                
        if direction > 0:
            collidable_rect = main.copy()
            collidable_rect.size = (
                collidable_rect.size[0] + 1, 
                collidable_rect.size[1]
                )

            for sprite in secondary:
                if sprite.rect.colliderect(collidable_rect):
                    if (sprite.rect.centerx 
                        >= collidable_rect.right 
                        >= sprite.rect.left):

                        callback[1](sprite.rect)
                        break
    
    @staticmethod
    def any_side_collision(main, secondary, callback, kill=False):
        if not kill:
            main = main.rect
            secondary = secondary.sprites()
            for sprite in secondary:
                if sprite.rect.colliderect(main):
                    callback(sprite.rect)
                    break
        else:
            collide = pg.sprite.spritecollide(main, secondary, kill)
            if collide:
                callback(None)
        


class ManyToManyCollision:
    @staticmethod
    def any_side_collision(
            first_group, second_group, 
            kill, callback
            ):

        if pg.sprite.groupcollide(
                first_group, second_group, 
                kill[0], kill[1]):
                
            callback()
