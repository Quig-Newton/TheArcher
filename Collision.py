import pygame, math
from pygame.locals import *
from math import *

class Ground(pygame.sprite.Sprite): #Ground piece
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Art/Ground.png")
        self.position = position
        self.rect = pygame.Rect(0, 0, 127, 127)
        self.rect.move_ip(self.position)
        
class Wall(pygame.sprite.Sprite): #Wall piece
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Art/Wall.png")
        self.position = position
        self.rect = pygame.Rect(0, 0, 127, 127)
        self.rect.move_ip(self.position)
        
class Target(pygame.sprite.Sprite): #A Target
    HIT = False
    def __init__(self, position, num):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load("Art/BasicTarget.png")
        self.image = self.src_image
        self.position = position
        self.Tnum = num
        self.angle = 0
        self.up = self.down = self.right = self.left = 0
        self.rect = self.image.get_rect()
        self.rect.move_ip(self.position)
        self.targ = []
        x = self.rect.left
        y = self.rect.top+2
        for num in range(0, 9):
            if num == 0 or num == 8:
                self.targ.append(pygame.Rect(x,y,22,16))
                y += 16
            else:
                self.targ.append(pygame.Rect(x,y,22,13))
                y += 13
    def score(self, rect):
        for x in self.targ:
            if rect.colliderect(x):
                self.HIT = True
                return abs(x.y - self.rect.centery)
        return 0
    def TarNum(self):
        return self.Tnum

class MovingTarget(Target):#A moving target
    def __init__(self, position, num, movType):
        super(MovingTarget, self).__init__(position, num)
        self.movType = movType
        self.dir = 1
    def update(self):
        super(Target.update(self))
        print self.dir
        if self.movType == 0:
            if self.rect.y <= 127:
                self.dir = 1
            if self.rect.bottom >= 762:
                self.dir = -1
            self.rect.y += self.dir
Levels = []
#grid of Strings, 12X7 127X127 Blocks
# W = Wall | T = Target | G = Ground
Terrain1 = ["WWWWWWWWWWWW",
               "W          W",
               "W          W",
               "W          W",
               "W          T",
               "W          W",
               "WGGGGGGGGGGW"]
Levels.append(Terrain1)
Terrain2 = ["WWWWWWWWWWWW",
               "W          T",
               "W          W",
               "W          W",
               "W          T",
               "W          W",
               "WGGGGGGGGGGW"]
Levels.append(Terrain2)
Terrain3 = ["WWWWWWWWWWWW",
               "W          W",
               "W          W",
               "W          W",
               "W       W  T",
               "W          W",
               "WGGGGGGGGGGW"]#make sure to change back
Levels.append(Terrain3)
Terrain4 = ["WWWWWWWWWWWW",
               "W     W    W",
               "W          W",
               "W     W    W",
               "W     W    W",
               "W     W    T",
               "WGGGGGGGGGGW"]
Levels.append(Terrain4)
Terrain5 = ["WWWWWWWWWWWW",
               "WWWWWWWWWWWW",
               "W     WWWWWW",
               "W          T",
               "W   WWWWWWWW",
               "W  WWWWWWWWW",
               "WGGGGGGGGGGW"]
Levels.append(Terrain5)
Terrain6 = ["WWWWWWWWWWWW",
               "WW         W",
               "W  WW      T",
               "W          W",
               "W    WWWW  W",
               "W    W  W  T",
               "WGGGGGGGGGGW"]
Levels.append(Terrain6)

Obstacles = pygame.sprite.Group()
MovingB = pygame.sprite.Group()
g = pygame.Rect(127,768, 127, 127)
MT = None

def CreateWorld(LvL):
    x = y = Target_num =  0
    for row in Levels[LvL]:
        for col in row:
            if col == "W":
                Obstacles.add( Wall( (x,y) ) )
            if col == "G":
                Obstacles.add( Ground( (x,y) ) )
            if col == "T":
                Obstacles.add( Target( (x,y), Target_num ) )
                Target_num += 1
            if col == "V":#This is a vertical moving target
                MT = MovingTarget( (x,y), Target_num, 0)
                Obstacles.add(MT)
                Target_num += 1
            x += 127
        y += 127
        x = 0

def obCollision(rect):
    for sprite in Obstacles:
        if Collision(rect, sprite.rect):
            if isinstance(sprite, Target):
                return sprite.score(rect), sprite.rect
            return 0, sprite.rect
    return -1, None

def Collision(rect1, rect2):
    #for instance:
    #rect 1 = arrow; rect 2 = obstacle
    if rect2.x+rect2.width >= rect1.x >= rect2.x and rect2.y+rect2.height >= rect1.y >= rect2.y:
        return True
    return False
    
