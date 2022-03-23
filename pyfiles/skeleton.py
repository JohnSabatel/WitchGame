import pygame
pygame.init()

class skelly(object):

    swalkLeft = [pygame.image.load('SKWL1.png'), pygame.image.load('SKWL2.png'), pygame.image.load('SKWL3.png'),
                 pygame.image.load('SKWL4.png'),pygame.image.load('SKWL5.png'), pygame.image.load('SKWL6.png'),
                 pygame.image.load('SKWL7.png'), pygame.image.load('SKWL8.png')]
    swalkRight = [pygame.image.load('SKWR1.png'), pygame.image.load('SKWR2.png'), pygame.image.load('SKWR3.png'),
                  pygame.image.load('SKWR4.png'), pygame.image.load('SKWR5.png'), pygame.image.load('SKWR6.png'),
                  pygame.image.load('SKWR7.png'), pygame.image.load('SKWR8.png')]
    sraiseLeft = [pygame.image.load('SKSL1.png'), pygame.image.load('SKSL2.png'), pygame.image.load('SKSL3.png'),
                  pygame.image.load('SKSL4.png'), pygame.image.load('SKSL5.png')]
    sraiseRight = [pygame.image.load('SKSR1.png'), pygame.image.load('SKSR2.png'),pygame.image.load('SKSR3.png'),
                   pygame.image.load('SKSR4.png'), pygame.image.load('SKSR5.png')]

    sDeath = [pygame.image.load('death1.png'), pygame.image.load('death2.png'), pygame.image.load('death3.png'),
             pygame.image.load('death4.png'), pygame.image.load('death5.png')]


    def __init__(self,x,start,stop,vel,face):
        self.x = x
        self.y = 420
        self.start = start
        self.stop = stop
        self.width = 64
        self.height = 64
        self.vel = vel * face
        self.health = 20
        self.damage = 1
        self.left = False
        self.right = False
        self.rise = True
        self.dead = False
        self.deathDone = False # This tells the main program when to stop calling death animation. Delete object
        self.deathSound = True
        self.walkCount = 0
        self.riseCount = 0
        self.deathCount = 0
        self.hitbox = (x + 21, 428, 35, 70) # (top left x, top left y, width, height)


    def drawWalk(self, win):
        self.moveAI()

        if self.walkCount >= 24:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.swalkRight[self.walkCount//6], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.swalkLeft[self.walkCount//6], (self.x, self.y))
            self.walkCount += 1

        self.hitbox = (self.x + 21, 428, 35, 70)  # Update position of the hitbox
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # To draw hitbox if you need to see

        # Health Bar
        pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0] - 5, self.hitbox[1] - 20, 40, 10))
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0] - 5, self.hitbox[1] - 20, 40 - (2 * (20 - self.health)), 10))

    def drawRise(self, win):

        if self.riseCount >= 24:
            self.rise = False

        if self.vel > 0:
            win.blit(self.sraiseRight[self.riseCount//5], (self.x, self.y))
            self.riseCount += 1

        else:
            win.blit(self.sraiseLeft[self.riseCount//5], (self.x, self.y))
            self.riseCount += 1

    def drawDeath(self,win):
        if self.deathCount >= 24:
            self.dead = False
            self.deathDone = True

        win.blit(self.sDeath[self.deathCount//5], (self.x, self.y))
        self.deathCount += 1



    def moveAI(self):

        if self.vel > 0: # If self.vel is a positive number
            if self.x < self.stop + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.start - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0









