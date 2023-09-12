import pygame as pg
from pygame.math import Vector2
import utils

SCALE = utils.SCALE

PlayerPos = Vector2(3, 8)


class Player:
    def __init__(self, x=3, y=8, health=5):
        global PlayerPos
        self.image = pg.image.load(f"assets/images/{SCALE}x/player.png")
        self.pos = Vector2(x, y)
        self.rect = self.image.get_rect(
            center=self.pos * 50 * SCALE + Vector2(25, 25) * SCALE
        )
        self.moving = False
        self.vel = Vector2(0, 0)
        self.target = self.pos
        self.targets = []
        self.mask = pg.mask.from_surface(self.image)
        self.health = health
        self.counter = 0
        self.hit = False

    def move(self, direction):
        match direction:
            case "up":
                self.targets.append(Vector2(0, -1))
            case "down":
                self.targets.append(Vector2(0, 1))
            case "left":
                self.targets.append(Vector2(-1, 0))
            case "right":
                self.targets.append(Vector2(1, 0))

    def wallcheck(self, direction, pos=None):
        if pos == None:
            pos = self.pos

        for i in utils.Collidable_list:
            if i.pos == pos + direction:
                return False
        return True

    def update(self, surface):
        global PlayerPos

        if self.moving:
            if (self.target - self.pos).length() < 0.05:
                self.pos = self.target
                self.moving = False
            self.pos = self.pos + (self.target - self.pos) * 0.3
        else:
            if len(self.targets) != 0:
                direction = self.targets.pop(0)
                target = self.pos + direction
                if (
                    -1 < target.x < 7
                    and -1 < target.y < 9
                    and self.wallcheck(direction)
                ):
                    self.target = target
                    self.moving = True
            self.tgt = self.pos
        PlayerPos = self.pos
        self.rect.center = self.pos * 50 * SCALE + Vector2(25, 25) * SCALE

        self.collision()
        self.shoot_stuff()

        surface.blit(self.image, self.rect)

    def shoot_stuff(self):
        try:
            if self.counter > 10:
                for enemy in utils.Enemylist:
                    if self.pos.x == enemy.tgt.x or self.pos.y == enemy.tgt.y:
                        utils.Bulletlist.append(
                            utils.Bullet(
                                self.pos,
                                (enemy.tgt - self.pos).normalize() * 20,
                                "blue",
                            )
                        )
                        self.counter = 0
            self.counter += 1
        except:
            pass

    def collision(self):
        for i in utils.Bulletlist:
            if i.type == "red":
                if self.mask.overlap(
                    i.mask,
                    (
                        int(i.pos.x - self.pos.x * 50 * SCALE),
                        int(i.pos.y - self.pos.y * 50 * SCALE),
                    ),
                ):
                    self.hit = True
                    utils.Bulletlist.remove(i)
                    self.health -= 1
