
import pygame
import numpy as np
from Spritesheet import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        self.color = color
        self.image = goblin1FrameArray[1]
        self.rect = self.image.get_rect()

        self.rect.width  -= TILESIZE
        self.rect.height -= TILESIZE

    def move(self):
        keys = pygame.key.get_pressed()

        speed = 6
        if keys[pygame.K_LEFT]:
            playerCar.moveLeft(speed)
        if keys[pygame.K_RIGHT]:
            playerCar.moveRight(speed)
        if keys[pygame.K_DOWN]:
            playerCar.moveForward(speed)
        if keys[pygame.K_UP]:
            playerCar.moveBack(speed)

#    def moveRight(self, pixels):
#        self.rect.x += pixels
#
#    def moveLeft(self, pixels):
#        self.rect.x -= pixels
    
    def moveRight(self, speed):
        self.rect.x += int(speed * speed/10)

    def moveLeft(self, speed):
        self.rect.x -= int(speed * speed/10)

    def moveForward(self, speed):
        self.rect.y += int(speed * speed/10)

    def moveBack(self, speed):
        self.rect.y -= int(speed * speed/10)


clock = pygame.time.Clock()
color = list(np.random.choice(range(256), size=3))
playerCar = Sprite(color, 20, 30)
playerCar.rect.x = np.random.choice(range(SCREEN_WIDTH  - 30))
playerCar.rect.y = np.random.choice(range(SCREEN_HEIGHT - 20))

