import pygame
pygame.init()

scLeft = [pygame.image.load('SPL1.png'), pygame.image.load('SPL2.png'), pygame.image.load('SPL3.png'),
          pygame.image.load('SPL4.png')]
scRight = [pygame.image.load('SPR1.png'), pygame.image.load('SPR2.png'), pygame.image.load('SPR3.png'),
           pygame.image.load('SPR4.png')]


class cast(object):

    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.distance = 0
        self.damage = 0.2
        self.facing = facing
        self.vel = 5 * facing
        self.castCount = 0
        self.hitbox = (self.x + 17, self.y + 15, 115, 20 )


    def draw(self, win):

        if self.castCount >= 8:
            self.castCount = 0

        if self.facing == -1:
            win.blit(scLeft[self.castCount//2], (self.x - 105, self.y))
            self.castCount += 1
        else:
            win.blit(scRight[self.castCount//2], (self.x, self.y))
            self.castCount += 1

        self.hitbox = (self.x + 17, self.y + 15, 115, 20)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # To draw hitbox if you need to see
