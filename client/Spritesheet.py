
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
GOBLIN_1INDEX = 14

TILES_SCALE_FACTOR = 4
GOBLIN_SCALE_FACTOR = 3
BOMB_SCALE_FACTOR = 2.5

sidewaysBrickWall = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                             TILES_SCALE_FACTOR,
                             BLACK, 0, (0, 0)).convert()

goblin1FrameArray = [getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                              GOBLIN_SCALE_FACTOR,
                              BLACK, i,
                              (0, GOBLIN_1INDEX * TILESIZE)).convert()
                              for i in range(10)]

EndFlameLeftPosition = (0, 18*TILESIZE)
MidFlamePosition = (TILESIZE, 18 * TILESIZE)
EndFlameRightPosition = (3 * TILESIZE, 18 * TILESIZE)
FourWayFlamePosition = (2 * TILESIZE, 18 * TILESIZE)
BottomFlamePosition = (14 * TILESIZE, 15 * TILESIZE)
TopFlamePosition = (14 * TILESIZE, 13 * TILESIZE)

grassTile = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                     TILES_SCALE_FACTOR,
                     BLACK, 0, (3 * TILESIZE, TILESIZE)).convert()

BombFrameArray = [getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                          BOMB_SCALE_FACTOR,
                          BLACK, i, (4 * TILESIZE, 18 * TILESIZE)).convert()
                          for i in range(3)]

EndFlameLeft  = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                    BOMB_SCALE_FACTOR, BLACK,
                    0, EndFlameLeftPosition).convert()

EndFlameRight = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                    BOMB_SCALE_FACTOR, BLACK,
                    0, EndFlameRightPosition).convert()

MidFlame = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                    BOMB_SCALE_FACTOR, BLACK,
                    0, MidFlamePosition).convert()

FourWayFlame = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                    BOMB_SCALE_FACTOR, BLACK,
                    0, FourWayFlamePosition).convert()


BottomFlame = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                    BOMB_SCALE_FACTOR, BLACK,
                    0, BottomFlamePosition).convert()

TopFlame = getImage(sprite_sheet_image, TILESIZE, TILESIZE,
                    BOMB_SCALE_FACTOR, BLACK,
                    0, TopFlamePosition).convert()

