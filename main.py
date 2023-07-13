import pygame as pg
import sys
from pygame.math import Vector2

import drawing_functions as df

pg.init()
screen = pg.display.set_mode((350,450))

quit = False



while not quit:
	quit = pg.event.get(pg.QUIT)

	
	df.draw_bg(screen)
	
	pg.display.flip()
	
pg.quit()
sys.exit()
