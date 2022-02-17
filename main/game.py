import pygame as pg
from main.utils.settings import *
from main.world.level import Level


class Game:
    def __init__(self):
        # Inicializa pygame e o loop
        pg.init()
        self.runnning = True

        # Inicializa a tela e atribui um nome
        self.screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGTH))
        pg.display.set_caption('Platformer Game')
        
        # Cria um timer para travar fps
        self.clock = pg.time.Clock()
        self.level = Level(-1)
    
    def run(self):
        # Game Loop

        while self.runnning:
            self.last_tick = self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
            
        pg.quit()

    def update(self):
        # Atualizar variaveis ou acionar metodos
        self.level.update(self.last_tick/1000)

    def draw(self):
        # Desenha as coisas na tela
        self.screen.fill('grey')
        self.level.draw(self.screen)
        pg.display.update()

    def events(self):
        # Pega os eventos que forem acionados

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.runnning = False
