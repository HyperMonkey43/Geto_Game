import pygame
import entity


class Projectile(entity.Entity):
    animationType = 0

    attackSprites = []
    destroySprites = []

    currentAttackSprite = 0
    currentDestroySprite = 0

    
    def createListWithSprites(self, imagePath, lenAttack, lenDestroy, imgSize):
        image = pygame.image.load(imagePath)    

        if len(self.attackSprites) == 0 and len(self.destroySprites) == 0:
            for i in range(0, lenAttack):
                self.attackSprites.append(self.getImage(image, imgSize, imgSize, 3, (0, 0, 0), i)) # load sprites to list
            for i in range(lenAttack, lenDestroy):
                self.destroySprites.append(self.getImage(image, imgSize, imgSize, 3, (0, 0, 0), i))

        return self.attackSprites[0]        

            
    def setAnimation(self):
        if self.isAttacking:
            self.animationType = 0
        elif self.dead:
            self.animationType = 1    
            
    
    def createAnimations(self, currentSprite, spriteList, animationSpeed):
        currentSprite += animationSpeed

        if currentSprite >= len(spriteList):
            match self.animationType:
                case 0:
                    currentSprite = 2

                case 1:
                    self.delete = True  
                    return            

        self.texture = spriteList[int(currentSprite)]    
        return currentSprite

    def animate(self):
        match self.animationType:
            case 0:
                self.currentAttackSprite = self.createAnimations(self.currentAttackSprite, self.attackSprites, 0.1)   
                
            case 1:
                self.currentDestroySprite = self.createAnimations(self.currentDestroySprite, self.destroySprites, 0.5)   
                    

    def checkCollisions(self, player, game):
        if pygame.Rect.colliderect(player.rect, self.rect) or self.rect.x < -100 or self.rect.x > game.resolution.x:
            self.dead = True
            self.isAttacking = False
            self.velocityX = 0

    def projectileActions(self, player, game):
        self.setAnimation()
        self.animate()
        self.update()
        self.checkCollisions(player, game)