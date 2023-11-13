import pygame
import entity
import time



class Player(entity.Entity):
    hp = 100
    velocity = pygame.Vector2(10, 17)
    gravity = 1
    jumpHeight = 17
    isJumping = False   
    isRunning = True
    isAttacking1 = False
    isAttacking2 = False
    
    
    attackType = 0
    animationType = 0
    invertSprite = False


    currentIdleSprite = 0
    currentJumpSprite = 0
    currentFallSprite = 0
    currentRunSprite = 0
    currentAttack1Sprite = 0
    currentAttack2Sprite = 0

    idleSprites = []
    jumpSprites = []
    fallSprites = []
    runSprites = []
    attack1Sprites= []
    attack2Sprites= []

 
    def update(self):
        keys = pygame.key.get_pressed()


        if not self.isAttacking1 and not self.isAttacking2:
            if keys[pygame.K_a]:
                self.rect.x -= self.velocity.x
                self.invertSprite = True
                self.isRunning = True

            elif keys[pygame.K_d]:
                self.rect.x += self.velocity.x
                self.invertSprite = False
                self.isRunning = True

            else:
                self.isRunning = False

            if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                self.isJumping = True  

        if time.time() - self.attackCoolDown > 0.1:
            if pygame.mouse.get_pressed()[0] or keys[pygame.K_e]:
                self.isAttacking1 = True 
                self.setAttackRect()

            elif pygame.mouse.get_pressed()[2] or keys[pygame.K_f]:
                self.isAttacking2 = True 
                self.setAttackRect()

            self.attackCoolDown = time.time()

    def setAttackRect(self):
        if self.invertSprite:
            self.attackRect = pygame.Rect(self.rect.x - 181, self.rect.y + 53, 153, 65) # for x 153 is the offset + 28 for the width of the player sprite

        else:
            self.attackRect = pygame.Rect(self.rect.x + 137, self.rect.y + 53, 153, 65)    


    def jump(self):
        if self.isJumping:
            self.rect.y -= self.velocity.y
            self.velocity.y -= self.gravity

            if self.velocity.y < -self.jumpHeight:
                self.isJumping = False
                self.velocity.y = self.jumpHeight    
            
    def outOfBounds(self, game):
        if self.rect.x <= 0: # left bound
            self.rect.x = 0

        elif self.rect.x + self.rect.width >= game.resolution.x - 200: # right bound
            self.rect.x = game.resolution.x - 200 - (self.rect.width + 1)  
            return True  
        
    def invert(self):
        if self.invertSprite:
            self.texture = pygame.transform.flip(self.texture, True, False)
            self.texture.set_colorkey((0, 0, 0))

    def getPlayerSpriteSubFunction(self, imagePath,  listRange):    
        black = (0, 0, 0)
        spriteList = []

        imagePathLocal = "images/Player/.png"[:14] + imagePath + "images/Player/.png"[14:]
        image = pygame.image.load(imagePathLocal)
        for i in range(listRange):
            spriteList.append(self.getImage(image, 200, 200, 3, black, i)) # load sprites to list

        return spriteList    

    def getPlayerSprites(self):
        self.idleSprites = self.getPlayerSpriteSubFunction("idle", 8)
        self.jumpSprites = self.getPlayerSpriteSubFunction("Jump", 2)
        self.fallSprites = self.getPlayerSpriteSubFunction("Fall", 2)
        self.runSprites = self.getPlayerSpriteSubFunction("Run", 8)
        self.attack1Sprites = self.getPlayerSpriteSubFunction("Attack1", 6)
        self.attack1Sprites.pop(0)
        self.attack2Sprites = self.getPlayerSpriteSubFunction("Attack2", 6)

        return self.idleSprites[0] # for initialization
    
    def setAnimation(self):
        if self.isAttacking1:
            self.animationType = 4

        elif self.isAttacking2:
            self.animationType = 5

        elif self.isJumping:       
            if self.velocity.y >= 0:
                self.animationType = 1
            else:
                self.animationType = 2

        elif self.isRunning: 
            self.animationType = 3 

        else: 
            self.animationType = 0    

    def createAnimations(self, currentSprite, spriteList, animationSpeed, attack):
        currentSprite += animationSpeed

        if currentSprite >= len(spriteList):
            currentSprite = 0

            # for cancelling attacks
            match attack:
                case 1:
                    self.isAttacking1 = False
                    self.currentAttack1Sprite = 0
                    self.animationType = 0
                    self.attackCoolDown = time.time()
                
                case 2:
                    self.isAttacking2 = False
                    self.currentAttack2Sprite = 0
                    self.animationType = 0    
                    self.attackCoolDown = time.time()

        self.texture = spriteList[int(currentSprite)]    
        return currentSprite 

    def animate(self):
    
        if self.animationType == 4: #att 1
            self.currentAttack1Sprite = self.createAnimations(self.currentAttack1Sprite, self.attack1Sprites, 0.25, 1)

        elif self.animationType == 5: #att 2
            self.currentAttack2Sprite = self.createAnimations(self.currentAttack2Sprite, self.attack2Sprites, 0.2, 2) 

        elif self.animationType == 0: # idle
            self.currentIdleSprite = self.createAnimations(self.currentIdleSprite, self.idleSprites, 0.17, 0)  

        elif self.animationType == 1: # jump
            self.currentJumpSprite = self.createAnimations(self.currentJumpSprite, self.jumpSprites, 0.17, 0) 

        elif self.animationType == 2: # fall    
            self.currentFallSprite = self.createAnimations(self.currentFallSprite, self.fallSprites, 0.3, 0) 

        elif self.animationType == 3: # run   
            self.currentRunSprite = self.createAnimations(self.currentRunSprite, self.runSprites, 0.2, 0)

    def checkAttackType(self):
        if self.isAttacking1:
            self.attackType = 1

        elif self.isAttacking2:
            self.attackType = 2

        else:
            self.attackType = 0    

    def playerActions(self):
        self.invertSprite
        self.setAnimation()
        self.animate()
        self.update()
        self.jump()
        self.invert()  
        self.checkAttackType()