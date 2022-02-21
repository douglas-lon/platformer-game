import pygame as pg
from main.utils.settings import GRAVITY, ACCELERATION, FRICTION

class Player(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()

        self.image = pg.Surface((size,size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.size = (size + 1, size + 1)

        self.position = pg.math.Vector2(self.rect.midbottom)
        self.velocity = pg.math.Vector2(0,0)
        self.direction = 0

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

        
        acceleration = ACCELERATION * self.direction
        acceleration += self.velocity.x * FRICTION
        
        self.velocity.x += acceleration

        if abs(self.velocity.x) < 0.18:
            self.velocity.x = 0
        
        self.position += pg.math.Vector2(self.velocity.x + 0.5 * acceleration,self.velocity.y)

        self.rect.midbottom = self.position 
    
    def apply_gravity(self, dt):
        self.velocity.y += GRAVITY * dt

    def jump(self):
        if self.jumping and self.jump_counter <= self.max_jump_counter:
            self.jump_counter += 1
            self.velocity.y = -9
        else:
            self.jumping = False

    def update(self, dt):
        self.input_handler()
        self.jump()
        self.movement(dt)
    
    def draw(self, surface, offset):
        offset_rect = pg.Rect((self.rect.x - offset.x, self.rect.y - offset.y), self.image.get_size())
        surface.blit(self.image, offset_rect)
    
