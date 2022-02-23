import pygame as pg
from main.utils.settings import GRAVITY, ACCELERATION, FRICTION

class Player(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        
        # Cria surface com o tamanho desejado e coloca ela na posição
        self.image = pg.Surface((size,size))
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft=pos)
        self.rect.size = (size, size +1)

        # Inicializa Vetor para posição e velocidade, 
        # cria variavel para direção
        self.position = pg.math.Vector2(self.rect.midbottom)
        self.velocity = pg.math.Vector2(0,0)
        self.direction = 0

        # Cria um contador para o tempo do jump e o limite,
        #  junto com variaveis booleanas para impedir double jump
        self.jump_counter = 0
        self.jumping = False
        self.max_jump_counter = 20
        self.on_ground = False

        # Onde o player está colididindo
        self.collided_side = pg.K_p
        self.collided_rect = ''

    def input_handler(self):
        # Cuida dos iputs '-'
        keys = pg.key.get_pressed()

        can = False
        if self.collided_rect != '':
            if self.rect.bottom < self.collided_rect.top:
                can = True

        self.direction = 0
        if keys[pg.K_RIGHT] and self.collided_side != pg.K_RIGHT:
            self.direction = 1
        elif keys[pg.K_LEFT] and  self.collided_side != pg.K_LEFT:
            self.direction = -1

        if keys[pg.K_SPACE] and self.on_ground:
            self.jumping = True
        else:
            self.jumping = False
            self.on_ground = False
            self.jump_counter = 0

        if not keys[self.collided_side] or can:
            self.collided_side = pg.K_p
    
        
    
    def apply_gravity(self, dt):
        # Aplica uma gravidade na velocidade y
        # Que é determinada por uma constante e o delta time
        self.velocity.y += GRAVITY * dt
        

    def movement(self, dt):
        self.apply_gravity(dt)

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
        # Nomes das variaveis explica o que ta acontecendo
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

        # Desenha na tela o player baseado no offset
        offset_rect = pg.Rect(
            (self.rect.x - offset.x, self.rect.y - offset.y), 
            self.image.get_size()
            )
        surface.blit(self.image, offset_rect)
    
