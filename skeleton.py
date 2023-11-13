import pygame
import entity
import time

class Skeleton(entity.Entity):
    attackDamage = None
    animationType = 0
    spriteRotation = 1
    velocity = pygame.Vector2(10, 17)
    
    invertSprite = False
    idle = True
    attack = False
    isAttacking = False
    takeHit = False
    isMoving = False

    idleSprites = []
    attackSprites = []
    weaponSprites = []
    takeHitSpriets = []
    runSprites = []
    deathSprites = []

    currentAttackSprite = 0
    currentIdleSprite = 0
    currentRunSprite = 0
    currentTakeHitSprite = 0
    currentDeathSprite = 0
    currentShieldSprite = 0
    
    def attack(self):
        if time.time() - self.attackCoolDown > 3:
            self.isAttacking = True
            self.attackCoolDown = time.time()

    def update(self, player): # AI
        if self.universalEnemyMovement(player, -250, 200, 800):
            self.attack()
        
        distance = abs(player.rect.x - self.rect.x)
        
        if distance < 750 and not self.isAttacking and not self.takeHit and not self.isMoving:
            self.shield = True
        else:
            self.shield = False    

    def makeListWithSprites(self):
            self.attackSprites = self.getEnemySpriteSubFunction("Skeleton", "Attack", 8)
            self.weaponSprites = self.getEnemySpriteSubFunction("Skeleton", "Shield", 1)
            self.deathSprites = self.getEnemySpriteSubFunction("Skeleton", "Death", 4)
            self.idleSprites = self.getEnemySpriteSubFunction("Skeleton", "Idle", 4)
            self.runSprites = self.getEnemySpriteSubFunction("Skeleton", "Walk", 4)
            self.takeHitSprites = self.getEnemySpriteSubFunction("Skeleton", "Take Hit", 4)

            return self.idleSprites[0] # for initialization
    
        
    def animate(self):
    
        if self.animationType == 1: # attack
            self.currentAttackSprite = self.createAnimations(self.currentAttackSprite, self.attackSprites, 0.15)

        elif self.animationType == 2: # run
            self.currentRunSprite = self.createAnimations(self.currentRunSprite, self.runSprites, 0.13) 

        elif self.animationType == 0: # idle
            self.currentIdleSprite = self.createAnimations(self.currentIdleSprite, self.idleSprites, 0.17)  

        elif self.animationType == 3: # take hit
            self.currentTakeHitSprite = self.createAnimations(self.currentTakeHitSprite, self.takeHitSprites, 0.17) 

        elif self.animationType == 4: # death    
            self.currentDeathSprite = self.createAnimations(self.currentDeathSprite, self.deathSprites, 0.3) 

        elif self.animationType == 5: # shield 
            self.currentShieldSprite = self.createAnimations(self.currentShieldSprite, self.weaponSprites, 0.05)
            
    def skeletonActions(self, player):
        if not self.dead:
            self.update(player)
            self.setAnimation(hasShield=True)
        else:
            self.animationType = 4
   
        self.animate()
        self.invert(player)           