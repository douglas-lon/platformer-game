from random import choice
import pygame as pg
from main.utils.settings import GRAVITY, ACCELERATION, FRICTION, TILE_SIZE
from main.items.gun import Gun
from main.utils.import_functions import import_sprites

class Player(pg.sprite.Sprite):
    def __init__(self, pos, size, health=100):
        super().__init__()
        
        # Cria surface com o tamanho desejado e coloca ela na posição
        #self.idle_frames = import_sprites('./main/assets/imgs/idle.png', 54)
        #self.run_frames = import_sprites('./main/assets/imgs/run.png', 54)
        #print(self.idle_frames)
        self.create_sprites()

        self.image = self.animated_frames['idle'][0]
            
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.size = (size, size)

        # Inicializa Vetor para posição e velocidade, 
        # cria variavel para direção
        self.position = pg.math.Vector2(self.rect.midbottom)
        self.velocity = pg.math.Vector2(0,0)
        self.direction = 0
        self.facing = 1

        self.animation_speed = 0.15
        self.current_frame = 0
        self.status = 'idle'

        self.jumping = False
        self.jump_count = 0
        # Cria um contador para o tempo do jump e o limite,
        #  junto com variaveis booleanas para impedir double jump
        self.on_ground = False
        self.gun = Gun((264,60))
        self.health = health

        self.invicible = False
        self.invincibility_time = 0
        self.knock_side = 0
        self.knock_distance = 0

        self.items = []
    
    def create_sprites(self):
        self.animated_frames = {
            'idle':[],
            'run': [],
            'jump': [],
            'landing': []
        }

        for i in self.animated_frames.keys():
            self.animated_frames[i] = import_sprites(f'./main/assets/imgs/{i}.png', 54)

    def animate(self):
        self.get_status()

        self.current_frame += self.animation_speed

        if self.current_frame > len(self.animated_frames[self.status]):
            self.current_frame = 0
        
        self.image = self.animated_frames[self.status][int(self.current_frame)]

        if self.invicible:
            disappear = choice([255, 0])
            self.image.set_alpha(disappear)
        else:
            self.image.set_alpha(255)

    def get_status(self):
        
        if self.velocity.y < 0:
            self.status = 'jump'
        elif self.velocity.y > 0:
            self.status = 'landing'
        else:
            if self.direction != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def input_handler(self):
        # Cuida dos iputs '-'
        keys = pg.key.get_pressed()

        self.direction = 0
        if keys[pg.K_RIGHT]:
            self.direction = 1
            self.facing = 1
        elif keys[pg.K_LEFT]:
            self.direction = -1
            self.facing = 0

        if keys[pg.K_SPACE]:
            self.jump()

        if keys[pg.K_z]:
            self.gun.fire()
        
        self.on_ground = False
    
    
    def apply_gravity(self, dt):
        # Aplica uma gravidade na velocidade y
        # Que é determinada por uma constante e o delta time
        self.velocity.y += GRAVITY * dt

    def movement(self):
        #self.apply_gravity(dt)

        # Define para que lado ele ira acelerar
        # E adiciona na aceleração a velocidade atual 
        # * a constante de fricção
        acceleration = ACCELERATION * self.direction
        acceleration += self.velocity.x * FRICTION
        
        self.velocity.x += acceleration

        # A velocidade x nunca é 0 por isso 
        # é necessario transforma-la em zero
        if abs(self.velocity.x) < 0.18:
            self.velocity.x = 0
        
        # Adiciona na posição a velocidade calculada 
        # mais a metade da aceleração atual, junto com o y com gravidade
        self.position += pg.math.Vector2(
                self.velocity.x + 0.5 * acceleration,
                self.velocity.y)

        self.rect.midbottom = self.position 

    def jump(self):
        if self.jump_count <= 20:
            self.velocity.y -= 2
            self.jump_count += 2

    def on_bottom_collision(self, rect):
        if self.velocity.y > 0:
            self.rect.bottom = rect.top
            self.position.y = rect.top
            self.velocity.y = 0
            self.on_ground = True

    def on_top_collision(self, rect):
        self.rect.top = rect.bottom
        self.position.y = rect.bottom + TILE_SIZE
        self.velocity.y = 0

    def on_left_collision(self, rect):
        x = (rect.right + self.rect.width / 2) 
        self.position.x = x + 2
        self.velocity.x = 0

    def on_right_collision(self, rect):
        x = (rect.left - self.rect.width / 2) 
        self.position.x = x - 1
        self.velocity.x = 0

    def get_knocback(self):
        if self.knock_distance < 10:
            self.velocity.y -= 2
            self.velocity.x += self.knock_side * 2

    def take_damage(self, rect_enemy):
        if  not self.invicible:
            if rect_enemy.right > self.rect.right:
                self.knock_side = -1
            elif rect_enemy.left < self.rect.left:
                self.knock_side = 1

            self.invicible = True
            self.invincibility_time = 0
            self.health -= 15
            self.knock_distance = 0
            self.jump_count = 30
            self.on_ground = False

    def update(self, dt):
        self.invincibility_time += 2
        self.knock_distance += 1

        if self.on_ground:
            self.jump_count = 0

        self.animate()
        self.input_handler()
        if not self.on_ground:
            self.apply_gravity(dt)

        
        self.movement()

        self.get_knocback()

        self.gun.update_pos(self.rect.midleft, self.facing)

        if self.invincibility_time > 100:
            self.invicible = False
    
    def draw(self, surface, offset):
        # Desenha na tela o player baseado no offset
        offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )
        surface.blit(self.image, offset_rect)
        
        self.gun.draw(surface, offset)
    
class TestPlayer(Player):
    def __init__(self, pos, size, health):
        super().__init__(pos, size, health)
        self.image = pg.Surface((size,size))
        self.image.fill('green')