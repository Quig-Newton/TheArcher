import pygame, math, sys, thread, Powerbar, Menu, Arrow, Collision, Leveler
from pygame.locals import *
from Powerbar import *
from Menu import *
from Arrow import Shoot
from Collision import *
from sys import exit
from Leveler import *
screen = pygame.display.set_mode((1524,768))
clock = pygame.time.Clock()

pygame.init()

#initilization of Arrow variables
shoot = Shoot()

arwCount = 0

bowImg = pygame.image.load('Art/Bow1.png')

class BowSprite(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = bowImg
        self.position = position
        self.rect = pygame.Rect(self.image.get_rect())
        self.rect.center = position
        self.dir = 0
        self.armx = 50
        self.army = 70
    def update(self, angle, Archer, sceen):
        rad = angle * math.pi / 180
        self.turn(angle)
        self.rect.centerx = Archer.rect.centerx + 60*math.cos(rad)
        self.rect.centery = Archer.rect.centery + 80*math.sin(-rad)
        pygame.draw.line(screen, (0,0,0), ( (Archer.rect.left+23), (Archer.rect.top + 39)),
                         (Archer.rect.centerx + 50*math.cos(rad), Archer.rect.centery + 70*math.sin(-rad)), 2)
        pygame.draw.line(screen, (0,0,0), ( (Archer.rect.left+23), (Archer.rect.top + 41)),
                         (Archer.rect.centerx + 65*math.cos(rad), Archer.rect.centery + 85*math.sin(-rad)), 2)
        #pygame.draw.circle(screen, (250, 0, 25), self.rect.center, 2)
    def turn(self, amount):
        "turn some amount"
        oldCenter = self.rect.center
        self.dir = amount
        self.image = pygame.transform.rotate(bowImg, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

class LegsSprite(pygame.sprite.Sprite):
    legs = pygame.image.load('Art/Legs.png')
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.rect = pygame.Rect(self.legs.get_rect())
        self.rect.move_ip(position)
        self.image = self.legs
         
class ArcherSprite(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.position = position
        self.legs = LegsSprite((position[0], position[1]+100))
        self.angle = 0
        self.k_up =  self.k_down = 0
        self.rect = self.image.get_rect()
        self.rect.move_ip(position)
        self.Lrect = self.legs.rect
        self.font = pygame.font.Font(None, 24)

    def update(self):
        self.angle += (self.k_up + self.k_down)
        if self.angle > 90:
            self.angle = 90
        if self.angle < 0:
            self.angle = 0
        #Code for displaying Angle of bow
        #ang = str(self.angle)
        #text = self.font.render(ang, 1, (10, 10, 10))
        #textpos = text.get_rect()
        #textpos.centerx = self.rect.x
        #rad = self.angle * math.pi / 180
        #textpos.centerx = self.rect.centerx + 100*math.cos(rad)
        #textpos.centery = self.rect.centery + 100*math.sin(-rad)
        #screen.blit(text, textpos)
        return self.angle
    def reset(self):
        self.angle = 0
        bow.update(self.angle, self, screen)

class TheScore():
    SCORE = 0
    font = pygame.font.Font(None, 120)
    def NewTotal(self, score):
        self.SCORE += self.getScore(score)
    def getScore(self, num):
        if num == 6 or num == 7:
            return 9
        if num == 19 or num == 20:
            return 7
        if num == 32 or num == 33:
            return 5
        if num == 45 or num == 46:
            return 3
        if num == 61 or num == 62:
            return 1
        return 0
    def update(self):
        scr = str(self.SCORE)
        scr += " | " + str(arwCount)
        text = self.font.render(scr, 1, (20, 50, 20), (250, 250, 50))
        textpos = text.get_rect()
        textpos = (0, 0)
        screen.blit(text, textpos)
    def reset(self):
        self.SCORE = 0

Scorer = TheScore()

arrow_group = pygame.sprite.Group()

#Game variabls
running = True
power = 0
#initilization of Menu
menuOn = 2
IGM = InGameMenu()

rect = screen.get_rect()
archer = ArcherSprite('Art/Body.png', (g.left,g.top-200))
archer_group = pygame.sprite.OrderedUpdates(archer)
archer_group.add(archer.legs)
pb = PowerBarSprite( ( (archer.rect)[0] - 120, (archer.rect)[1] ) )
ps = PowerSelectorSprite( (pb.rect.x, pb.rect.bottom) )
bow = BowSprite((0,0))
archer_group.add(pb)
archer_group.add(ps)
archer_group.add(bow)


Selector = IGM.openMenu(screen, "Start", "Sandbox")
if Selector < 0:
    pygame.quit()
    sys.exit()

#initilization of Leveler system
level = LevelUp(0)
reset = 0
    
screen.fill( (0,0,0) )
Difficulty = IGM.openMenu(screen, "Easy", "Hard")
if Difficulty < 0:
    pygame.quit()
    sys.exit()

while running:
    if menuOn > 0:
        if menuOn == 2:
            helpImg = pygame.image.load("Art/Help Screen.png")
            screen.blit(helpImg, (0,0))
        menuOn = IGM.openMenu(screen, "Continue", "Help")
        if menuOn == 1:
            helpImg = pygame.image.load("Art/Help Screen.png")
            screen.blit(helpImg, (0,0))
    else:
        #User Input
        deltat = clock.tick(30)
        for event in pygame.event.get():
            if not hasattr(event, 'key'): continue
            type = event.type
            if type == KEYDOWN and power == 0:
                if event.key == K_UP: archer.k_up = 1 * (Difficulty+4)
                elif event.key == K_DOWN: archer.k_down = 1 * -(Difficulty+4)
                elif event.key == K_SPACE:
                    if power == 0:
                        power = 1
                elif event.key == K_ESCAPE: menuOn = 1
                if Selector == 1:
                    if event.key == K_1: reset = level.setLvL(0, Obstacles)
                    elif event.key == K_2: reset =  level.setLvL(1, Obstacles)
                    elif event.key == K_3: reset = level.setLvL(2, Obstacles)
                    elif event.key == K_4: reset = level.setLvL(3, Obstacles)
                    elif event.key == K_5: reset = level.setLvL(4, Obstacles)
                    elif event.key == K_6: reset = level.setLvL(5, Obstacles)
            elif type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    archer.k_up = 0
                    archer.k_down = 0
                else:
                    if power == 1:
                        s = Select()
                        power = shoot.anArrow(ang, bow.rect.center, s.returnval(pb, ps))
                        ps.reset()
                        arwCount += 1
                        archer.reset()
                    
        #Rendering
        screen.fill( (0,255,255) )
        if Selector == 0:
            reset = level.update(Scorer.SCORE)
        if reset == 1:
            arrow_group.empty()
            MovingB.empty()
            Scorer.reset()
            arwCount = 0
            reset = 0
        if reset == -1:
            pygame.quit()
            sys.exit()
        ang = archer.update()
        bow.update(ang, archer, screen)
        ps.update(power, (pb.rect.bottom, pb.rect.y), Difficulty+3)
        if power == 2:
            power, arw, score = shoot.fired(screen)
            if arw != None:
                Scorer.NewTotal(score)
                arrow_group.add(arw)
        if len(arrow_group) > 0:
            arrow_group.draw(screen)
        if MT != None:
            MT.update()
        Obstacles.draw(screen)
        archer_group.draw(screen)
        Scorer.update()
        pygame.display.flip()

pygame.quit()
sys.exit()
