
import pygame
import time
import random
import character
import playerattack
import playerspecial
import skeleton
import healthpotion
import enemytree
import enemyboss
import bossattack
import bossaoe
pygame.init()

#Setting size of the window
win = pygame.display.set_mode((900,525))
pygame.display.set_caption("Witch Game")

# Clock speed
clock = pygame.time.Clock()

#Background Images
bg1 = pygame.image.load('level1.png')
bg2 = pygame.image.load('level2.png')
bg3 = pygame.image.load('level3.png')

# Other Images
witchImg = pygame.image.load('profile.png')
gameover = pygame.image.load('gameover.png')
levelcomp = pygame.image.load('lvlcomp.png')
UI = pygame.image.load('witchUI.png') # Witch UI frame
treeleftStart = pygame.image.load('TSL.png')
treerightStart = pygame.image.load('TSR.png')

# SOUNDS
cursesnd = pygame.mixer.Sound('cursesound.wav')
specialsnd = pygame.mixer.Sound('specialsound.wav')
witchhitsnd = pygame.mixer.Sound('witchhitsound.wav')
witchdeathsnd = pygame.mixer.Sound('witchdeathsound.wav')
skellyraisesnd = pygame.mixer.Sound('skellyraisesound.wav')
skellydeathsnd = pygame.mixer.Sound('skeletondeath.wav')
treedeathsnd = pygame.mixer.Sound('treedeathsound.wav')
bossintrosnd = pygame.mixer.Sound('bossintrosound.wav')
bossdeathsnd = pygame.mixer.Sound('bossdeath.wav')
bloodboltsnd = pygame.mixer.Sound('bloodboltsound.wav')
bossstaffchrgsnd = pygame.mixer.Sound('bossattchrgsound.wav')
bossaoesnd = pygame.mixer.Sound('aoesound.wav')
bossswipesnd = pygame.mixer.Sound('bossswipesound.wav')

# Global variables
bgSet = 1
cooldown = False
cooldownStart = 100
totalHeal = 0 # Full amount healed over
overHeal = 0 # Number that is over 100
actualHeal = 0 # Final product of solution for heals player gets
treeStart1 = True
treeStart2 = True
treeStart3 = True

# Music Start Play
gameMusic = pygame.mixer.music.load('mmSound.mp3')
pygame.mixer.music.play(-1)

""" /////////////////////////////////////////////////////////////////////////////  """
"""                           GRAPHIC BUILD SECTION                                """

