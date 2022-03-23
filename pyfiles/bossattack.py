import pygame
pygame.init()

bLeft = [pygame.image.load('BB1.png'), pygame.image.load('BB2.png'), pygame.image.load('BB3.png'),
         pygame.image.load('BB4.png'), pygame.image.load('BB5.png')]

class bloodbolt(object):

    def __init__(self):
        self.x = 680
        self.y = 455
        self.damage = 15
        self.vel = 8
        self.castCount = 0
        self.distance = 0

    def draw(self,win):

        if self.castCount + 1 >= 10:
            self.castCount = 0

        win.blit(bLeft[self.castCount//2], (self.x, self.y))
        self.castCount += 1
        self.distance += self.vel
