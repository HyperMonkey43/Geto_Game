import pygame 
import projectile

class Bomb(projectile.Projectile):
    velocityX = 10
    velocityY = 10
    isFalling = False
    gravity = 1
    throwHeight = 10
    

    def __init__(self, size, position, goblin):
        self.rect = pygame.Rect(position, size)
        self.isAttacking = True

        if goblin.invertSprite:
            self.velocityX *= -1

        self.texture = self.createListWithSprites("images/Enemies/Goblin/Bomb_sprite.png", 3, 19, 100)

    def update(self):
        self.rect.x += self.velocityX

        if self.isFalling:
            self.rect.y -= self.velocityY
            self.velocityY -= self.gravity

            if self.velocityY < -self.throwHeight:
                self.isFalling = False
                self.velocityY = self.throwHeight 