import pygame, math, Collision
from pygame.locals import *
from Collision import *

pygame.mixer.init(22050, 8, 2, 2024)#16, 4096

class ArrowSprite(pygame.sprite.Sprite):

    TOP_FORCE = 10
    GRAVITY = .5
    
    def __init__(self,image):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.image = self.src_image
        self.position = (0,0)
        self.speed = (0,0)
        self.rect = self.image.get_rect()
        self.rect.move_ip(-100, -100)
        self.moving = 0
        self.xSpeed = self.ySpeed = 0
        self.shot = False
        self.angle = 0
        self.colBox = pygame.Rect(-100, -100, 10, 10)
        self.theta = 0
        self.shootSound = pygame.mixer.Sound("Sound/shoot")
        self.hitSound = pygame.mixer.Sound("Sound/hit")

    def update(self):
        #use center of arrow rect for all coords; doesn't change
        if self.moving > 0:
            if self.shot == False:
                rad = self.angle * math.pi / 180
                self.shot = True
                self.xSpeed = self.moving*math.cos(rad)
                self.ySpeed = self.moving*math.sin(rad)
            self.ySpeed -= self.GRAVITY
            self.speed = (self.xSpeed, self.ySpeed)
            self.theta = float(self.ySpeed) / float(self.xSpeed)
            self.turn(math.atan(self.theta)*180/math.pi)
            x, y = self.position
            x += self.speed[0]/1.8
            y += -self.speed[1]/1.8
            self.position = (x, y)
            self.rect.center = self.position
            self.colBox.center = tupAdd(self.rect.center, (self.xSpeed/2, -self.ySpeed/2))

    #This is for when the arrow hits something.
    def hit(self):
        self.shot = False
        self.moving = 0

    def turn(self, amount):
        "turn some amount"
        oldCenter = self.rect.center
        self.dir = amount
        self.image = pygame.transform.rotate(self.src_image, self.dir)
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

def tupAdd(tup1, tup2):
    xTmp = tup1[0] + tup2[0]
    yTmp = tup1[1] + tup2[1]
    return (xTmp, yTmp)

class Shoot:
    #needs initial angle, position and force.
    def anArrow(self, angle, position, force):
        self.arrow = ArrowSprite("Art/Arrow.png")
        self.arrow.position = position
        self.arrow.image = pygame.transform.rotate(self.arrow.src_image, angle)
        self.arrow.moving = force
        self.arrow.angle = angle
        self.arrow.shootSound.play()
        self.quiver = pygame.sprite.GroupSingle(self.arrow)
        if force <= 0:
            return 0
        return 2
    def fired(self, screen):
        score, ob_rect = obCollision(self.arrow.colBox)
        if score >= 0:
            channel = self.arrow.hitSound.play()
            self.arrow.hit()
            return 0, self.arrow, score
        self.quiver.update()
        self.quiver.draw(screen)
        return 2, None, -1
