import pygame as pg
import drawing_functions as df
def draw_bg(surface):
	surface.fill('#baf9ff')
	for x,y in [(i,j) for i in range(7) for j in range(9) if (i+j)%2]:
		pg.draw.rect(surface,'#a4eeff',(50*x,50*y,50,50))

def draw_menu_bg(surface):
	surface.fill('#d8fcff')
	for x,y in [(i,j) for i in range(7) for j in range(9) if (i+j)%2]:
		pg.draw.rect(surface,'#bef3ff',(50*x,50*y,50,50))

def draw_txt(surface,txt,x,y,color,font):
	label = font.render(txt, True, color)
	rect = label.get_rect(center = (x,y))
	surface.blit(label,rect)

def fade_to(surface,color,duration):
	surf = pg.Surface((700,450))
	surf.fill(color)
	for i in range(60):
		surf.set_alpha(int(17))
		surface.blit(surf,(0,0))
		pg.display.flip()
		pg.time.delay(int(duration * 1000/60))
