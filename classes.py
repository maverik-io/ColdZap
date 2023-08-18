import pygame as pg
from pygame.math import Vector2

Bulletlist = []
Enemylist = []
Collidable_list = []

PlayerPos = Vector2(0,0)

SCALE = 1.7

#---FUNCTIONS----------------------------------
def displayBullets(screen):
    for i in Bulletlist:
        if i.update(screen):
            Bulletlist.remove(i)
#----------------------------------------------
def update_enemies(screen):
    for i in Enemylist:
        i.update(screen)
#----------------------------------------------
def update_collidables(screen):
    for i in Collidable_list:
        i.update(screen)
#----------------------------------------------

#---CLASSES------------------------------------
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
#----------------------------------------------
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
#----------------------------------------------
class Player:
    def __init__(self, x=3, y=8,health=5):
        global PlayerPos
        self.image = pg.image.load(f"assets/images/{SCALE}x/player.png")
        self.pos = Vector2(x, y)
        self.rect = self.image.get_rect(center=self.pos * 50*SCALE + Vector2(25, 25)*SCALE)
        self.moving = False
        self.vel = Vector2(0, 0)
        self.target = self.pos
        self.targets = []
        PlayerPos = self.pos
        self.mask = pg.mask.from_surface(self.image)
        self.health = health
        self.counter = 0
        self.hit = False

    def move(self, direction):
        match direction:
            case "up":
                self.targets.append( Vector2(0, -1))
            case "down":
                self.targets.append( Vector2(0, 1))
            case "left":
                self.targets.append( Vector2(-1, 0))
            case "right":
                self.targets.append( Vector2(1, 0))

    def wallcheck(self, direction, pos= None):
        if pos == None:
            pos = self.pos

        for i in Collidable_list:
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
                if -1 < target.x < 7 and -1 < target.y < 9 and self.wallcheck(direction):
                    self.target = target
                    self.moving = True
            self.tgt = self.pos
        PlayerPos = self.pos
        self.rect.center = self.pos * 50*SCALE + Vector2(25, 25)*SCALE

        self.collision()
        self.shoot_stuff()

        surface.blit(self.image, self.rect)


    def shoot_stuff(self):
        try:
            if self.counter > 10:
                for enemy in Enemylist:

                    if (self.pos.x == enemy.tgt.x or self.pos.y == enemy.tgt.y):
                        Bulletlist.append(Bullet(self.pos, (enemy.tgt - self.pos).normalize() * 20, "blue"))
                        self.counter = 0
            self.counter += 1
        except:
            pass

    def collision(self):
        for i in Bulletlist:
            if i.type == "red":
                if self.mask.overlap(i.mask, (int(i.pos.x- self.pos.x * 50*SCALE), int(i.pos.y - self.pos.y * 50*SCALE))):
                    self.hit = True
                    Bulletlist.remove(i)
                    self.health -= 1
#----------------------------------------------
class TxtButton:
    def __init__(self, x, y, txt, color, font):
        self.label = font.render(txt, True, color)
        self.rect = self.label.get_rect(center=(x, y))
        self.bgrect = self.rect.inflate(10, 10)
        self.clicked = False

    def update(self, surface, pos):
        action = False

        mp = pg.mouse.get_pos()
        if self.rect.collidepoint(mp):
            pg.draw.rect(surface, "#dddddd", self.bgrect)
        if self.rect.collidepoint(pos):
            action = True
        surface.blit(self.label, self.rect)
        return action
#----------------------------------------------
class Bullet:
    def __init__(self, pos, vel, type="red"):
        self.type = type
        self.image = pg.image.load(f"assets/images/{SCALE}x/{type}-bullet.png")
        self.pos = pos * 50*SCALE + Vector2(25, 25)*SCALE
        self.vel = vel * SCALE
        self.dir = vel.angle_to(Vector2(0, -1))
        self.rect = self.image.get_rect(center=self.pos * 50*SCALE + Vector2(25, 25)*SCALE)
        self.mask = pg.mask.from_surface(self.image)

    def update(self, surface):
        tempimage = pg.transform.rotate(self.image, self.dir)
        self.pos += self.vel 
        self.rect.center = self.pos
        surface.blit(tempimage, self.rect)


        if not (0 < self.pos.x < 7*SCALE*50 and 0 < self.pos.y < 9*SCALE*50):
            return True
#----------------------------------------------
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
            Bulletlist.append(Bullet(self.pos, (PlayerPos - self.pos).normalize() * 2))

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
            except Exception as e:
                pass

    def collision(self):
        for i in Bulletlist:
            if i.type == "blue":
                if self.mask.overlap(i.mask, (int(i.pos.x- self.pos.x * 50*SCALE), int(i.pos.y - self.pos.y * 50*SCALE))):
                    Bulletlist.remove(i)
                    self.health -= 1
#----------------------------------------------