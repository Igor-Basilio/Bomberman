
import pygame
from Setup import *

sprite_sheet_image = pygame.image.load('assets/bomb_party_v4.png').convert_alpha()

def getImage(sheet, width, height, scale, color, frame, pos):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (pos[0] + width * frame, pos[1], width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(color)
    return image

TILESIZE = 16
TILES_SCALE_FACTOR = 4
GOBLIN_SCALE_FACTOR = 3
GOBLIN_1INDEX = 14

sidewaysBrickWall = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                             TILES_SCALE_FACTOR,
                             BLACK, 0, (0, 0)).convert()

goblin1FrameArray = [getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                              GOBLIN_SCALE_FACTOR,
                              BLACK, i,
                              (0, GOBLIN_1INDEX * TILESIZE))
                              for i in range(10)]


grassTile = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                     TILES_SCALE_FACTOR,
                     BLACK, 0, (3 * TILESIZE, TILESIZE)).convert()