def redrawGameWindow():
    # Change background depending on level character is on
    if bgSet == 1:
        win.blit(bg1, (0,0))
    elif bgSet == 2:
        win.blit(bg2, (0,0))
    else:
        win.blit(bg3,(0,0))

    # Draw skeletons
    for skelly in skellys:
        if skelly.rise:
            skelly.drawRise(win)
        elif skelly.dead:
            skelly.drawDeath(win)
            if skelly.deathSound:
                skellydeathsnd.play()
                skelly.deathSound = False
        else:
            skelly.drawWalk(win)

    # Draw trees
    for tree in trees:
        if tree.dead:
            tree.drawDeath(win) # Draw death animation if dead
            if tree.deathSound: # If dead, play sound
                treedeathsnd.play()
                tree.deathSound = False
        else:
            tree.drawWalk(win)

    # Evil Tree Static Drawing
    if bgSet == 2:
        if treeStart1:
            win.blit(treeleftStart, (300,430))
        if treeStart2:
            win.blit(treerightStart, (550,430))
        if treeStart3:
            win.blit(treerightStart, (700,430))

    # Draw Boss
    if bgSet == 3:
        if demonWitch.dead: # If dead, draw death animation
            pygame.mixer.music.stop()
            demonWitch.drawDeath(win)
            if demonWitch.deathSound: # Play death sound
                bossdeathsnd.play()
                demonWitch.deathSound = False
        else:
            demonWitch.draw(win)

    # Draw Potions
    for potion in potions:
        potion.draw(win)

    # Player UI
    win.blit(UI, (20, 50)) # Player UI graphic
    pygame.draw.rect(win, (255,0,0), (101, 69, 100, 8)) # Red under rect
    pygame.draw.rect(win, (0,128,0), (101, 69, 100 - (100 - witch.health), 8)) # Green rect
    win.blit(witchImg, (40, 77)) # Witch profile image
    pygame.draw.rect(win, (255, 127, 0), (101, 89, cooldownStart + (cooldownTime // 2), 8)) # Player cooldown update

    # Check if witch is dead
    if not witch.dead:
        witch.draw(win)  # Draw walking if not dead
    else:
        witch.drawDeath(win)  # Draw death animation if dead
        if witch.deathSound: # Play death sound once
            witchdeathsnd.play()
            witch.deathSound = False

    # Display GAME OVER if witch is dead
    if witch.deathDone:
        win.blit(gameover, (245, 115))

    # Display LEVEL COMPLETE if witch beats the boss
    if demonWitch.deathTimer >= 5:
        win.blit(levelcomp, (210, 115))

    # Update position of player attacks
    for curse in curses:
        curse.draw(win)
    for special in specials:
        special.draw(win)

    # Update position of boss attacks
    for bolt in bbAttacks:
        bolt.draw(win)
    for aoe in aoes:
        aoe.draw(win)

    pygame.display.update()

    """ --------------------------------------------------------------------  """


""" ////////////////////////////////////////////////////////////////////////////   """
"""                            MAIN GAME LOOP SECTION                              """

run = True
witch = character.player() # Create player object
demonWitch = enemyboss.boss() # Create boss object

""" /////////////////// """
"""      ARRAYS         """
# Arrays for boss and player attacks
curses = [] # Player
specials = [] # Player
bbAttacks = [] # Boss
aoes = [] # Boss

#Enemies
skellys = [] # Skeleton array
trees = [] # Evil tree array
skellys.append(skeleton.skelly(700,600,840,2,-1)); skellyraisesnd.play() # Initial skeleton


potions = [] # Health potion array

""" ///////////////////  """

# Timers
cooldownTime = 0 # Timer
bossCD = 0 # Timer for boss spell animations
swipeCD = 0 # Timer for boss swipe

# Enemy position update. Used to prevent loop generation of array objects.
skellypos1 = True
skellypos2 = True
skellypos3 = True
treepos1 = True
treepos2 = True
treepos3 = True

# Level completion
lvl1 = False
lvl2 = False

# Boss Phases
bossAction = 1 # Variable to store random generator number of what boss does next
bossSwipe = False
phase1 = True
phase2 = False
phase3 = False
phase4 = False

while run:
    clock.tick(28)

    if witch.health <= 0: # Check if witch is dead
        witch.dead = True
        pygame.mixer.music.stop()

    if witch.deathDone: # Screen freeze game before ending
        time.sleep(5)
        pygame.quit()

    if demonWitch.deathTimer >= 5: # Screen freeze game before ending if boss animation is done
        time.sleep(5)
        pygame.quit()

    """ ////////////////////////// """
    """      ENEMY CREATION        """

    #Skeleton Creation Station
    if skellypos1:
        if witch.x == 300:
            skellys.append(skeleton.skelly(150,200,500,4,1))
            skellyraisesnd.play()
            skellys.append(skeleton.skelly(100,30,190,2,-1))
            skellyraisesnd.play()
            skellypos1 = False

    if skellypos2 and not skellypos1 and not skellys:
        skellys.append(skeleton.skelly(700,650,840,4,-1))
        skellyraisesnd.play()
        skellys.append(skeleton.skelly(20,10,100,2,-1))
        skellyraisesnd.play()
        skellys.append(skeleton.skelly(285,270,600,6,1))
        skellyraisesnd.play()
        skellypos2 = False
        lvl1 = True

    # Evil Tree Creation
    if bgSet == 2 and witch.x >= 50 and treepos1:
        trees.append(enemytree.tree(300,witch.x))
        treepos1 = False
        treeStart1 = False
    if bgSet == 2 and not treepos1 and witch.x >= 300 and not trees and treepos2:
        trees.append(enemytree.tree(550,witch.x))
        treepos2 = False
        treeStart2 = False
    if bgSet == 2 and not treepos2 and witch.x >= 500 and not trees and treepos3:
        trees.append(enemytree.tree(700,witch.x))
        treepos3 = False
        treeStart3 = False
        lvl2 = True

    # BOSS FIGHT!
    if bgSet == 3 and demonWitch.introSound: # Check if fight start. Play intro sound
        bossintrosnd.play()
        pygame.mixer.music.stop()
        gameMusic = pygame.mixer.music.load('bmSound.mp3')
        pygame.mixer.music.play(-1)
        demonWitch.introSound = False

    if witch.x >= 480: # If player is to close. Do swipe attack
        bossSwipe = True
    else:
        bossSwipe = False
        swipeCD = 0

    if bgSet == 3 and demonWitch.health <= 175 and demonWitch.health >= 126: # Set phase 2
        phase1 = False
        phase2 = True
    elif bgSet == 3 and demonWitch.health <= 125 and demonWitch.health >= 51: # Set phase 3
        phase2 = False
        phase3 = True
    elif bgSet == 3 and demonWitch.health <= 50: # Set phase 4
        phase3 = False
        phase4 = True

    if not bossSwipe:
        if bgSet == 3 and phase1 and bossCD <= 99: # Phase 1
            bossCD += 1
        elif bgSet == 3 and phase1 and bossCD >= 100:
            demonWitch.bolt = True
            if demonWitch.boltCount == 32:
                bbAttacks.append(bossattack.bloodbolt())
                bloodboltsnd.play()
                bossCD = 0

        if bgSet == 3 and phase2 and bossCD <= 99: # Phase 2
            bossCD += 1
            bossAction = random.randint(1,2)
        elif bgSet == 3 and phase2 and bossCD >= 100:
            if bossAction == 1: # Cast blood bolt
                demonWitch.bolt = True
                if demonWitch.boltCount == 36:
                    bossCD = 0
                    bbAttacks.append(bossattack.bloodbolt())
                    bloodboltsnd.play()
            if bossAction == 2: # Cast summon
                demonWitch.summon = True
                if demonWitch.summonCount == 38:
                    bossCD = 0
                    skellys.append(skeleton.skelly(620,20,620,3,-1))
                    skellyraisesnd.play()

        if bgSet == 3 and phase3 and bossCD <= 99: # Phase 3
            bossCD += 1
            bossAction = random.randint(1,3)
        elif bgSet == 3 and phase3 and bossCD >= 100:
            if bossAction == 1: # Cast blood bolt
                demonWitch.bolt = True
                if demonWitch.boltCount == 36:
                    bossCD = 0
                    bbAttacks.append(bossattack.bloodbolt())
                    bloodboltsnd.play()
            if bossAction == 2: # Cast summon
                demonWitch.summon = True
                if demonWitch.summonCount == 36:
                    bossCD = 0
                    skellys.append(skeleton.skelly(620,5,620,3,-1))
                    skellyraisesnd.play()
            if bossAction == 3: # Cast AOE
                demonWitch.bolt = True
                if demonWitch.boltCount == 36:
                    bossCD = 0
                    aoes.append(bossaoe.aoe(random.randint(20,450)))
                    bossaoesnd.play()

        if bgSet == 3 and phase4 and bossCD <= 49: # Phase 4
            bossCD += 1
            bossAction = random.randint(1,3)
        elif bgSet == 3 and phase4 and bossCD >= 50:
            if bossAction == 1: # Cast blood bolt
                demonWitch.bolt = True
                if demonWitch.boltCount == 36:
                    bossCD = 0
                    bbAttacks.append(bossattack.bloodbolt())
                    bloodboltsnd.play()
            if bossAction == 2: # Cast summon
                demonWitch.summon = True
                if demonWitch.summonCount == 36:
                    bossCD = 0
                    skellys.append(skeleton.skelly(620,5,620,3,-1))
                    skellyraisesnd.play()
            if bossAction == 3: # Cast AOE
                demonWitch.bolt = True
                if demonWitch.boltCount == 36:
                    bossCD = 0
                    aoes.append(bossaoe.aoe(random.randint(20,450)))
                    bossaoesnd.play()
    else:
        # If player is close to boss, boss will cast swipe attack
        if bgSet == 3 and swipeCD <= 39:
            swipeCD += 1
        elif bgSet == 3 and swipeCD == 40:
            demonWitch.swipe = True
            if demonWitch.swipeCount == 28:
                swipeCD = 0
                bossswipesnd.play()
                witch.health -= demonWitch.swipeDamage

    """ -------------------------- """
    """ /////////////////////////// """
    """  Array Class Object Logic   """
    """ 
    This section contains the logic for the following:
    - Player attack collisions for each enemy
    - Boss attack collisions
    - Player, Enemy, and Boss position updates
    - Player, Enemy, and Boss health and death updates
    - Enemy collision with player
    """

    # KEY EVENT HANDLER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP: # Enables cooldown timer if special key is released early
            if event.key == pygame.K_1:
                if witch.stand:
                    cooldown = True

    # SKELETONS
    for skelly in skellys:
        if skelly.health <= 0: # Check if dead
            skelly.dead = True
            if skelly.deathDone: # If death animation is finished
                potions.append(healthpotion.healthpot(skelly.x)) # Drop potion at x of skelly
                skellys.pop(skellys.index(skelly))
        # Also check if skelly hit the player at all
        if witch.x + 30 > skelly.hitbox[0] and witch.x - 5 < skelly.hitbox[0] + skelly.hitbox[2]:
            witch.health -= skelly.damage

    # EVIL TREES
    for tree in trees: # Update the player x position so trees know where to walk
        tree.ptrackX = witch.x
        if tree.health <= 0: # Check if dead
            tree.dead = True
            if tree.deathDone:
                potions.append(healthpotion.healthpot(tree.x)) # Drop potion at x of tree
                trees.pop(trees.index(tree))
    for tree in trees:
        if tree.attacking and tree.attackCount == 22:
            witch.health -= tree.damage

    # BOSS HEALTH
    if bgSet == 3:
        if demonWitch.health <= 0:
            demonWitch.dead = True

    # CURSE COLLISION MANAGEMENT
    for curse in curses: # Check if curse is within range distance. If not, delete from array
        if curse.distance < 400:
            curse.x += curse.vel
        else:
            curses.pop(curses.index(curse))

        for skelly in skellys: # Check each skeleton to see if it was hit by player curse attack
            if curse.x + 25 > skelly.hitbox[0] and curse.x - 25 < skelly.hitbox[0] + skelly.hitbox[2]:
                if skelly.health > 0:
                    if not skelly.rise:
                        skelly.health -= curse.damage
                        try:
                            curses.pop(curses.index(curse))
                        except:
                            print("Collision Error")

        for tree in trees: # Check each tree to see if it was hit by player curse attack
            if curse.x + 25 > tree.hitbox[0] and curse.x - 25 < tree.hitbox[0] + tree.hitbox[2]:
                tree.health -= curse.damage
                curses.pop(curses.index(curse))

        # Check if curse hit boss
        if bgSet == 3:
            if curse.x + 25 > demonWitch.hitbox[0] and curse.x - 25 < demonWitch.hitbox[0] + demonWitch.hitbox[2]:
                demonWitch.health -= curse.damage
                curses.pop(curses.index(curse))


    # SPECIAL COLLISION MANAGEMENT
    for special in specials: # Check if special is within range distance. If not, delete from array
        if special.distance < 900:
            special.x += special.vel
        else:
            specials.pop(specials.index(special))

        # Check each skeleton to see if it was hit by player special attack
        for skelly in skellys:
            if special.hitbox[0] + special.hitbox[2] > skelly.hitbox[0] and special.hitbox[0] - special.hitbox[2] < skelly.hitbox[0] + skelly.hitbox[2]:
                if skelly.health > 0:
                    if not skelly.rise:
                        skelly.health -= special.damage

        for tree in trees:
            if special.hitbox[0] + special.hitbox[2] > tree.hitbox[0] and special.hitbox[0] - special.hitbox[2] < tree.hitbox[0] + tree.hitbox[2]:
                tree.health -= special.damage

        # Check if special hit the boss
        if bgSet == 3:
            if special.x + 25 > demonWitch.hitbox[0] and special.x - 25 < demonWitch.hitbox[0] + demonWitch.hitbox[2]:
                demonWitch.health -= special.damage


    # BOSS BLOOD BOLT COLLISION MANAGEMENT
    for bolt in bbAttacks: # Check if distance has been reached.
        if bolt.distance < 450:
            bolt.x -= bolt.vel
            if bolt.x - 10 < witch.hitbox[0] and bolt.x + 10 > witch.hitbox[0] - witch.hitbox[2]:
                witch.health -= bolt.damage
                bbAttacks.pop(bbAttacks.index(bolt))
        else:
            bbAttacks.pop(bbAttacks.index(bolt))

    # BOSS AOE TRACKER
    for aoe in aoes:
        if aoe.burnTimer == 5:
            aoes.pop(aoes.index(aoe))
        if witch.x + 30 > aoe.hitbox[0] and witch.x - 5 < aoe.hitbox[0] + aoe.hitbox[2]:
            witch.health -= aoe.damage

    # HEALTH POTIONS
    for potion in potions: # Check if player has run over health potion
        if witch.x + 30 > potion.hitbox[0] and witch.x - 5 < potion.hitbox[0] + potion.hitbox[2]:
            if witch.health <= 80:
                witch.health += potion.heal
                potions.pop(potions.index(potion))
            else:
                totalHeal = witch.health + potion.heal
                overHeal = totalHeal - 100
                finalHeal = potion.heal - overHeal
                witch.health += finalHeal
                potions.pop(potions.index(potion))

    # If timer is over 200, cooldown is finished.
    if cooldown and cooldownTime < 200:
        cooldownStart = 0
        cooldownTime += 1
    else:
        cooldown = False

    """ --------------------------  """
    """ /////////////////////////// """
    """      KEY EVENTS LOGIC       """

    keys = pygame.key.get_pressed()

    # Curse Attack
    if keys[pygame.K_SPACE] and witch.health > 0:
        witch.walk = False
        witch.attack = True
        if witch.attackCount == 20:
            if witch.left:
                facing = -1
            else:
                facing = 1
            curses.append(playerattack.cast(round(witch.x + witch.width // 2), facing))
            cursesnd.play()


    elif keys[pygame.K_1] and witch.health > 0:
        witch.walk = False
        if not cooldown:
            witch.attack = True
            if witch.attackCount == 20: # Cast at 4th attack animation frame
                cooldown = True
                cooldownTime = 0
                if witch.left:
                    facing = -1
                else:
                    facing = 1
                specials.append(playerspecial.cast(round(witch.x + witch.width//2), round(witch.y), facing)) # Create curse attack in array
                specialsnd.play()

    # Walk Right
    elif keys[pygame.K_RIGHT] and witch.x < 870 and witch.health > 0:
        witch.x += witch.vel
        witch.attack = False
        witch.walk = True
        witch.left = False
        witch.right = True
        witch.stand = False
        witch.standCount = 0

    # Walk Left
    elif keys[pygame.K_LEFT] and witch.x > witch.vel and witch.health > 0:
        witch.x -= witch.vel
        witch.attack = False
        witch.walk = True
        witch.left = True
        witch.right = False
        witch.stand = False
        witch.standCount = 0

    else:
        witch.attack = False
        witch.walk = False
        witch.stand = True
        witch.walkCount = 0
        witch.attackCount = 0

    """ --------------------------  """

    # If level is complete, reset witch position and change bgSet
    if lvl1 and not skellys and witch.x >= 850:
        bgSet = 2
        witch.x = 30
        witch.y = 445
        lvl1 = False
    if lvl2 and not trees and witch.x >= 850:
        bgSet = 3
        witch.x = 30
        witch.y = 445
        lvl2 = False

    redrawGameWindow()
pygame.quit()

