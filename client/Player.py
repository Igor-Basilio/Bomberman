
import pygame
import numpy as np
from Spritesheet import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        self.color = color
        self.image = goblin1FrameArray[1]
        self.rect = self.image.get_rect() 

        self.rect.width  -= TILESIZE / 4
        self.rect.height -= TILESIZE / 4

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            playerCar.moveLeft(10)
        if keys[pygame.K_RIGHT]:
            playerCar.moveRight(10)
        if keys[pygame.K_DOWN]:
            playerCar.moveForward(10)
        if keys[pygame.K_UP]:
            playerCar.moveBack(10)

    def moveRight(self, pixels):
        self.rect.x += pixels

    def moveLeft(self, pixels):
        self.rect.x -= pixels

    def moveForward(self, speed):
        self.rect.y += int(speed * speed/10)

    def moveBack(self, speed):
        self.rect.y -= int(speed * speed/10)


clock = pygame.time.Clock()
color = list(np.random.choice(range(256), size=3))
playerCar = Sprite(color, 20, 30)
playerCar.rect.x = np.random.choice(range(SCREEN_WIDTH  - 30))
playerCar.rect.y = np.random.choice(range(SCREEN_HEIGHT - 20))

