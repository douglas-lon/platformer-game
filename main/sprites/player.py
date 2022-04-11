import pygame as pg
from main.utils.settings import GRAVITY, ACCELERATION, FRICTION, TILE_SIZE
from main.items.gun import Gun

class Player(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        
        # Cria surface com o tamanho desejado e coloca ela na posição
        self.image = pg.image.load(
            './main/assets/imgs/player.png'
            ).convert_alpha()
            
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.size = (size, size)

        # Inicializa Vetor para posição e velocidade, 
        # cria variavel para direção
        self.position = pg.math.Vector2(self.rect.midbottom)
        self.velocity = pg.math.Vector2(0,0)
        self.direction = 0
        self.facing = 1

        self.jumping = False
        self.jump_count = 0
        # Cria um contador para o tempo do jump e o limite,
        #  junto com variaveis booleanas para impedir double jump
        self.on_ground = False
        self.gun = Gun((264,60))

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

    def update(self, dt):
        if self.on_ground:
            self.jump_count = 0
        self.input_handler()
        if not self.on_ground:
            self.apply_gravity(dt)
        self.movement()
        self.gun.update_pos(self.rect.center, self.facing)
    
    def draw(self, surface, offset):
        # Desenha na tela o player baseado no offset
        offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )
        surface.blit(self.image, offset_rect)
        self.gun.draw(surface, offset)
    
class TestPlayer(Player):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        self.image = pg.Surface((size,size))
        self.image.fill('green')