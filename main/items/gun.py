import pygame as pg
from main.items.bullet import Bullet


class Gun(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pg.Surface((30,20))
        #self.image.fill('blue')
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.size = (20, 10)
        self.bullets = pg.sprite.Group()
        self.change = False
        self.bullet_distance = 400
        self.time = 30

    def update_pos(self, pos, direction):
        self.time += 1
        if direction > 0:
            offset = 30
            self.change = False
        else:
            offset = - 60
            self.change = True

        self.rect.x = pos[0] + offset
        self.rect.y = pos[1] - 10

        self.manage_bullets()

    def fire(self):
        vel = 7
        if self.time >= 30:
            if self.change:
                self.bullets.add(Bullet(self.rect.topleft, -vel))
            else:
                self.bullets.add(Bullet(self.rect.topright, vel))
            self.time = 0
            print('pow', len(self.bullets))

    def manage_bullets(self):
        if self.bullets:
            for bullet in self.bullets:
                if bullet.init_pos[0] - self.bullet_distance > bullet.rect.centerx or bullet.init_pos[0] + self.bullet_distance < bullet.rect.centerx:
                    self.bullets.remove(bullet)

                bullet.update()

    def draw(self, surface, offset):
        # Desenha na tela o player baseado no offset
        #offset_rect = pg.Rect(
        #    (self.rect.x - offset.x, self.rect.y - offset.y), 
        #    self.image.get_size()
        #    )
        #surface.blit(self.image, offset_rect)

        if self.bullets:
            for bullet in self.bullets:
                bullet.draw(surface, offset)
