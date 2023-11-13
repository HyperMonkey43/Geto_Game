import pygame
import entity
import projectile


class Mushroom_projectile(projectile.Projectile):
    velocityX = 30
    
    def __init__(self, size, position, mushroom):
        self.rect = pygame.Rect(position, size)
        self.isAttacking = True

        if mushroom.invertSprite:
            self.velocityX *= -1

        self.createListWithSprites("images/Enemies/Mushroom/Projectile_sprite.png", 3, 8, 50)    

    def update(self):
        self.rect.x += self.velocityX
    