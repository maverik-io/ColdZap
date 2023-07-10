import pygame as pg
import sys
from pygame.math import Vector2

pg.init()
screen = pg.display.set_mode((700,900))

quit = False

while not quit:
	quit = pg.event.get(pg.QUIT)
	screen.fill('#4e9c16')
	
	for x,y in [(i,j) for i in range(7) for j in range(9) if (i+j)%2]:
		pg.draw.rect(screen,'#6acf21',(100*x,100*y,100,100))
	
	pg.display.flip()
	
pg.quit()
sys.exit()
