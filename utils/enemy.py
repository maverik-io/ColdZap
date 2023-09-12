import pygame as pg
from pygame.math import Vector2
from utils import Bulletlist, SCALE

from .bullet import Bullet 
from . import player

Enemylist = []

class Enemy:
    def __init__(self, type: str, positions: list[list[int, int]], ):
        self.type = type
        self.positions = positions + positions[::-1]

        self.image = pg.image.load(f"assets/images/{SCALE}x/{self.type}.png")
        self.rect = self.image.get_rect()

        self.counter = 0

        self.mask = pg.mask.from_surface(self.image)

        self.pos = Vector2(self.positions[self.counter])
        self.tgt = Vector2(self.positions[1])

        self.health = 5

        Enemylist.append(self)

    def update(self, surface):
        if self.counter > 120:
            self.counter = 0
            Bulletlist.append(Bullet(self.pos, (player.PlayerPos - self.pos).normalize() * 2))

        self.counter += 1

        if (self.tgt - self.pos).length() < 0.05:
            self.pos = self.tgt
            self.positions.append(self.positions.pop(0))
            self.tgt = Vector2(self.positions[0])
        self.pos = self.pos + (self.tgt - self.pos) * 0.1
        self.rect.center = self.pos * 50*SCALE + Vector2(25, 25)*SCALE
        surface.blit(self.image, self.rect)
        
        self.collision()
        if self.health <= 0:
            try:
                Enemylist.remove(self)
                return True
            except Exception as e:
                pass

    def collision(self):
        for i in Bulletlist:
            if i.type == "blue":
                if self.mask.overlap(i.mask, (int(i.pos.x- self.pos.x * 50*SCALE), int(i.pos.y - self.pos.y * 50*SCALE))):
                    Bulletlist.remove(i)
                    self.health -= 1