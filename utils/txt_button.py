import pygame as pg


class TxtButton:
    def __init__(self, x, y, txt, color, font):
        self.txt = txt
        self.label = font.render(txt, True, color)
        self.rect = self.label.get_rect(center=(x, y))
        self.bgrect = self.rect.inflate(10, 10)
        self.clicked = False
        self.color = color
        self.font = font

    def update(self, surface, pos):
        action = False

        self.label = self.font.render(self.txt, True, self.color)
        self.bgrect = self.rect.inflate(10, 10)
        self.rect = self.label.get_rect(center=self.rect.center)

        mp = pg.mouse.get_pos()
        if self.rect.collidepoint(mp):
            pg.draw.rect(surface, "#dddddd", self.bgrect)
        if self.rect.collidepoint(pos):
            action = True
        surface.blit(self.label, self.rect)
        return action
