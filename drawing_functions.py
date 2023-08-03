import pygame as pg
import drawing_functions as df
from pygame.math import Vector2

scale = 1.7

def draw_bg(surface):

    surface.fill("#baf9ff")
    pg.draw.rect(surface, "#a4eeff", (0, 0, 350 * scale*scale, 450 * scale), 5)
    for x, y in [(i, j) for i in range(7) for j in range(9) if (i + j) % 2]:
        pg.draw.rect(surface, "#a4eeff", (50 * scale * x, 50 * scale * y, 50*scale, 50*scale))




def draw_menu_bg(surface):
    surface.fill("#d8fcff")
    for x, y in [(i, j) for i in range(7) for j in range(10) if (i + j) % 2]:
        pg.draw.rect(surface, "#bef3ff", (50*scale * x, 50*scale * y, 50*scale, 50*scale))


def draw_txt(surface, txt, x, y, color, font, align="center"):
    label = font.render(txt, True, color)
    rect = (
        label.get_rect(center=(x, y))
        if align == "center"
        else label.get_rect(midleft=(x, y))
    )
    surface.blit(label, rect)


def fade_to(surface, color, duration):
    surf = pg.Surface((700*scale, 500*scale))
    surf.fill(color)
    for i in range(60):
        surf.set_alpha(int(17))
        surface.blit(surf, (0, 0))
        pg.display.flip()
        pg.time.delay(int(duration * 1000 / 60))


def draw_ui(surface, font: pg.font.Font, level, score, lives):
    score = "Score: " + str(score)
    level = "Level: " + str(level)
    pg.draw.rect(surface, '#baf9ff', (0, 450*scale, 350*scale, 50*scale))
    draw_txt(surface, str(level), 210*scale, 465*scale, (0, 0, 0), font, "")
    draw_txt(surface, str(score), 210*scale, 490*scale, (0, 0, 0), font, "")

    for i in range(lives):
        rect = pg.Rect(60*scale + 25*scale * i, 470*scale, 20*scale, 20*scale)
        pg.draw.rect(surface, (255, 0, 0), rect, 0, 5)
