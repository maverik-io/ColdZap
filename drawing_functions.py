import pygame as pg

def draw_bg(screen):
	screen.fill('#66e40c')
	for x,y in [(i,j) for i in range(7) for j in range(9) if (i+j)%2]:
		pg.draw.rect(screen,'#6aff00',(50*x,50*y,50,50))