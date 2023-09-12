import pygame as pg
from pygame.math import Vector2
from utils import Collidable_list, SCALE

class Pit:
    def __init__(self,pos):
        x,y = pos
        self.image = pg.image.load(f"assets/images/{SCALE}x/pit.png")
        self.pos = Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos * 50*SCALE + Vector2(25, 25)*SCALE)
        self.mask = pg.mask.from_surface(self.image)
        Collidable_list.append(self)

    def update(self, surface):
        surface.blit(self.image, self.rect)