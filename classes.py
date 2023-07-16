import pygame as pg
from pygame.math import Vector2
from pygame.sprite import AbstractGroup

#player sprite that moves uniformly in steps from one cell to another
class Player():

	def __init__(self,x = 3,y = 8):
		self.image = pg.image.load("assets/images/player.png")
		self.pos = Vector2(x,y)
		self.rect = self.image.get_rect(center = self.pos*50 + Vector2(25,25))
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
		self.rect.center = self.pos*50 + Vector2(25,25)
		#draw a dot at the target
		pg.draw.circle(surface,(255,0,0),self.target*50 + Vector2(25,25),5)
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
	def __init__(self,type:str,positions:list[list[int,int]],speed:int):
		self.type = type
		self.positions = positions
		self.speed = speed

		self.image = pg.image.load(f"assets/images/{self.type}.png")
		self.rect = self.image.get_rect()

		self.counter = 0
		
		self.pos = Vector2(self.positions[self.counter])
		self.tgt = Vector2(self.positions[1])

	#moves the enemy from one position (using interpolation like the player class) to another cycling through the positions list. also draws the sprite
	def update(self,surface):
		if (self.tgt - self.pos).length() < 0.05:
			self.pos = self.tgt
			self.positions.append(self.positions.pop(0))
			self.tgt = Vector2(self.positions[0])
		self.pos  = self.pos + (self.tgt - self.pos) * 0.3
		self.rect.center = self.pos*50 + Vector2(25,25)
		surface.blit(self.image,self.rect)