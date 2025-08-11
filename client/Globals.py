
from threading import Lock, Event
import struct

#672
SCREEN_WIDTH = 624
SCREEN_HEIGHT = 624

SERVER_IP = 'localhost'
rect_position_lock = Lock()
players_lock = Lock()
background = None
numberOfPlacedBombs = 0
thisClientSocket = None
thisListeningThread = None
player_joined_event = Event()
player_updated_event = Event()

connectedPlayers     = [ [False, -1, 1], [False, -1, 2], [False, -1, 3],
                         [False, -1, 4] ] 

def getPosition(ID):
    for i in range(4):
        player = connectedPlayers[i]
        if(player[1] == ID):
            return player[2]

def getLobbyData():
    thisClientSocket.sendall(struct.pack('>I', len(b'LOBBY DATA')) + b'LOBBY DATA')

def addPlayer(ID):
    for i in range(4):
        player = connectedPlayers[i]
        if(player[1] == -1):
            player[0] = True
            player[1] = ID
            break

def removePlayer(ID):
    for i in range(4):
        player = connectedPlayers[i]
        if(player[1] == ID):
            player[0] = False
            player[1] = -1
            break



