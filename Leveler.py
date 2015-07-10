import pygame, Collision, ctypes
from pygame.locals import *
from Collision import *

class LevelUp:
    LvL = 0
    start = 2
    def __init__(self, level):
        self.LvL = level
        if self.LvL != -1:
            CreateWorld(self.LvL)
    def Level0(self, score):
        if self.start == 1:
            self.start = 0
            ctypes.windll.user32.MessageBoxA(0,"LEVEL 0, Score at least 10 points to move on.", "LvL UP!", 0)
        if self.start == 2:
            self.start = 1
        if score >= 10:
            self.LvLUp(self.LvL+1, Obstacles)
            ctypes.windll.user32.MessageBoxA(0,"LEVEL 1, Hit both targets to move on.", "LvL UP!", 0)
            return 1
        return 0
    def Level1(self, score):
        count = 0
        for x in Obstacles:
            if isinstance(x, Target):
                if x.HIT == True:
                    count += 1
        if count > 1:
            self.LvLUp(self.LvL+1, Obstacles)
            ctypes.windll.user32.MessageBoxA(0,"LEVEL 2, Score 10 points.", "LvL UP!", 0)
            return 1
        return 0
    def Level2(self, score):
        if score >= 10:
            self.LvLUp(self.LvL+1, Obstacles)
            ctypes.windll.user32.MessageBoxA(0,"LEVEL3, Hit the target to WIN.", "LvL UP!", 0)
            return 1
        return 0
    def Level3(self, score):
        count = 0
        for x in Obstacles:
            if isinstance(x, Target):
                if x.HIT == True:
                    count += 1
        if count > 0:
            ctypes.windll.user32.MessageBoxA(0,"YOU WIN!!!.", "WIN SCREEN!", 0)
            return -1
        return 0
    def LvLUp(self, lvl, Obs):
        self.LvL = lvl
        Obs.empty()
        CreateWorld(self.LvL)
    def update(self, score):
        if self.LvL == 0:
            return self.Level0(score)
        if self.LvL == 1:
            return self.Level1(score)
        if self.LvL == 2:
            return self.Level2(score)
        if self.LvL == 3:
            return self.Level3(score)
        return 0

    def setLvL(self, lvl, Obs):
        self.LvLUp(lvl, Obs)
        return 1
