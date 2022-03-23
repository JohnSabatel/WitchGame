import pygame

pygame.init()

cLeft = [pygame.image.load('CL1.png'), pygame.image.load('CL2.png'), pygame.image.load('CL3.png'),
         pygame.image.load('CL4.png')]
cRight = [pygame.image.load('CR1.png'), pygame.image.load('CR2.png'), pygame.image.load('CR3.png'),
          pygame.image.load('CR4.png')]

class cast(object):

    def __init__(self, x, facing):
        self.x = x
        self.y = 455
        self.damage = 4
        self.facing = facing
        self.vel = 9 * facing # Speed and direction of curse
        self.castCount = 0
        self.distance = 0

    def draw(self, win):\

        if self.castCount + 1 >= 8:
            self.castCount = 0


        # If facing left
        if self.facing == -1:
            win.blit(cLeft[self.castCount//2], (self.x - 70, self.y))
            self.castCount += 1
            self.distance += 8
        # If facing right
        else:
            win.blit(cRight[self.castCount//2], (self.x, self.y))
            self.castCount += 1
            self.distance += 8



