import pygame as pg
from pygame.math import Vector2

LEVEL_ID = 0

SCALE = 1.7
pg.init()
screen = pg.display.set_mode((int(350*SCALE),int(450*SCALE)))

TILE_TYPES = ['W','P','O','E','AE','G']

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.txt = ''
        self.rect = pg.Rect(10 + self.x*40*SCALE, 70 + self.y*40*SCALE, 40*SCALE, 40*SCALE)
    def update(self):
        hover = True if self.rect.collidepoint(pg.mouse.get_pos()) else False
        if hover: pg.draw.rect(screen, '#222222', self.rect)
        pg.draw.rect(screen, 'white', self.rect,1)

class TileSelector:
    def __init__(self,x,y,txt):
        self.x = x
        self.y = y
        self.txt = txt
        self.rect = pg.Rect(30 + self.x*40*SCALE, 70 + self.y*45*SCALE, 40*SCALE, 40*SCALE)

    def update(self):
        hover = True if self.rect.collidepoint(pg.mouse.get_pos()) else False
        if hover: pg.draw.rect(screen, '#222222', self.rect)
        pg.draw.rect(screen, 'red', self.rect,1)

        label = pg.font.SysFont('Arial', int(20*SCALE)).render(self.txt, True, 'red')
        labelrect = label.get_rect(center=self.rect.center)
        screen.blit(label, labelrect)


TILES = [Tile(x,y) for x in range(7) for y in range(9)]
TILE_SELECTORS = [TileSelector(7,y,txt) for y,txt in enumerate(TILE_TYPES)]

while True:
    screen.fill('black')
    for tile in TILES+TILE_SELECTORS:
        tile.update()

    pg.display.flip()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()