
import pygame
from Bomb import *
import Player
from Globals import *

def collisionDetection(oldPos):
   with players_lock:
      collidedBombSprite = pygame.sprite.spritecollideany(Player.playerCar, bombsGroup,
                                             collided=None)

      collidedWallIndex = Player.playerCar.rect.collidelist(Walls)
      collidedBoxIndex = Player.playerCar.rect.collidelist(BoxesRects) 

   #if collidedBombSprite and not justPlacedBomb:
   #    with players_lock:
   #        Player.playerCar.rect = oldPos.copy()

   for bomb in bombsGroup:

       if bomb == lastPlacedBomb and lastPlacedBomb is not None:
           continue
       
       if Player.playerCar.rect.colliderect(bomb.rect):
           Player.playerCar.rect = oldPos.copy()

   if collidedWallIndex != -1:
       with players_lock:
           Player.playerCar.rect = oldPos.copy()
   elif collidedBoxIndex != -1:
       with players_lock:
           Player.playerCar.rect = oldPos.copy()

oldPos = 0
Walls = []
BoxesRects = []
BoxesSurfaces = []
justPlacedBomb = False
lastPlacedBomb = None

