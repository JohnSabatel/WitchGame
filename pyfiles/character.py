"""

"""


import pygame
import time
pygame.init()

# Image loading for player animation
pstandLeft = [pygame.image.load('SL1.png'), pygame.image.load('SL2.png'), pygame.image.load('SL3.png'),
              pygame.image.load('SL4.png')]
pstandRight = [pygame.image.load('SR1.png'), pygame.image.load('SR2.png'), pygame.image.load('SR3.png'),
               pygame.image.load('SR4.png')]
pwalkLeft = [pygame.image.load('WL1.png'), pygame.image.load('WL2.png'), pygame.image.load('WL3.png'),
             pygame.image.load('WL4.png'), pygame.image.load('WL5.png'), pygame.image.load('WL6.png'),
             pygame.image.load('WL7.png'), pygame.image.load('WL8.png')]
pwalkRight = [pygame.image.load('WR1.png'), pygame.image.load('WR2.png'), pygame.image.load('WR3.png'),
              pygame.image.load('WR4.png'), pygame.image.load('WR5.png'), pygame.image.load('WR6.png'),
              pygame.image.load('WR7.png'), pygame.image.load('WR8.png')]
pattackLeft = [pygame.image.load('AL1.png'), pygame.image.load('AL2.png'), pygame.image.load('AL3.png'),
               pygame.image.load('AL4.png'), pygame.image.load('AL5.png'), pygame.image.load('AL6.png'),
               pygame.image.load('AL7.png'), pygame.image.load('AL8.png')]
pattackRight = [pygame.image.load('AR1.png'), pygame.image.load('AR2.png'),pygame.image.load('AR3.png'),
                pygame.image.load('AR4.png'), pygame.image.load('AR5.png'), pygame.image.load('AR6.png'),
                pygame.image.load('AR7.png'), pygame.image.load('AR8.png')]
pdeathLeft = [pygame.image.load('DL1.png'), pygame.image.load('DL2.png'), pygame.image.load('DL3.png'),
              pygame.image.load('DL4.png'), pygame.image.load('DL5.png'), pygame.image.load('DL6.png'),
              pygame.image.load('DL7.png'), pygame.image.load('DL8.png'), pygame.image.load('DL9.png'),
              pygame.image.load('DL10.png')]
pdeathRight = [pygame.image.load('DR1.png'), pygame.image.load('DR2.png'), pygame.image.load('DR3.png'),
               pygame.image.load('DR4.png'), pygame.image.load('DR5.png'), pygame.image.load('DR6.png'),
               pygame.image.load('DR7.png'), pygame.image.load('DR8.png'), pygame.image.load('DR9.png'),
               pygame.image.load('DR10.png')]


class player(object):

    def __init__(self):
        self.x = 30
        self.y = 445
        self.width = 64
        self.height = 64
        self.vel = 6 # Player running speed
        self.left = False
        self.right = False
        self.stand = True
        self.attack = False
        self.walk = False
        self.dead = False
        self.deathDone = False
        self.deathSound = True
        self.walkCount = 0
        self.standCount = 0
        self.attackCount = 0
        self.deathCount = 0
        self.health = 100
        self.hitbox = (self.x + 8, self.y + 11, 35, 52) # (top left x, top left y, width height)

    def draw(self, win):

        if self.walkCount + 1 >= 24:
            self.walkCount = 0

        if self.standCount + 1 >= 8:
            self.standCount = 0

        if self.attackCount + 1 >= 24:
            self.attackCount = 0

        # Walking frames
        if self.walk:
            if self.left:
                win.blit(pwalkLeft[self.walkCount//4], (self.x,self.y)) # Each frame plays 4 times
                self.walkCount += 1
            elif self.right:
                win.blit(pwalkRight[self.walkCount // 4], (self.x, self.y))
                self.walkCount += 1

        elif self.attack:
            if self.left:
                win.blit(pattackLeft[self.attackCount//4], (self.x, self.y))
                self.attackCount += 1
            elif self.right:
                win.blit(pattackRight[self.attackCount//4], (self.x, self.y))
                self.attackCount += 1
        else:
            if self.left:
                win.blit(pstandLeft[self.standCount//2], (self.x, self.y))
                self.standCount += 1
            else:
                win.blit(pstandRight[self.standCount//2], (self.x, self.y))
                self.standCount += 1

        # Hit box position update
        self.hitbox = (self.x + 8, self.y, 35, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # To draw hitbox if you need to see

    def drawDeath(self,win):

        if self.deathCount + 1 >= 30:
            self.dead = False
            self.deathDone = True

        if self.left:
            win.blit(pdeathLeft[self.deathCount//3], (self.x, self.y + (self.deathCount - 5)))
            self.deathCount += 1
        else:
            win.blit(pdeathRight[self.deathCount//3], (self.x, self.y + (self.deathCount - 5)))
            self.deathCount += 1








