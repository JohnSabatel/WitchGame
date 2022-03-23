import pygame
pygame.init()


twalkLeft = [pygame.image.load('TWL1.png'), pygame.image.load('TWL2.png'), pygame.image.load('TWL3.png'),
             pygame.image.load('TWL4.png'), pygame.image.load('TWL5.png'), pygame.image.load('TWL6.png')]
twalkRight = [pygame.image.load('TWR1.png'), pygame.image.load('TWR2.png'), pygame.image.load('TWR3.png'),
              pygame.image.load('TWR4.png'), pygame.image.load('TWR5.png'), pygame.image.load('TWR6.png')]
tattackLeft = [pygame.image.load('TAL1.png'), pygame.image.load('TAL2.png'), pygame.image.load('TAL3.png'),
               pygame.image.load('TAL4.png'), pygame.image.load('TAL5.png')]
tattackRight = [pygame.image.load('TAR1.png'), pygame.image.load('TAR2.png'), pygame.image.load('TAR3.png'),
                pygame.image.load('TAR4.png'), pygame.image.load('TAR5.png')]
tdeathLeft = [pygame.image.load('TDL1.png'), pygame.image.load('TDL2.png'), pygame.image.load('TDL3.png'),
              pygame.image.load('TDL4.png'), pygame.image.load('TDL5.png')]
tdeathRight = [pygame.image.load('TDR1.png'), pygame.image.load('TDR2.png'), pygame.image.load('TDR3.png'),
               pygame.image.load('TDR4.png'), pygame.image.load('TDR5.png')]

class tree(object):
    def __init__(self, x, playerx):
        self.x = x
        self.y = 430
        self.ptrackX = playerx # Keeps track of what player x position so we can tell enemy where to walk.
        self.damage = 15
        self.health = 40
        self.vel = 2
        self.attacking = False
        self.left = False
        self.right = False
        self.dead = False
        self.deathDone = False # This tells the main program when to stop calling death animation. Delete object
        self.deathSound = True
        self.walkCount = 0
        self.attackCount = 0
        self.deathCount = 0
        self.hitbox = (x + 21, self.y, 50, 70) # (top left x, top left y, width, height)

    def drawWalk(self, win):
        self.moveAI()

        if self.walkCount >= 18:
            self.walkCount = 0

        if self.attackCount >= 25:
            self.attackCount = 0

        if not (self.attacking):
            if self.left:
                win.blit(twalkLeft[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(twalkRight[self.walkCount//3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(tattackLeft[self.attackCount//5], (self.x, self.y))
                self.attackCount += 1
            else:
                win.blit(tattackRight[self.attackCount//5], (self.x, self.y))
                self.attackCount += 1

        # Switch hitbox position to compensate for the image flip
        if self.left:
            self.hitbox = (self.x + 11, self.y, 50, 70)
        if self.right:
            self.hitbox = (self.x + 21, self.y, 50, 70)
        #pygame.draw.rect(win, (255,0,0), self.hitbox, 2) # To draw hitbox if you need to see

        # HEALTH BAR
        pygame.draw.rect(win, (255,0,0), (self.hitbox[0] - 5, self.hitbox[1] - 20,40, 10))
        pygame.draw.rect(win, (0,128,0), (self.hitbox[0] - 5, self.hitbox[1] - 20, self.health, 10))

    def drawDeath(self,win):

        if self.deathCount >= 29:
            self.dead = False
            self.deathDone = True

        if self.left:
            win.blit(tdeathLeft[self.deathCount//6], (self.x, self.y))
            self.deathCount += 1
        else:
            win.blit(tdeathRight[self.deathCount//6], (self.x, self.y))
            self.deathCount += 1


    def moveAI(self):
        if self.ptrackX < self.x - 41: # Walking left
            self.x -= self.vel
            self.left = True
            self.right = False
            self.attacking = False

        elif self.ptrackX > self.x + 71: # Walking right. It is 30 more to compensate for the visual of graphic flip
            self.x += self.vel
            self.right = True
            self.left = False
            self.attacking = False

        elif self.ptrackX <= self.x - 38: # Attacking left. The attacks are 3 less to compensate for vel space
            self.left = True
            self.right = False
            self.attacking = True

        elif self.ptrackX >= self.x + 68: # Attacking right
            self.right = True
            self.left = False
            self.attacking = True

        else:
            self.right = True


