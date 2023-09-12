import pygame as pg

# ---VARIABLES----------------------------------
SCALE = 1.7
Collidable_list = []
# ----------------------------------------------
# ---CLASSES------------------------------------
from .txt_button import TxtButton
from .bullet import Bulletlist, Bullet
from .enemy import Enemylist, Enemy
from .player import Player
from .wall import Wall
from .pit import Pit


# ----------------------------------------------
# ---FUNCTIONS----------------------------------
def displayBullets(screen):
    for i in Bulletlist:
        if i.update(screen):
            Bulletlist.remove(i)


# ----------------------------------------------
def update_enemies(screen):
    hit = False
    for i in Enemylist:
        if i.update(screen):
            hit = True
    return hit


# ----------------------------------------------
def update_collidables(screen):
    for i in Collidable_list:
        i.update(screen)


# ----------------------------------------------
