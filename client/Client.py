
import socket
import pygame
from pygame.locals import *
import math
import sys
import time
import struct
import threading
from threading import Lock, Event
import numpy as np

from Setup import *
from Spritesheet import *
import Physics
from Globals import *
import Globals
import Player
from Bomb import *

# Heartbeat to disconnect players

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 5000))

def checkNumClients():
    connStr = sock.recv(2)
    if connStr.decode() == 'NO':
        print('Limite de jogadores alcançado (4).')
        sock.close()
        pygame.quit()
        exit()

player_joined_event = Event()
player_updated_event = Event()

#lenState = sock.recv(4)
#state = sock.sendall(struct.pack('>I', len('STATE')) + b'STATE') or sock.recv(7)
#state_color = tuple(state)
#print(state_color)
#sock.sendall(struct.pack('>I', len('STATE2')) + b'STATE2')
#
#lenState2 = sock.recv(4)
#state2 = struct.unpack('>HH', sock.recv(4))
#print(state2)
#rect_position = list(state2)

state_color = (0, 0, 255)
rect_position = (100, 100)

pygame.display.set_caption("Game")

# TODO: make server generate ID 
# and look for duplicates 
ID = np.random.choice(range(30000))

playerDict = {}

def updateState2():
    global rect_position
    pos = pygame.mouse.get_pos()
    rect_position = list(pos)
    data = b'UPDATE' + struct.pack('>HH', *pos)
    sock.sendall(struct.pack('>I', len(data)) + data)

def parseProtocolMSG(msg):
    global rect_position, playerDict

    if msg.startswith(b'NEWP'):
        with rect_position_lock:
            rect_position = list(struct.unpack('>HH', msg[4:]))

    elif msg.startswith(b'PLAYER UPDATED'):

       R, G, B, height, width, x, y, incomingID = list(struct.
                                                    unpack('>3B2H2iH',
                                                    msg[14:]))

       player = Player.Sprite((R, G, B), height, width)
       player.rect.x = x
       player.rect.y = y

       with players_lock:
           playerDict[incomingID] = player
           player_updated_event.set()
            
    elif msg.startswith(b'PLAYER JOINED'):

        global ID

        playersConnected = struct.unpack('>H', msg[13:15])[0]

        for i in range(playersConnected):

            # 17 Bytes { (R, G, B), 2 shorts, 2 ints and 1 more short }
            R, G, B, height, width, x, y, incomingID = list(struct.
                                             unpack_from('>3B2H2iH',
                                                     msg[15:], i * 17))

            player = Player.Sprite((R, G, B), height, width)
            player.rect.x = x
            player.rect.y = y

            with players_lock:

                if incomingID not in playerDict:
                    playerDict[incomingID] = player

                    if ID == incomingID:
                        Player.playerCar = player

                    player_joined_event.set()

    elif msg.startswith(b'PLAYER DISC'):
        # unpack always returns a tuple IMPORTANT TO REMEMBER
        disconnectedID = struct.unpack('>H', msg[11:])[0]
        with players_lock:
            del playerDict[disconnectedID]

    elif msg.startswith(b'TOO MANY CONNECTIONS'):
        nmClients = struct.unpack('>I', msg[20:])[0]
        print(f'Too many clients on the server : {nmClients}')

    elif msg.startswith(b'BOMB PLACED'):
        posX, posY, time = struct.unpack('>2iI', msg[11:])
        bomb = Bomb(posX, posY, time)
        bomb.animate()

def recv_updates():
    recv_buffer = b""

    while True:
        try:
            data = sock.recv(2048)

            if not data:
               break

            recv_buffer += data

            while len(recv_buffer) >= 4:
                msg_len = struct.unpack('>I', recv_buffer[:4])[0]
                if len(recv_buffer) < 4 + msg_len:
                    break
                msg = recv_buffer[4:4 + msg_len]
                recv_buffer = recv_buffer[4 + msg_len:]
                parseProtocolMSG(msg)

        except Exception as e:
            print(f"Error: {e}")
            break


SURFACE_COLOR = (99, 99, 99)
COLOR = (255, 100, 98)

def quit():
    global recv_thread
    pygame.quit()
    recv_thread.join(timeout=0.1)
    sock.close()
    sys.exit()

def playerJoined():

    # Endianess, int 4 bytes ( little endian, big endian )
    data = b'PLAYER JOINED' + struct.pack('>3B2H2iH', *Player.color, 20, 30,
                                      Player.playerCar.rect.x,
                                      Player.playerCar.rect.y, ID)

    sock.sendall(struct.pack('>I', len(data)) + data)
    player_joined_event.wait(timeout=0.1)
    player_joined_event.clear()

def drawBoundingWalls(background):
    Physics.Walls.append(background.blit(sidewaysBrickWall, (0, 0)))
    
    # for i in range is non inclusive thats why
    # SCREEN_WIDTH - TILESIZE * TILES_SCALE_FACTOR
    # is not drawn as a topBrickWall
    for i in range(TILESIZE * TILES_SCALE_FACTOR, SCREEN_WIDTH -
                   TILESIZE * TILES_SCALE_FACTOR, TILESIZE * TILES_SCALE_FACTOR):
        Physics.Walls.append(background.blit(topBrickWall, (i, 0)))

    Physics.Walls.append(background.blit(sidewaysBrickWall,
                    (SCREEN_WIDTH - TILESIZE * TILES_SCALE_FACTOR, 0)))

    for i in range(TILESIZE * TILES_SCALE_FACTOR, SCREEN_HEIGHT,
                   TILESIZE * TILES_SCALE_FACTOR):
        Physics.Walls.append(background.blit(sidewaysBrickWall, (0, i)))

    for i in range(TILESIZE * TILES_SCALE_FACTOR, SCREEN_HEIGHT,
                   TILESIZE * TILES_SCALE_FACTOR):
        Physics.Walls.append(background.blit(sidewaysBrickWall, 
                        (SCREEN_WIDTH - TILESIZE * TILES_SCALE_FACTOR, i)))

    for i in range(0, SCREEN_WIDTH,
                   TILESIZE * TILES_SCALE_FACTOR):
        Physics.Walls.append(background.blit(topBrickWall, 
                        (i,SCREEN_HEIGHT - TILESIZE * TILES_SCALE_FACTOR)))

