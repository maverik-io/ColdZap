import pygame as pg
import sys
from pygame.math import Vector2

import drawing_functions as df
import classes as cl


pg.init()
screen = pg.display.set_mode((350,450))

quit = False
player = cl.Player()
clock = pg.time.Clock()


Comfortaa = pg.font.Font("assets/fonts/Comfortaa.ttf", 60)
Comfortaa_small = pg.font.Font("assets/fonts/Comfortaa.ttf", 20)

def main():

	global quit

	def event_handler():

		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_UP or event.key == pg.K_w:
					player.move("up")
				elif event.key == pg.K_DOWN or event.key == pg.K_s:
					player.move("down")
				elif event.key == pg.K_LEFT or event.key == pg.K_a:
					player.move("left")
				elif event.key == pg.K_RIGHT or event.key == pg.K_d:
					player.move("right")
				elif event.key == pg.K_ESCAPE or event.key == pg.K_q:
					return True
				


	while not quit:
		clock.tick(60) 
		quit = pg.event.get(pg.QUIT) or event_handler() #quit if window is closed or event_handler returns True

		df.draw_bg(screen) #draw background

		player.update(screen) #update player

		pg.display.flip()
		
	pg.quit()
	sys.exit()

def menu():
	global quit

	def event_handler():
		for event in pg.event.get():
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE or event.key == pg.K_q:
					return True
				elif event.key == pg.K_RETURN:
					return False
				
	new_game = cl.TxtButton(175,200,"New Game",(0,0,0),Comfortaa_small)
	load_game = cl.TxtButton(175,250,"Load Game",(0,0,0),Comfortaa_small)
	view_highscore = cl.TxtButton(175,300,"Highscores",(0,0,0),Comfortaa_small)
	quit_game = cl.TxtButton(175,350,"Quit",(0,0,0),Comfortaa_small)
	

	while not quit:
		clock.tick(60) 

		quit = pg.event.get(pg.QUIT) or event_handler() #quit if window is closed or event_handler returns True

		df.draw_menu_bg(screen) #draw background
		mouse_pos = pg.mouse.get_pos() if pg.mouse.get_pressed()[0] else (0,0) #get mouse position if mouse is pressed, else (0,0)

		df.draw_txt(screen,"ColdZap",175,100,(0,0,0),Comfortaa)


		if quit_game.update(screen,mouse_pos): break
		if load_game.update(screen,mouse_pos): return load
		if view_highscore.update(screen,mouse_pos): return highscore
		if new_game.update(screen,mouse_pos):
			df.fade_to(screen,(0,0,0),0.25)
			return main


		pg.display.flip()
		
	pg.quit()
	sys.exit()


def load():
	return menu

def highscore():
	return menu

if __name__ == "__main__":
	active_screen = menu
	while True:
		 active_screen = active_screen()


