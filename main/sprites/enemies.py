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
        self.knockback = 0

        self.health = 100

    def move(self, direction):
        self.rect.x += (self.velocity_x * direction)    

    def update(self, player_rect):
        self.enemy_logic(player_rect)

        # Move o inimigo para trás quando ele é atigingido
        if self.knockback > 0:
            self.rect.x += (self.direction*-1) * 10
            self.knockback -= 1
    
    def enemy_logic(self, player_rect):
        self.idle()

    def idle(self):
        self.move(self.direction)

    def on_boundarie_collision(self, rect):

        if self.rect.right <= rect.right:
            self.rect.right = rect.left
        elif rect.left <= self.rect.left:
            self.rect.left = rect.right
            
        self.direction *= -1

    def on_bullet_collision(self, sprite_rect):
        self.knockback = 20
        self.take_damage(20)

    def take_damage(self, dmg):
        self.health -= dmg

    def draw(self, surface, offset):
        
        offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )
        surface.blit(self.image, offset_rect)

        # Calcula a porcentagem da vida atual para desenhar na tela
        health_percentage = (60*self.health) / 100
        offset_rect_health = pg.Rect(
            (self.rect.x - offset.x, (self.rect.y - 30) - offset.y), 
            (health_percentage, 10)
            )

        pg.draw.rect(surface, 'yellow', offset_rect_health)


class StalkerEnemy(Enemy):
    def __init__(self, pos, size):
        super().__init__(pos, size)

    def find_player(self, player_rect):
        # Achara o lado em que o player está em relação ao inimigo

        if player_rect.right - 10 >= self.rect.right:
            self.direction = 1
        elif player_rect.left + 10 <= self.rect.left:
            self.direction = -1

        return self.direction

    def chase_player(self, player_rect):
        # Move na direção do player

        direction = self.find_player(player_rect)
        self.move(direction)
    
    def enemy_logic(self, player_rect):
        self.state_controller(player_rect)
    
    def state_controller(self,  player_rect):
        if abs(distance_betwewn_rects(self.rect, player_rect)) <= 300:
            # Testa se a distancia entre o player e o inimigo é 
            # menor que 300 para o inimigo correr atrás dele

            self.chase_player(player_rect)
        else:
            self.idle()


class ShooterEnemy(Enemy):
    def __init__(self, pos, size):
        super().__init__(pos, size)
    
    def shoot(self):
        pass