def drawInsideWalls(background):
    for i in range(2*TILESIZE * TILES_SCALE_FACTOR, SCREEN_WIDTH - 2*TILESIZE * TILES_SCALE_FACTOR, 2*TILESIZE * TILES_SCALE_FACTOR):
        for j in range(2*TILESIZE * TILES_SCALE_FACTOR, SCREEN_HEIGHT- 2*TILESIZE * TILES_SCALE_FACTOR, 2*TILESIZE * TILES_SCALE_FACTOR):
            Physics.Walls.append(background.blit(topBrickWall, (i, j)))

# def drawBoxes(background,):
def drawBoxes(background, x, y):
    box_rect = pygame.Rect(x * TILESIZE * TILES_SCALE_FACTOR,
                       y * TILESIZE * TILES_SCALE_FACTOR,
                       TILESIZE * TILES_SCALE_FACTOR, TILESIZE * TILES_SCALE_FACTOR)

    background_subsurface = background.subsurface(box_rect).copy()
    background.blit(WoodBox, box_rect)

    Physics.BoxesRects.append(box_rect.copy())
    Physics.BoxesSurfaces.append((background_subsurface, box_rect.copy()))

def drawBackground():
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for i in range(0, SCREEN_HEIGHT, TILESIZE * TILES_SCALE_FACTOR):
        for j in range(0, SCREEN_WIDTH, TILESIZE * TILES_SCALE_FACTOR):
            background.blit(grassTile, (j, i))

    drawBoundingWalls(background)
    drawInsideWalls(background)
    drawBoxes(background, 3, 4)
    drawBoxes(background, 1, 3)
    drawBoxes(background, 2, 3)
    drawBoxes(background, 3, 3)
    drawBoxes(background, 3, 2)
    drawBoxes(background, 3, 1)
    drawBoxes(background, 5, 6)
    background = background.convert()
    return background

def sendBombPlaced(posX, posY, time):
    packed = b'BOMB PLACED' + struct.pack('>2iI', posX, posY, time) 
    sock.sendall(struct.pack('>I', len(packed)) + packed)

if __name__ == "__main__":
    
    checkNumClients()
    Globals.background = drawBackground()
    recv_thread = threading.Thread(target=recv_updates, daemon=True)
    recv_thread.start()
    playerJoined()
    debug = False
    
    while True:
        Player.clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                updateState2()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    if Physics.lastPlacedBomb is not None:
                        collidingWithLastPlacedBomb = Player.playerCar \
                            .rect.colliderect(Physics.lastPlacedBomb.rect)

                    if (Physics.lastPlacedBomb is None or \
                       collidingWithLastPlacedBomb is None) and \
                       Globals.numberOfPlacedBombs < 2:

                        time = 2
                        bomb = Bomb(Player.playerCar.rect.x,
                                    Player.playerCar.rect.y, time)

                        Physics.justPlacedBomb = True
                        Physics.lastPlacedBomb = bomb

                        bomb.animate()
                        sendBombPlaced(Player.playerCar.rect.x,
                                       Player.playerCar.rect.y, time)
                if event.key == pygame.K_p:
                    debug = not debug

        #DISPLAY.blit(sidewaysBrickWall, (0, 0))
        #DISPLAY.blit(goblin1FrameArray[1], (TILESIZE * SCALE_FACTOR, 0))
        
        with players_lock:
            data = b'CHANGEPOS' + struct.pack('>H2i',  ID, Player.playerCar.rect.x,
                                            Player.playerCar.rect.y)

            sock.sendall(struct.pack('>I', len(data)) + data)
            #player_updated_event.wait(timeout=0.1)
            #player_updated_event.clear()


        DISPLAY.blit(Globals.background, (0, 0))
        bombsGroup.draw(DISPLAY)
        bombsGroup.update()

        explosionGroup.draw(DISPLAY)
        explosionGroup.update()
        

        #with rect_position_lock:
        #    pygame.draw.rect(DISPLAY, state_color,
        #                     (*rect_position, 50, 50))

        collided = pygame.sprite.spritecollideany(Player.playerCar, bombsGroup,
                                                  collided=None)

        indexofCollidedWall = Player.playerCar.rect.collidelist(Physics.Walls)
        indexofCollidedBox  = Player.playerCar.rect.collidelist(Physics.BoxesRects)

        if collided is None and indexofCollidedWall == -1 and indexofCollidedBox == -1:
            Physics.oldPos = Player.playerCar.rect.copy()
            Physics.justPlacedBomb = False
            Physics.lastPlacedBomb = None

        with players_lock:
            Player.playerCar.move()
            for p in playerDict.values():
                DISPLAY.blit(p.image, (p.rect.x - TILESIZE / 2,
                                       p.rect.y - TILESIZE))

                if debug:
                    pygame.draw.rect(DISPLAY, (0, 255, 0),
                                     (p.rect.x,
                                      p.rect.y, p.rect.width,
                                      p.rect.height), 3)

        Physics.collisionDetection(Physics.oldPos)

        pygame.display.update()

