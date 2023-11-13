import pygame
import entity
import bomb
import time



class Goblin(entity.Entity):
    hp = 100
    attackDamage = None
    animationType = 0
    attackCoolDown = 0
    velocity = pygame.Vector2(10, 17)

    attack = False
    invertSprite = False
    stopAttacksFromAddingBombs = False
    isReadyToInitBomb = False

    idleSprites = []
    attackSprites = []
    weaponSprites = []
    takeHitSpriets = []
    runSprites = []
    deathSprites = []
    bombs = []

    currentAttackSprite = 0
    currentIdleSprite = 0
    currentRunSprite = 0
    currentTakeHitSprite = 0
    currentDeathSprite = 0

    def update(self, player): # AI
            minX = min(player.rect.x, self.rect.x + 250)
            maxX = max(player.rect.x, self.rect.x - 250)

            a = maxX - minX
            if a < 100 and a > 50: self.velocity.x = a
            

            if self.isAttacking != True:
                
                
                if time.time() - self.attackCoolDown > 3:

                    if self.rect.x > player.rect.x:
                        self.invertSprite = True
                    self.isMoving = False 
                    
                    self.isAttacking = True    
                    self.stopAttacksFromAddingBombs = False  
                    self.attackCoolDown = time.time()

                if a < 57: # for getting too close to the player
                    self.invertSprite = True

                    if self.rect.x > player.rect.x:
                        self.rect.x += player.velocity.x
                    else:
                        self.invertSprite = False
                        self.rect.x -= player.velocity.x

                    if self.velocity.x > 0: 
                        self.isMoving = True  
                    
                    else:
                        self.isMoving = False

                elif a > 100: # for getting too far away
                    if self.rect.x > player.rect.x:
                        self.invertSprite = True
                        self.rect.x -= self.velocity.x * 0.07

                    else:
                        self.invertSprite = False
                        self.rect.x += self.velocity.x * 0.07

                    if self.velocity.x > 0: 
                        self.isMoving = True
                    
                    else:
                        self.isMoving = False

                else:
                    self.isMoving = False

    def attack(self):
        self.bombs.append(bomb.Bomb((24, 39), "", (self.rect.x + self.rect.width + 33, self.rect.y + 12), False))
        self.bombs[len(self.bombs) - 1].texture = self.bombs[len(self.bombs) - 1].makeListWithSprites() 
        self.bombs[len(self.bombs) - 1].initBombPosY()   # load sprites for the last bomb added to the list AKA the line above
        self.stopAttacksFromAddingBombs = True
        self.attackCoolDown = time.time()
  
    def makeListWithSprites(self):
            self.attackSprites = self.getEnemySpriteSubFunction("Goblin", "Attack3", 12)
            self.weaponSprites = self.getEnemySpriteSubFunction("Goblin", "Bomb_sprite", 19)
            self.deathSprites = self.getEnemySpriteSubFunction("Goblin", "Death", 4)
            self.idleSprites = self.getEnemySpriteSubFunction("Goblin", "Idle", 4)
            self.runSprites = self.getEnemySpriteSubFunction("Goblin", "Run", 8)
            self.takeHitSprites = self.getEnemySpriteSubFunction("Goblin", "Take Hit", 4)

            return self.idleSprites[0] # for initialization
    
    def animate(self):
    
        if self.animationType == 1: # attack
            self.currentAttackSprite = self.createAnimations(self.currentAttackSprite, self.attackSprites, 0.23)

        elif self.animationType == 2: # run
            self.currentRunSprite = self.createAnimations(self.currentRunSprite, self.runSprites, 0.2) 

        elif self.animationType == 0: # idle
            self.currentIdleSprite = self.createAnimations(self.currentIdleSprite, self.idleSprites, 0.15)  

        elif self.animationType == 3: # take hit
            self.currentTakeHitSprite = self.createAnimations(self.currentTakeHitSprite, self.takeHitSprites, 0.17) 

        elif self.animationType == 4: # death    
            self.currentDeathSprite = self.createAnimations(self.currentDeathSprite, self.deathSprites, 0.3) 

    def goblinActions(self, player):
        # print(len(self.bombs))  

        self.setAnimation()
        self.animate()
        self.update(player)
        self.invert(player)   
