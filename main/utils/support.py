from math import sqrt, hypot

def distance_betwewn_rects(rect1, rect2):
    return sqrt((rect2.centerx - rect1.centerx)**2+(rect2.centery - rect1.centery)**2)

def distance_betwewn_rects_poor(rect1, rect2):
    return rect2.centerx - rect1.centerx


if __name__ == '__main__':
    from pygame import Rect
    r1 = Rect(656, 200, 60, 60)
    r2 = Rect(663, 223, 60, 60)
    print(distance_betwewn_rects(r1, r2))
    print(hypot(r2.centerx-r1.centerx, r2.centery - r1.centery))