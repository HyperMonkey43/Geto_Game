import pygame
import time




class Entity:
    texture = None
    rect = None
    attackRect = pygame.Rect(0, 0, 0, 0)
    scrollSpeed = 3
    animationType = 0
    attackCoolDown = 0

    
    shield = False
    hp = 65 # TODO: overload in constructor
    isMoving = False
    idle = True
    isAttacking = False
    takeHit = False
    invertSprite = False
    createProjectile = False
    dead = False
    delete = False

    def __init__(self, size, texturePath, position, opaque, entityType="None"):
        self.rect = pygame.Rect(position, size)

        if len(texturePath) > 0 :
            if not opaque:
                self.texture = pygame.image.load(texturePath)
            elif opaque:
                self.texture = pygame.image.load(texturePath).convert_alpha()    

        if entityType == "flying_eye":
            self.isMoving = True
            self.idle = False

    def getImage(self, spriteSheet, width, height, scale, color, frame):
        image = pygame.Surface((width, height)).convert_alpha()        
        image.blit(spriteSheet, (0, 0), ((frame * width), 0, width, height))    
       
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image
    
    def universalEnemyMovement(self, player, movementBoundL=-60, movementBoundR=50, ignoreDistance=600):
        distance = abs(player.rect.x - self.rect.x)
        if distance < 70 and distance > 30: self.velocity.x = distance

        if distance < movementBoundL: # for getting too close to the player
            self.animationType = 2
            self.idle = False
            self.isMoving = True

            if self.rect.x > player.rect.x:
                self.rect.x += player.velocity.x
                
            else:
                self.rect.x -= player.velocity.x


        elif distance > movementBoundR and distance < ignoreDistance: # for getting too far away
            self.animationType = 2
            self.idle = False
            self.isMoving = True

            if self.rect.x > player.rect.x:
                self.rect.x -= self.velocity.x * 0.07

            else:
                self.rect.x += self.velocity.x * 0.07

        else:
            self.isMoving = False
            self.idle = True
            return True             

    def takeHitFunction(self, damage, hasShield=False):
        if hasShield and self.shield:
            self.shield = False
        else:
            self.takeHit = True    
            self.hp -= damage 
    
    def getEnemySpriteSubFunction(self, enemy, imagePath,  listRange, x=150, y=150):    

        black = (0, 0, 0)
        spriteList = []
        match enemy:
            case "Goblin":
                imagePathLocal = "images/Enemies/Goblin/" + imagePath + ".png"

            case "Skeleton":
                imagePathLocal = "images/Enemies/Skeleton/" + imagePath + ".png"

            case "Mushroom":
                imagePathLocal = "images/Enemies/Mushroom/" + imagePath + ".png"

            case "Flying eye":
                imagePathLocal = "images/Enemies/Flying eye/" + imagePath + ".png"

            case "Bomb":
                imagePathLocal = "images/Enemies/Goblin/Bomb_sprite.png"    
                 

        image = pygame.image.load(imagePathLocal)
        
        for i in range(listRange):
            spriteList.append(self.getImage(image, x, y, 3, black, i)) # load sprites to list

        return spriteList

    def invert(self, player):
        if self.rect.x > player.rect.x:
            self.invertSprite = True
        else:
            self.invertSprite = False

        if self.invertSprite:
            self.texture = pygame.transform.flip(self.texture, True, False)
            self.texture.set_colorkey((0, 0, 0))

    def setAnimation(self, hasShield=False):
        if self.hp <= 0:
            self.animationType = 4 
            self.dead = True
        
        elif self.takeHit: 
            self.animationType = 3
        
        elif self.isAttacking:
            self.animationType = 1

        elif self.isMoving: 
            self.animationType = 2 
            
        elif hasShield and self.shield:
            self.animationType = 5   

        elif self.idle: 
            self.animationType = 0


    def createAnimations(self, currentSprite, spriteList, animationSpeed, projectileEntity=False):
        currentSprite += animationSpeed

        if currentSprite >= len(spriteList):
            currentSprite = 0

            # for cancelling attacks
            match self.animationType:
                case 1: 
                    self.isAttacking = False
                    self.currentAttackSprite = 0
                    self.animationType = 0
                    self.attackCoolDown = time.time()  
                    if projectileEntity:
                        self.createProjectile = True


                case 3:
                    self.takeHit = False
                    self.currentTakeHitSprite = 0
                    self.animationType = 0

                case 4:    
                    self.delete = True

        self.texture = spriteList[int(currentSprite)]    
        return currentSprite 