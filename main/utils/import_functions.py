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

def import_sprites(path, tile_size=TILE_SIZE):
    full_image = pg.image.load(path).convert_alpha()
    qtd_sprite_x = full_image.get_size()[0] // tile_size
    qtd_sprite_y = full_image.get_size()[1] // tile_size

    separated_sprites = []
    for col in range(qtd_sprite_y):
        for row in range(qtd_sprite_x):
            x = row * tile_size
            y = col * tile_size

            sprite = full_image.subsurface(
                    pg.Rect(x,y, tile_size, tile_size)
                    )

            new_sprite = pg.Surface(
                (tile_size, tile_size), flags=pg.SRCALPHA
                )
            new_sprite.blit(sprite, (0,0))
            
            separated_sprites.append(new_sprite)
    
    return separated_sprites


if __name__ == '__main__':
    pg.init()
    a = pg.display.set_mode((400,400))
    print(import_sprites('./main/assets/terrain_tileset.png'))
    pg.quit()
