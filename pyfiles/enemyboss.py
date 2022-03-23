import pygame
pygame.init()

bIdle = pygame.image.load('BIdle.png')
bBolt = [pygame.image.load('BA1.png'), pygame.image.load('BA2.png'), pygame.image.load('BA3.png'),
         pygame.image.load('BA4.png'), pygame.image.load('BA5.3.png'), pygame.image.load('BA6.2.png'),
         pygame.image.load('BAR5.3.png'), pygame.image.load('BAR4.png'),pygame.image.load('BAR3.png'),
         pygame.image.load('BAR2.png'), pygame.image.load('BAR1.png')]
bSwipe = [pygame.image.load('BA1.png'), pygame.image.load('BA2.png'), pygame.image.load('BA3.png'),
          pygame.image.load('BA4.png'), pygame.image.load('BAS1.png'), pygame.image.load('BAS2.png'),
          pygame.image.load('BAS3.png'), pygame.image.load('BAR4.png'), pygame.image.load('BAR3.png'),
          pygame.image.load('BAR2.png'), pygame.image.load('BAR1.png')]
bSummon = [pygame.image.load('BA1.png'), pygame.image.load('BA2.png'), pygame.image.load('BA3.png'),
           pygame.image.load('BA4.png'), pygame.image.load('BA5.2.png'), pygame.image.load('BA6.3.png'),
           pygame.image.load('BAR5.2.png'),  pygame.image.load('BAR4.png'), pygame.image.load('BAR3.png'),
           pygame.image.load('BAR2.png'), pygame.image.load('BAR1.png')]
bDeath = [pygame.image.load('death1.png'), pygame.image.load('death2.png'), pygame.image.load('death3.png'),
          pygame.image.load('death4.png'), pygame.image.load('death5.png')]



class boss (object):

    def __init__(self):
        self.x = 670
        self.y = 225
        self.health = 200
        self.swipeDamage = 35
        self.bolt = False
        self.swipe = False
        self.summon = False
        self.dead = False
        self.introSound = True
        self.deathSound = True
        self.boltCount = 0
        self.summonCount = 0
        self.swipeCount = 0
        self.deathCount = 0
        self.deathTimer = 0
        self.hitbox = (self.x + 50, self.y + 70, 110, 210) # (top left x, top left y, width, height)

    def draw(self,win):

        # If animation is concluded, stop playing and return false value to main game
        if self.boltCount >= 65:
            self.bolt = False
            self.boltCount = 0

        if self.swipeCount >= 32:
            self.swipe = False
            self.swipeCount = 0

        if self.summonCount >= 65:
            self.summon = False
            self.summonCount = 0

        # Boss animation drawings
        if self.bolt:
            win.blit(bBolt[self.boltCount//6], (self.x, self.y))
            self.boltCount += 1
        elif self.swipe:
            win.blit(bSwipe[self.swipeCount//3], (self.x, self.y))
            self.swipeCount += 1
        elif self.summon:
            win.blit(bSummon[self.summonCount//6], (self.x, self.y))
            self.summonCount += 1
        else:
            win.blit(bIdle, (self.x, self.y))

        # Health Bar
        pygame.draw.rect(win, (255,0,0), (675, 220, 200, 10))
        pygame.draw.rect(win, (0, 128, 0), (675, 220, self.health, 10))

        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2) # To draw hitbox if you need to see

    def drawDeath(self,win):

        if self.deathCount + 1 >= 25:
            self.deathCount = 0
            self.deathTimer += 1

        win.blit(bIdle, (self.x, self.y))
        win.blit(bDeath[self.deathCount // 5], (self.x + 60, self.y + 70))
        win.blit(bDeath[self.deathCount//5], (self.x + 60, self.y + 100))
        win.blit(bDeath[self.deathCount//5], (self.x + 60, self.y + 130))
        win.blit(bDeath[self.deathCount // 5], (self.x + 40, self.y + 70))
        win.blit(bDeath[self.deathCount // 5], (self.x + 40, self.y + 100))
        win.blit(bDeath[self.deathCount // 5], (self.x + 40, self.y + 130))
        win.blit(bDeath[self.deathCount // 5], (self.x + 80, self.y + 70))
        win.blit(bDeath[self.deathCount // 5], (self.x + 80, self.y + 100))
        win.blit(bDeath[self.deathCount // 5], (self.x + 80, self.y + 130))
        self.deathCount += 1


