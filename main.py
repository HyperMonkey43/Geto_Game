import pygame
import random
import game
import entity
import player
import goblin
import skeleton
import mushroom
import flying_eye
import bomb
import mushroom_projectile

def staticloadEntities():
    global backgrounds, player, PlayBtn, ControlsBtn, QuitBtn, goblins, skeletons, mushrooms, flying_eyes, mushroom_projectiles, bombs

    backgrounds = []      
    goblins = [] 
    skeletons = []
    mushrooms = []
    flying_eyes = []
    bombs = []
    mushroom_projectiles = []

    '''

    !!! EVERYTHING IS SCALED UP BY 3 LIL N****S !!!

    SIZES:
    Player --- W = 75, H = 132
    Goblin --- W = 96, H = 105
    Skeleton --- W = 108, H = 150
    Mushroom --- W = 63, H = 108
    Flying Eye --- W = 120, H = 81
    Bomb --- W = 24, H = 39
    
    OFFSETS:
    Player --- X = 257, Y = 235        Att1 --- X = 137, Y = 51 * 3, 118 ??? kvo e tva 118 mai trqq da e 195????
    Goblin --- X = 174, Y = 150
    Skeleton --- X = 180, Y = 150
    Mushroom --- X = 192, Y = 150
    Flying Eye --- X = 171, Y = 189
    Bomb --- X = 144, Y =  129
    Mushroom Projectile Offset from Mushroom --- X = -53, Y = 80
    Bomb Offset From Goblin --- X = goblins[0].rect.x + goblins[0].rect.width + 33, Y = goblins[0].rect.y + 12

    '''
                
    player = player.Player((75/3, 132/3), "", (25, game.resolution.y - 131), False) 
    player.texture = player.getPlayerSprites()
  
    for i in range(2):
        backgrounds.append(entity.Entity(game.resolution, "images/Backgrounds/backgroundLaptop.png",(i * game.resolution.x, 0), True))

    for i in range(1, random.randint(2, 2)):
        goblins.append(goblin.Goblin((96, 105), "", (i*350, game.resolution.y - 150), False))
        goblins[i - 1].texture = goblins[i - 1].makeListWithSprites()

    for i in range(1, random.randint(2, 2)):
        mushrooms.append(mushroom.Mushroom((63, 108), "", (i * 350, game.resolution.y - 150), False))
        mushrooms[i - 1].texture = mushrooms[i - 1].makeListWithSprites()

    for i in range(1, random.randint(2, 2)):
        flying_eyes.append(flying_eye.Flying_eye((120, 81), "", (i*200, game.resolution.y - 300), False, entityType="flying_eye"))
        flying_eyes[i - 1].texture = flying_eyes[i - 1].makeListWithSprites()    

    for i in range(1, random.randint(2, 2)):
        skeletons.append(skeleton.Skeleton((108, 150), "", (i*350, game.resolution.y - 150), False))
        skeletons[i - 1].texture = skeletons[i - 1].makeListWithSprites()    

    bombs.append(bomb.Bomb((100, 100), (200, 400), goblins[0]))

def createProjectiles(enemy, enemyType):
    if enemy.createProjectile:
        if enemyType == "mushroom":
            if enemy.invertSprite:
                position = (enemy.rect.x - 21, enemy.rect.y + 40)   
            else:
                position = (enemy.rect.x, enemy.rect.y + 40)

            mushroom_projectiles.append(mushroom_projectile.Mushroom_projectile((29, 29), position, enemy))
            
        enemy.createProjectile = False    

def draw():
    game.drawMultiple(backgrounds, (0, 0))

    game.screen.blit(player.texture, (player.rect.x - 257, player.rect.y - 235))
   
    game.drawMultiple(goblins, (174, 150))
    # game.drawMultiple(skeletons, (180, 150))
    # game.drawMultiple(mushrooms, (192, 150))
    # game.drawMultiple(flying_eyes, (171, 189))
    # game.drawMultiple(mushroom_projectiles, (21, 21))
    game.drawMultiple(bombs, (0, 0))

def deleteEnemies(game):
    game.offloadDeadEnemies(skeletons)
    game.offloadDeadEnemies(goblins)
    game.offloadDeadEnemies(mushrooms)
    game.offloadDeadEnemies(flying_eyes)
    game.offloadDeadEnemies(mushroom_projectiles)


def checkEnemyHitboxes(enemyList, attackType, hasShield=False):
    for i in enemyList:
        if pygame.Rect.colliderect(player.attackRect, i.rect):
                i.takeHitFunction(attackType, hasShield)            

def checkAttackCollisions():
    match player.attackType:
        case 1:
            checkEnemyHitboxes(skeletons, 1, True)
            checkEnemyHitboxes(goblins, 1)
            checkEnemyHitboxes(mushrooms, 1)
            checkEnemyHitboxes(flying_eyes, 1)

            player.attackType = 0    

        case 2:
            checkEnemyHitboxes(skeletons, 2, True)
            checkEnemyHitboxes(goblins, 2)
            checkEnemyHitboxes(mushrooms, 2)
            checkEnemyHitboxes(flying_eyes, 2)

            player.attackType = 0    
    
def scrollBackgrounds(backgrounds, player, game):
    if player.outOfBounds(game):
        if backgrounds[1].rect.x <= 0:
            backgrounds[0].rect.x = backgrounds[1].rect.x + backgrounds[1].rect.width
        if backgrounds[0].rect.x <= 0:
            backgrounds[1].rect.x = backgrounds[0].rect.x + backgrounds[0].rect.width    
        

        for i in range(0, 2):
            backgrounds[i].rect.x -= backgrounds[i].scrollSpeed

def checkEnemyBounds(enemy):
    if not (enemy.rect.x > game.resolution.x or (enemy.rect.x + enemy.rect.w) < 0):
        return True
    return False

def enemyActions():
    for i in goblins:
        if checkEnemyBounds(i): i.goblinActions(player)
    
    for i in skeletons:
        if checkEnemyBounds(i): i.skeletonActions(player)
        
    for i in mushrooms:
        if checkEnemyBounds(i): 
            i.mushroomActions(player)
            createProjectiles(i, "mushroom")
        
    for i in flying_eyes:
        if checkEnemyBounds(i): i.flying_eyeActions(player)

    for i in mushroom_projectiles:
        i.projectileActions(player, game)    

    for i in bombs:
        i.projectileActions(player, game)    


# Before Starting the Game
game = game.Game()
staticloadEntities()

while True:
    while game.startMenu:       
        game.startMenu()
    
    game.getEvent()

    scrollBackgrounds(backgrounds, player, game)


    checkAttackCollisions()

    player.playerActions()

    deleteEnemies(game)

    enemyActions()
    draw()
    game.update()
    game.clock.tick(60)

    '''
    TODO:
    - attack type 2 of player plays take hit animations twice
    - skeleton shield animation when getting hit is shit
    - make projectile as a parent class, things to change:
        image path and amount of frames
        velocity and update function in child classes not in parent
    '''