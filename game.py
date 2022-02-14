import pygame as pg

class Game:
    def __init__(self):
        # Inicializa pygame e o loop
        pg.init()
        self.runnning = True

        # Inicializa a tela e atribui um nome
        self.screen = pg.display.set_mode((800,600))
        pg.display.set_caption('Game')
        
        # Cria um timer para travar fps
        self.clock = pg.time.Clock()
    
    def run(self):
        # Game Loop

        while self.runnning:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
            
        pg.quit()

    def update(self):
        # Atualizar variaveis ou acionar metodos
        pass

    def draw(self):
        # Desenha as coisas na tela

        self.screen.fill('black')
        pg.display.update()

    def events(self):
        # Pega os eventos que forem acionados

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.runnning = False

if __name__ == '__main__':
    g = Game()
    g.run()