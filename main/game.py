import pygame as pg
from main.menu.menus import SimpleMenu
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

        self.menus = SimpleMenu(48, self.screen)
        
        self.player_health = 100
        # Cria um timer para travar fps
        self.clock = pg.time.Clock()
        self.current_level = -1
        self.level = Level(self.current_level, self.player_health)
        self.max_level = 0
    
    def change_current_level(self, index):
        del self.level

        self.level = Level(index, self.player_health)
    
    def run(self):
        # Game Loop

        self.menus.menu("HeHe Adventure", 'Press Any Key To Start', 'green', 'brown')

        while self.runnning:
            self.last_tick = self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
            level_index = self.level.change_level()
            
            if level_index != '' and level_index <= self.max_level:
                self.change_current_level(level_index)
            
            if self.level.end:
                self.menus.menu('The End', 'Press Any Key To Close the Game', 'green', 'brown')
                self.runnning = False

        pg.quit()

    def update(self):
        # Atualizar variaveis ou acionar metodos
        self.level.update(self.last_tick/1000)

        if self.level.restart:
            self.menus.menu('You Died', 'Press Any Key To Restart', 'green', 'brown')
            self.change_current_level(self.current_level)

    def draw(self):
        # Desenha as coisas na tela
        self.screen.fill('lightblue')
        self.level.draw(self.screen)
        pg.display.update()

    def events(self):
        # Pega os eventos que forem acionados

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.runnning = False
