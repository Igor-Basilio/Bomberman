
import socket
import pygame
from pygame.locals import *
import sys
import time
import struct
import threading
from threading import Lock, Event
import numpy as np

from Setup import *
from Spritesheet import *

# Heartbeat to disconnect players

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.0.212', 5000))

rect_position_lock = Lock()
players_lock = Lock()

def checkNumClients():
    connStr = sock.recv(2)
    print(connStr)
    if connStr == 'NO':
        print('TOO MANY CONNECTIONS')
        sock.close()
        pygame.quit()
        exit()
    else:
        print('OK')


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

       player = Sprite((R, G, B), height, width)
       player.rect.x = x
       player.rect.y = y

       with players_lock:
           playerDict[incomingID] = player
           player_updated_event.set()
            
    elif msg.startswith(b'PLAYER JOINED'):

        global ID, playerCar

        playersConnected = struct.unpack('>H', msg[13:15])[0]

        for i in range(playersConnected):

            # 17 Bytes { (R, G, B), 2 shorts, 2 ints and 1 more short }
            R, G, B, height, width, x, y, incomingID = list(struct.
                                             unpack_from('>3B2H2iH',
                                                     msg[15:], i * 17))

            player = Sprite((R, G, B), height, width)
            player.rect.x = x
            player.rect.y = y

            with players_lock:

                if incomingID not in playerDict:
                    playerDict[incomingID] = player

                    if ID == incomingID:
                        playerCar = player

                    player_joined_event.set()

    elif msg.startswith(b'PLAYER DISC'):
        # unpack always returns a tuple IMPORTANT TO REMEMBER
        disconnectedID = struct.unpack('>H', msg[11:])[0]
        with players_lock:
            del playerDict[disconnectedID]

    elif msg.startswith(b'TOO MANY CONNECTIONS'):
        nmClients = struct.unpack('>I', msg[20:])[0]
        print(f'Too many clients on the server : {nmClients}')

def recv_updates():
    recv_buffer = b""

    while True:
        try:
            data = sock.recv(2048)

            if not data:
                continue

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


class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()

        self.color = color
        self.image = goblin1FrameArray[1]
        self.rect = self.image.get_rect()

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
playerCar.rect.x = np.random.choice(range(800 - 30))
playerCar.rect.y = np.random.choice(range(600 - 20))


def quit():
    global recv_thread
    pygame.quit()
    recv_thread.join(timeout=0.1)
    sock.close()
    sys.exit()

def playerJoined():
    global playerCar
    data = b'PLAYER JOINED' + struct.pack('>3B2H2iH', *color, 20, 30,
                                      playerCar.rect.x, playerCar.rect.y, ID)

    sock.sendall(struct.pack('>I', len(data)) + data)
    player_joined_event.wait(timeout=0.1)
    player_joined_event.clear()


def drawGrass():
    background = pygame.Surface((720, 576))
    for i in range(0, 576, TILESIZE):
        for j in range(0, 720, TILESIZE):
            background.blit(grassTile, (j, i))

    
    background = background.convert()
    return background


if __name__ == "__main__":

    #checkNumClients()
    background = drawGrass()
    recv_thread = threading.Thread(target=recv_updates, daemon=True)
    recv_thread.start()
    playerJoined()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                quit()
            elif event.type == pygame.MOUSEBUTTONUP:
                updateState2()

        #DISPLAY.blit(sidewaysBrickWall, (0, 0))
        #DISPLAY.blit(goblin1FrameArray[1], (TILESIZE * SCALE_FACTOR, 0))
        
        with players_lock:
            data = b'CHANGEPOS' + struct.pack('>H2i',  ID, playerCar.rect.x,
                                            playerCar.rect.y)

            sock.sendall(struct.pack('>I', len(data)) + data)
            #player_updated_event.wait(timeout=0.1)
            #player_updated_event.clear()

        DISPLAY.blit(background, (0, 0))
        with rect_position_lock:
            pygame.draw.rect(DISPLAY, state_color,
                             (*rect_position, 50, 50))

        with players_lock:
            playerCar.move()
            for p in playerDict.values():
                DISPLAY.blit(p.image, p.rect)

        pygame.display.update()

