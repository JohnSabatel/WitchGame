import pygame
pygame.init()

bFire = [pygame.image.load('death1.png'), pygame.image.load('death2.png'), pygame.image.load('death3.png'),
         pygame.image.load('death4.png'), pygame.image.load('death5.png')]

class aoe(object):
    def __init__(self, x):
        self.x = x
        self.y = 420
        self.damage = 1
        self.burnCount = 0
        self.burnTimer = 0
        self.hitbox = (x - 10, 430, 85, 60)

    def draw(self,win):

        if self.burnCount + 1 >= 25:
            self.burnCount = 0
            self.burnTimer += 1

        win.blit(bFire[self.burnCount//5], (self.x, self.y))
        win.blit(bFire[self.burnCount//5], (self.x + 15, self.y))
        win.blit(bFire[self.burnCount // 5], (self.x + 25, self.y))
        win.blit(bFire[self.burnCount // 5], (self.x - 15, self.y))
        win.blit(bFire[self.burnCount // 5], (self.x - 25, self.y))
        self.burnCount += 1

        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # To draw hitbox if you need to see