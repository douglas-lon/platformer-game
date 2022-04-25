import pygame as pg

class UI:
    def __init__(self, path):
        self.image = pg.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft=(0,5))

    def draw(self, surface, player_health,):

        health_percentage = ((self.rect.size[0] - 94) * player_health) / 100
        pg.draw.rect(surface, pg.Color(234,182,118), pg.Rect((60, 20), (self.rect.size[0] - 94, self.rect.size[1] - 29)))
        pg.draw.rect(surface, 'red', pg.Rect((60, 20), (health_percentage, self.rect.size[1] - 29)))
        surface.blit(self.image, self.rect)
        