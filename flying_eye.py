import pygame
import entity
import math
import time

class Flying_eye(entity.Entity):
    hp = 100
    attackDamage = None
    animationType = 0
    velocity = pygame.Vector2(10, 17)
        
    idleSprites = []
    attackSprites = []
    weaponSprites = []
    takeHitSpriets = []
    flightSprites = []
    deathSprites = []

    currentAttackSprite = 0
    currentFlightSprite = 0
    currentTakeHitSprite = 0
    currentDeathSprite = 0

    loopTime = 0

    def attack(self):
        if time.time() - self.attackCoolDown > 3:
            self.idle = False
            self.isAttacking = True
            self.attackCoolDown = time.time()
        else:
            self.idle = True  
    
    def update(self, player): # AI
        self.loopTime += 0.1 # This will overflow at some point but idgaf
        self.rect.y += int(math.sin(self.loopTime) * 5)  

        if self.universalEnemyMovement(player, -250, 200):
            # print(self.animationType)
            self.attack()

    def makeListWithSprites(self):
            self.attackSprites = self.getEnemySpriteSubFunction("Flying eye", "Attack", 8)
            self.deathSprites = self.getEnemySpriteSubFunction("Flying eye", "Death", 4)
            self.flightSprites = self.getEnemySpriteSubFunction("Flying eye", "Flight", 8)
            self.takeHitSprites = self.getEnemySpriteSubFunction("Flying eye", "Take Hit", 4)

            return self.flightSprites[0] # for initialization
    

    def animate(self):
    
        if self.animationType == 1: # attack
            self.currentAttackSprite = self.createAnimations(self.currentAttackSprite, self.attackSprites, 0.25)

        elif self.animationType == 2 or self.animationType == 0: # fly
            self.currentFlightSprite = self.createAnimations(self.currentFlightSprite, self.flightSprites, 0.17)  

        elif self.animationType == 3: # take hit
            self.currentTakeHitSprite = self.createAnimations(self.currentTakeHitSprite, self.takeHitSprites, 0.17) 

        elif self.animationType == 4: # death    
            self.currentDeathSprite = self.createAnimations(self.currentDeathSprite, self.deathSprites, 0.3) 
            
    def flying_eyeActions(self, player):

        self.setAnimation()
        self.animate()
        self.update(player)
        self.invert(player)   