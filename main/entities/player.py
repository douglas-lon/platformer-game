import pygame as pg
from main.utils.support import lerp

class Player(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        self.image = pg.Surface((size,size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.size = (size + 1, size + 1)

        self.position = pg.math.Vector2(self.rect.midbottom)
        self.velocity = pg.math.Vector2(0,0)
        self.gravity = 40
        self.direction = 0
        self.speed = 8
        self.acceleration = 0.1
        self.friction = 0.2

        self.jump_counter = 0
        self.jumping = False
        self.max_jump_counter = 20
        self.on_ground = False

    def input_handler(self):
        keys = pg.key.get_pressed()

        self.direction = 0
        if keys[pg.K_RIGHT]:
            self.direction = 1
        elif keys[pg.K_LEFT]:
            self.direction = -1

        if keys[pg.K_SPACE] and self.on_ground:
            self.jumping = True
        else:
            self.jumping = False
            self.on_ground = False
            self.jump_counter = 0

    def movement(self, dt):
        self.apply_gravity(dt)

        if self.direction != 0:
            self.velocity.x = lerp(self.velocity.x, self.direction * self.speed, self.acceleration)
            print(self.velocity.x)
        else:
            self.velocity.x = lerp(self.velocity.x, 0, self.friction)

        self.position += self.velocity 
        
        self.rect.midbottom = self.position 
    
    def apply_gravity(self, dt):
        self.velocity.y += self.gravity * dt

    def jump(self):
        if self.jumping and self.jump_counter <= self.max_jump_counter:
            self.jump_counter += 1
            self.velocity.y = -8
        else:
            self.jumping = False

    def update(self, dt):
        self.input_handler()
        self.jump()
        self.movement(dt)
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
    
