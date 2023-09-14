import pygame as pg
from pygame.math import Vector2
from utils import SCALE

Bulletlist = []

"""
This file contains the bullet class.
"""


class Bullet:
    """
    Class for the bullets in the game.

    :param pos: The position of the bullet.
    :param vel: The velocity of the bullet. Vector stores both direction and speed.
    :param type: The type of the bullet.
    """

    def __init__(self, pos, vel, type="red"):
        self.type = type
        self.image = pg.image.load(f"assets/images/{SCALE}x/{type}-bullet.png")
        self.pos = pos * 50 * SCALE + Vector2(25, 25) * SCALE
        self.vel = vel * SCALE
        self.dir = vel.angle_to(Vector2(0, -1))
        self.rect = self.image.get_rect(
            center=self.pos * 50 * SCALE + Vector2(25, 25) * SCALE
        )
        self.mask = pg.mask.from_surface(self.image)

    def update(self, surface):
        tempimage = pg.transform.rotate(self.image, self.dir)
        self.pos += self.vel
        self.rect.center = self.pos
        surface.blit(tempimage, self.rect)

        if not (0 < self.pos.x < 7 * SCALE * 50 and 0 < self.pos.y < 9 * SCALE * 50):
            return True
