from csv import reader
import pygame as pg
from main.utils.settings import TILE_SIZE

def import_csv(path):
    layout = []
    with open(path) as csv_file:
        map = reader(csv_file,  delimiter=',')
        for row in map:
            layout.append(list(row))
        return layout

def import_sprites(path):
    full_image = pg.image.load(path).convert_alpha()
    qtd_sprite_x = full_image.get_size()[0] // TILE_SIZE
    qtd_sprite_y = full_image.get_size()[1] // TILE_SIZE

    separated_sprites = []
    for row in range(qtd_sprite_x):
        for col in range(qtd_sprite_y):
            x = col * TILE_SIZE
            y = row * TILE_SIZE

            sprite = pg.Surface((TILE_SIZE, TILE_SIZE), flags=pg.SRCALPHA)
            sprite.blit(full_image, (0,0), pg.Rect(x,y, TILE_SIZE, TILE_SIZE))

            separated_sprites.append(sprite)
    
    return separated_sprites


if __name__ == '__main__':
    pg.init()
    a = pg.display.set_mode((400,400))
    print(import_sprites('./main/assets/terrain_tileset.png'))
    pg.quit()
