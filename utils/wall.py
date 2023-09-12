import pygame as pg
from pygame.math import Vector2
from utils import Bulletlist, Collidable_list, SCALE

class Wall:
    def __init__(self,pos):
        x,y = pos
        self.image = pg.image.load(f"assets/images/{SCALE}x/wall.png")
        self.pos = Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos * 50*SCALE + Vector2(25, 25)*SCALE)
        self.mask = pg.mask.from_surface(self.image)
        Collidable_list.append(self)

    def update(self, surface):
        #set the color of the wall to red if a bullet hits it
        for i in Bulletlist:
            if self.mask.overlap(i.mask, (int(i.pos.x- self.pos.x * 50*SCALE), int(i.pos.y - self.pos.y * 50*SCALE))):
                Bulletlist.remove(i)

        surface.blit(self.image, self.rect)