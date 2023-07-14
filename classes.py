import pygame as pg
from pygame.math import Vector2
from pygame.sprite import AbstractGroup

#player sprite that moves uniformly in steps from one cell to another
class Player():

	def __init__(self,x = 3,y = 8):
		self.image = pg.Surface((50,50))
		self.image.set_colorkey((0,0,0))
		
		pg.draw.circle(self.image,(255,0,0),(25,25),15)
		self.rect = self.image.get_rect(topleft = (x*50,y*50))
		self.pos = Vector2(x,y)

		self.moving = False
		self.vel = Vector2(0,0)
		self.target = Vector2(0,0)

	def move(self,direction):
		if not self.moving:
			if direction == "up":
				if self.pos.y > 0:
					self.target = self.pos + Vector2(0,-1)
					self.vel = Vector2(0,-1/30)
			elif direction == "down":
				if self.pos.y < 8:
					self.target = self.pos + Vector2(0,1)
					self.vel = Vector2(0,1/30)
			elif direction == "left":
				if self.pos.x > 0:
					self.target = self.pos + Vector2(-1,0)
					self.vel = Vector2(-1/30,0)
			elif direction == "right":
				if self.pos.x < 6:
					self.target = self.pos + Vector2(1,0)
					self.vel = Vector2(1/30,0)

		
			self.moving = True

	def update(self,surface):
		if self.moving:
			if (self.target - self.pos).length() < 0.05:
				self.pos = self.target
				self.moving = False
			self.pos  = self.pos + (self.target - self.pos) * 0.3
		else:
			self.moving = False
			self.vel = Vector2(0,0)
		self.rect.topleft = self.pos*50
		surface.blit(self.image,self.rect)


class TxtButton():
	def __init__(self, x, y, txt, color, font):
		self.label = font.render(txt, True, color)
		self.rect = self.label.get_rect(center = (x,y))
		self.clicked = False
	
	def update(self,surface,pos):
		action  = False
		if self.rect.collidepoint(pos):
			action = True
		surface.blit(self.label,self.rect)
		return action

