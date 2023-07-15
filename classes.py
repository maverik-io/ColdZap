import pygame as pg
from pygame.math import Vector2
from pygame.sprite import AbstractGroup

#player sprite that moves uniformly in steps from one cell to another
class Player():

	def __init__(self,x = 3,y = 8):
		self.image = pg.Surface((50,50))
		self.image.set_colorkey((0,0,0))
		
		pg.draw.circle(self.image,(0, 141, 159),(25,25),15)
		self.rect = self.image.get_rect(topleft = (x*50,y*50))
		self.pos = Vector2(x,y)

		self.moving = False
		self.vel = Vector2(0,0)
		self.target = self.pos
		self.targets = []

	def move(self,direction):
		if len(self.targets) < 2:
			if direction == "up":
				if self.pos.y > 0:
					self.targets.append([(self.targets[0][0] + Vector2(0,-1)) if any(self.targets) else self.target + Vector2(0,-1),Vector2(0,-1)])
			elif direction == "down":
				if self.pos.y < 8:
					self.targets.append([(self.targets[0][0] + Vector2(0,1)) if any(self.targets) else self.target + Vector2(0,1),Vector2(0,1)])
			elif direction == "left":
				if self.pos.x > 0:
					self.targets.append([(self.targets[0][0] + Vector2(-1,0)) if any(self.targets) else self.target + Vector2(-1,0),Vector2(-1,0)])
			elif direction == "right":
				if self.pos.x < 6:
					self.targets.append([(self.targets[0][0] + Vector2(1,0)) if any(self.targets) else self.target + Vector2(1,0),Vector2(1,0)])
		print(self.targets)



	def update(self,surface):
		if self.moving:
			if (self.target - self.pos).length() < 0.05:
				self.pos = self.target
				self.moving = False
			self.pos  = self.pos + (self.target - self.pos) * 0.3
		else:
			if any(self.targets):
				target = self.targets.pop(0)
				if -1 < target[0].x < 7 and -1 < target[0].y < 9:
					self.target = target[0]
					self.moving = True
					self.vel = self.target[1] * 0.03
			self.vel = Vector2(0,0)
			self.tgt = self.pos
		self.rect.topleft = self.pos*50
		surface.blit(self.image,self.rect)


class TxtButton():
	def __init__(self, x, y, txt, color, font):
		self.label = font.render(txt, True, color)
		self.rect = self.label.get_rect(center = (x,y))
		self.bgrect = self.rect.inflate(10,10)
		self.clicked = False
	
	def update(self,surface,pos):
		action  = False

		mp = pg.mouse.get_pos()
		if self.rect.collidepoint(mp):
			pg.draw.rect(surface,'#dddddd',self.bgrect)
		if self.rect.collidepoint(pos):
			action = True
		surface.blit(self.label,self.rect)
		return action

class Enemy():
	def __init__(self,type:str,posA:Vector2,posB:Vector2,speed:int):
		self.type = type
		self.posA = posA
		self.posB = posB
		self.speed = speed

		self.image = pg.Surface((50,50))
		self.image.set_colorkey((0,0,0))
		pg.draw.circle(self.image,(255,0,0),(25,25),15)
		self.rect = self.image.get_rect(topleft = self.posA*50)
		self.pos = self.posA
		self.tgt = self.posB

	def update(self,surface):
		self.vel = (self.tgt-self.pos).normalize() * self.speed * 0.03
		self.pos = self.pos + self.vel
		if (self.pos - self.tgt).length() < 0.05:
			self.pos = self.tgt
			self.tgt = self.posA if self.tgt == self.posB else self.posB
		
		self.rect.topleft = self.pos*50
		surface.blit(self.image,self.rect)