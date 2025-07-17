
import pygame
from Spritesheet import *
import Physics
import Globals

FPS = 60

REAL_TILESIZE = TILESIZE * TILES_SCALE_FACTOR

class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, timeUntilExplosion):
        super().__init__()

        Globals.numberOfPlacedBombs += 1
        self.is_animating = False
        self.sprites = BombFrameArray
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()

        self.rect.center = (round(pos_x / REAL_TILESIZE) * REAL_TILESIZE 
                            + REAL_TILESIZE // 2,
                    round(pos_y / REAL_TILESIZE) * REAL_TILESIZE +
                            REAL_TILESIZE // 2)

        dt = pygame.time.Clock().tick(FPS) / 1000
        self.animationSpeed = (len(self.sprites) / timeUntilExplosion) * dt

        bombsGroup.add(self)

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating:
            self.current_sprite += self.animationSpeed

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
                BombExplosion(self.rect.center[0], self.rect.center[1], 2)
                bombsGroup.remove(self)
                self.kill()
                return

            self.image = self.sprites[int(self.current_sprite)]

class BombExplosion(pygame.sprite.Sprite):

    # Peeks and returns True if there is no collision
    # on the direction peeked, unless the direction
    # is different from {"left", "right", "down", "up"}
    # which then it always returns False.
    def peekDirection(self, pos_x, pos_y, direction, colliders):
        peekRect = pygame.Rect((0,0), (0,0))
        peekRect.width = TILESIZE
        peekRect.height = TILESIZE
        pos = (0, 0)

        match direction:
            case "left":
                pos = (pos_x - TILESIZE * TILES_SCALE_FACTOR,
                           pos_y)
            case "right":
                pos = (pos_x + TILESIZE * TILES_SCALE_FACTOR,
                           pos_y)
            case "down":
                pos = (pos_x,
                           pos_y + TILESIZE * TILES_SCALE_FACTOR)
            case "up":
                pos = (pos_x,
                           pos_y - TILESIZE * TILES_SCALE_FACTOR)
            case _:
                return False

        peekRect.center = pos

        # This tests on every possible collision that exists 
        # ( very bad but since the game is small its ok )
        indexOfCollidedWall = peekRect.collidelist(colliders)
        return indexOfCollidedWall == -1

    def peekAndReturnIndex(self, pos_x, pos_y, direction, colliders):
        peekRect = pygame.Rect((0,0), (0,0))
        peekRect.width = TILESIZE
        peekRect.height = TILESIZE
        pos = (0, 0)

        match direction:
            case "left":
                pos = (pos_x - TILESIZE * TILES_SCALE_FACTOR,
                           pos_y)
            case "right":
                pos = (pos_x + TILESIZE * TILES_SCALE_FACTOR,
                           pos_y)
            case "down":
                pos = (pos_x,
                           pos_y + TILESIZE * TILES_SCALE_FACTOR)
            case "up":
                pos = (pos_x,
                           pos_y - TILESIZE * TILES_SCALE_FACTOR)
            case _:
                return False

        peekRect.center = pos
        # This tests on every possible collision that exists 
        # ( very bad but since the game is small its ok )
        return peekRect.collidelist(colliders)

    def __init__(self, pos_x, pos_y, explosionTime):
        super().__init__()
        
        surface = pygame.Surface((3*TILESIZE,
                                  3*TILESIZE)).convert_alpha()

        surface.blit(sprite_sheet_image,
                     (1*TILESIZE, 1*TILESIZE),
                     (FourWayFlamePosition[0], FourWayFlamePosition[1],
                      TILESIZE, TILESIZE)) 

        
        box = self.peekAndReturnIndex(pos_x, pos_y, "left", Physics.BoxesRects)
        if self.peekDirection(pos_x, pos_y, "left", Physics.Walls) and box == -1:
            surface.blit(sprite_sheet_image,
                         (0, 1*TILESIZE), (EndFlameLeftPosition[0],
                                           EndFlameLeftPosition[1],
                                           TILESIZE, TILESIZE))
        elif box != -1:
            surface.blit(sprite_sheet_image,
                         (0, 1*TILESIZE), (EndFlameLeftPosition[0],
                                           EndFlameLeftPosition[1],
                                           TILESIZE, TILESIZE))

            Globals.background.blit(Physics.BoxesSurfaces[box][0],
                                    Physics.BoxesSurfaces[box][1])
            del Physics.BoxesRects[box]
            del Physics.BoxesSurfaces[box]


        box = self.peekAndReturnIndex(pos_x, pos_y, "right", Physics.BoxesRects)
        if self.peekDirection(pos_x, pos_y, "right", Physics.Walls) and box == -1:
            surface.blit(sprite_sheet_image,
                         (2*TILESIZE, 1*TILESIZE), (EndFlameRightPosition[0],
                                                    EndFlameRightPosition[1],
                                           TILESIZE,
                                           TILESIZE))
        elif box != -1:
            surface.blit(sprite_sheet_image,
                         (2*TILESIZE, 1*TILESIZE), (EndFlameRightPosition[0],
                                                    EndFlameRightPosition[1],
                                           TILESIZE,
                                           TILESIZE))

            Globals.background.blit(Physics.BoxesSurfaces[box][0],
                                    Physics.BoxesSurfaces[box][1])
            del Physics.BoxesRects[box]
            del Physics.BoxesSurfaces[box]


        box = self.peekAndReturnIndex(pos_x, pos_y, "up", Physics.BoxesRects)
        if self.peekDirection(pos_x, pos_y, "up", Physics.Walls) and box == -1:
            surface.blit(sprite_sheet_image,
                         (TILESIZE, 0), (TopFlamePosition[0],
                                         TopFlamePosition[1],
                                           TILESIZE,
                                           TILESIZE))
        elif box != -1:
            surface.blit(sprite_sheet_image,
                         (TILESIZE, 0), (TopFlamePosition[0],
                                         TopFlamePosition[1],
                                           TILESIZE,
                                           TILESIZE))

            Globals.background.blit(Physics.BoxesSurfaces[box][0],
                                    Physics.BoxesSurfaces[box][1])
            del Physics.BoxesRects[box]
            del Physics.BoxesSurfaces[box]

        box = self.peekAndReturnIndex(pos_x, pos_y, "down", Physics.BoxesRects)
        if self.peekDirection(pos_x, pos_y, "down", Physics.Walls) and box == -1:
            surface.blit(sprite_sheet_image,
                         (TILESIZE, 2 * TILESIZE), (BottomFlamePosition[0],
                                                    BottomFlamePosition[1],
                                                    TILESIZE,
                                                    TILESIZE))
        elif box != -1:
            surface.blit(sprite_sheet_image,
                         (TILESIZE, 2 * TILESIZE), (BottomFlamePosition[0],
                                                    BottomFlamePosition[1],
                                                    TILESIZE,
                                                    TILESIZE))

            Globals.background.blit(Physics.BoxesSurfaces[box][0],
                                    Physics.BoxesSurfaces[box][1])
            del Physics.BoxesRects[box]
            del Physics.BoxesSurfaces[box]
        else:
            surface.blit(sprite_sheet_image,
                         (TILESIZE, 2 * TILESIZE), (BottomFlamePosition[0],
                                                    BottomFlamePosition[1],
                                                    TILESIZE,
                                                    TILESIZE / 3))
            

        surface = pygame.transform.scale(surface, (3 * TILESIZE * TILES_SCALE_FACTOR,
                                                   3 * TILESIZE * TILES_SCALE_FACTOR))
        surface.set_colorkey(BLACK)

        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.center = (pos_x,
                            pos_y)

        explosionGroup.add(self)
        self.startTime = pygame.time.get_ticks()
        self.time = self.startTime
        self.explosionTime = explosionTime

    def update(self):
        self.time = (pygame.time.get_ticks() - self.startTime) / 1000
        if self.time > self.explosionTime:
            explosionGroup.remove(self)
            Globals.numberOfPlacedBombs -= 1
            self.kill()
            return


bombsGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()

