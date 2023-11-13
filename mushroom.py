import pygame
import entity
import time 

class Mushroom(entity.Entity):
    hp = 100
    attackDamage = None
    spriteRotation = 1
    velocity = pygame.Vector2(10, 17)
    

    idleSprites = []
    attackSprites = []
    weaponSprites = []
    takeHitSpriets = []
    runSprites = []
    deathSprites = []

    attackCoolDown = 0
    currentAttackSprite = 0
    currentIdleSprite = 0
    currentRunSprite = 0
    currentTakeHitSprite = 0
    currentDeathSprite = 0

    def attack(self):
        if time.time() - self.attackCoolDown > 3:
            self.isAttacking = True
            self.attackCoolDown = time.time()

    def update(self, player): # AI
        if self.universalEnemyMovement(player, -370, 265, 350):
            self.attack()

    def makeListWithSprites(self):
            self.attackSprites = self.getEnemySpriteSubFunction("Mushroom", "Attack", 8)
            self.weaponSprites = self.getEnemySpriteSubFunction("Mushroom", "Projectile_sprite", 3)  #New File needed
            self.deathSprites = self.getEnemySpriteSubFunction("Mushroom", "Death", 4)
            self.idleSprites = self.getEnemySpriteSubFunction("Mushroom", "Idle", 4)
            self.runSprites = self.getEnemySpriteSubFunction("Mushroom", "Run", 8)
            self.takeHitSprites = self.getEnemySpriteSubFunction("Mushroom", "Take Hit", 4)

            return self.idleSprites[0] # for initialization
    
        
    def animate(self):
    
        if self.animationType == 1: # attack
            self.currentAttackSprite = self.createAnimations(self.currentAttackSprite, self.attackSprites, 0.25, True)

        elif self.animationType == 2: # run
            self.currentRunSprite = self.createAnimations(self.currentRunSprite, self.runSprites, 0.2) 

        elif self.animationType == 0: # idle
            self.currentIdleSprite = self.createAnimations(self.currentIdleSprite, self.idleSprites, 0.17) 

        elif self.animationType == 3: # take hit
            self.currentTakeHitSprite = self.createAnimations(self.currentTakeHitSprite, self.takeHitSprites, 0.17) 

        elif self.animationType == 4: # death    
            self.currentDeathSprite = self.createAnimations(self.currentDeathSprite, self.deathSprites, 0.3) 

    def mushroomActions(self, player):
        self.setAnimation()
        self.animate()
        self.update(player)
        self.invert(player)   