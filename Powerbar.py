import pygame, math
from pygame.locals import *

class PowerBarSprite(pygame.sprite.Sprite):
    bar = pygame.image.load('Art/PowerBar.png')
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.rect = pygame.Rect(self.bar.get_rect())
        self.rect.move_ip(position)
        self.image = self.bar
        self.Ys = []

class PowerSelectorSprite(pygame.sprite.Sprite):
    selector = pygame.image.load('Art/PowerSelector.png')
    updown = 0
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.rect = pygame.Rect(self.selector.get_rect())
        self.rect.move_ip(position)
        self.image = self.selector
    def update(self, power, Ys, Diff):
        self.Ys = Ys
        if self.updown == 0 and power == 1:
            self.rect.centery -= Diff
        if self.updown == 1 and power == 1:
            self.rect.centery += Diff
        if self.rect.centery >= self.Ys[0]:
            self.reset()
        if self.rect.centery <= self.Ys[1]:
            self.updown = 1
    def reset(self):
        self.rect.centery = self.Ys[0]
        self.updown = 0

class Select:
    def returnval(self, sprite1, sprite2):
        return (100 - (sprite2.rect.centery - sprite1.rect.top)) / 2
        
