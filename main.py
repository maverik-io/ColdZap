import pygame as pg
import sys
from pygame.math import Vector2

pg.init()
screen = pg.display.set_mode((700,900))

quit = False

while not quit:
	quit = pg.event.get(pg.QUIT)
	screen.fill('#4e9c16')
	
	pg.display.flip()
	
pg.quit()
sys.exit()
