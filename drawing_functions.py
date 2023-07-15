import pygame as pg
import drawing_functions as df
def draw_bg(surface):
	surface.fill('#baf9ff')
	pg.draw.rect(surface,'#a4eeff',(0,0,350,450),5)
	for x,y in [(i,j) for i in range(7) for j in range(9) if (i+j)%2]:
		pg.draw.rect(surface,'#a4eeff',(50*x,50*y,50,50))

def draw_menu_bg(surface):
	surface.fill('#d8fcff')
	for x,y in [(i,j) for i in range(7) for j in range(10) if (i+j)%2]:
		pg.draw.rect(surface,'#bef3ff',(50*x,50*y,50,50))

def draw_txt(surface,txt,x,y,color,font,align = "center"):
	label = font.render(txt, True, color)
	rect = label.get_rect(center = (x,y)) if align == "center" else label.get_rect(midleft = (x,y))
	surface.blit(label,rect)

def fade_to(surface,color,duration):
	surf = pg.Surface((700,500))
	surf.fill(color)
	for i in range(60):
		surf.set_alpha(int(17))
		surface.blit(surf,(0,0))
		pg.display.flip()
		pg.time.delay(int(duration * 1000/60))

def draw_ui(surface,font:pg.font.Font,level,score,lives):
	score = 'Score: ' + str(score)
	level = 'Level: ' + str(level)

	draw_txt(surface,str(level),210,465,(0,0,0),font,'')
	draw_txt(surface,str(score),210,490,(0,0,0),font,'')
	

	for i in range(lives):
		rect = pg.Rect(60 + 25*i,470,20,20)
		pg.draw.rect(surface,(255,0,0),rect,0,5)



