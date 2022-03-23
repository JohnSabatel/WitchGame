import pygame
pygame.init()

globe = pygame.image.load('healthpotion.png')

class healthpot(object):

    def __init__(self,x):
        self.x = x
        self.y = 465
        self.heal = 20
        self.hitbox = (x + 2, 460, 35, 35)

    def draw(self,win):
        win.blit(globe, (self.x, self.y))
        #pygame.draw.rect(win,(255,0,0), self.hitbox, 2) # Display if you need to see hitbox
