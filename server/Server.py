import socketserver
import struct
import socket
import threading

state = (0, 0, 255)
state2 = (100, 100)

clients = []  # List of all active client sockets
clients_lock = threading.Lock()

players = {}

def resendPlayers():
    pass

def valueChanged():
    pass

recv_buffer = b""

def parseProtocolMSG(self, msg):

    if msg.startswith(b'UPDATE'):
        x, y = struct.unpack('>HH', msg[6:10])
        state2 = (x, y)
        packed_data = b'NEWP' + struct.pack('>HH', *state2)
        with clients_lock:
            for client in clients:
                if client != self.request:
                    try:
                        client.sendall(struct.pack('>I',
                                len(packed_data)) + packed_data)
                    except:
                        pass 

    elif msg.startswith(b'PLAYER JOINED'):
        global players


        R, G, B, height, width, x, y, ID = struct.unpack('>3B2H2iH', 
                                                         msg[13:])

        self._color = (R, G, B)
        self._height = height
        self._width = width

        #pos = (0, 0)
        #match len(clients):
        #    case 1:
        #        pos = (8, 8)
        #    case 2:
        #        pos = (8, 525)
        #    case 3:
        #        pos = (665, 8)
        #    case 4:
        #        pos = (665, 525)
        #    case _:
        #        pos = (x, y)

        pos = (50, 50)
        self._pos = pos
        self._ID = ID

        self._playerData = struct.pack('>3B2H2iH', R, G, B, height, width,
                                       pos[0], pos[1], ID)
        # maybe use [-2:] 
        # ( gotta to learn more about python indexing )
        #ID = struct.unpack('>H', data[28:30])[0]

        players[self._ID] = self._playerData

        data = b'PLAYER JOINED' + struct.pack('>H', len(players))

        for player in players.values():
            data += player

        with clients_lock:
            for client in clients:
                    try:
                        client.sendall(struct.pack('>I', len(data)) 
                                       + data)
                    except:
                        pass

    elif msg.startswith(b'CHANGEX'):
        ID, newX = struct.unpack('>Hi', msg[7:13]) 

        #R, G, B, height, width, x, y, playerID = struct.unpack('>3B2H2iH', 
        #                                                 players[ID])

        R, G, B = self._color
        x, y = self._pos
        self._pos = (newX, y)

        players[self._ID] = struct.pack('>3B2H2iH', R, G, B, self._height, 
                                  self._width,
                                  newX, y, self._ID )

        self._playerData = players[self._ID]

        packedData = b'PLAYER UPDATED' + self._playerData
        with clients_lock:
            for client in clients:
                    try:
                        client.sendall(struct.pack('>I', len(packedData)) 
                                       + packedData)
                    except:
                        pass

    elif msg.startswith(b'CHANGEY'):
        ID, newY = struct.unpack('>Hi', msg[7:13]) 

        #R, G, B, height, width, x, y, playerID = struct.unpack('>3B2H2iH', 
        #                                                 players[ID])

        R, G, B = self._color
        x, y = self._pos
        self._pos = (x, newY)

        players[self._ID] = struct.pack('>3B2H2iH',
                                  R, G, B, self._height,
                                  self._width,
                                  x, newY, self._ID )

        self._playerData = players[self._ID]

        packedData = b'PLAYER UPDATED' + self._playerData
        with clients_lock:
            for client in clients:
                    try:
                        client.sendall(struct.pack('>I', len(packedData)) 
                                       + packedData)
                    except:
                        pass

    elif msg.startswith(b'CHANGEPOS'):
        ID, newX, newY = struct.unpack('>H2i', msg[9:19]) 

        #R, G, B, height, width, x, y, playerID = struct.unpack('>3B2H2iH', 
        #                                                 players[ID])

        R, G, B = self._color
        self._pos = (newX, newY)

        players[self._ID] = struct.pack('>3B2H2iH',
                                  R, G, B, self._height,
                                  self._width,
                                  newX, newY, self._ID )

        self._playerData = players[self._ID]

        packedData = b'PLAYER UPDATED' + self._playerData
        with clients_lock:
            for client in clients:
                    try:
                        client.sendall(struct.pack('>I', len(packedData)) 
                                       + packedData)
                    except:
                        pass
    elif msg.startswith(b'BOMB PLACED'):
        lenMsg = struct.pack('>I', len(msg))
        with clients_lock:
            for client in clients:
                if client != self.request:
                    try:
                        client.sendall(lenMsg + msg)
                    except:
                        pass

    elif msg.strip() == b'STATE':
        self.request.send(struct.pack('>I', len(bytes(state))) 
                          + bytes(state))

    elif msg.strip() == b'STATE2':
        msg = struct.pack('>HH', *state2)
        self.request.send(struct.pack('>I', len(msg)) + msg)

class RequestHandler(socketserver.BaseRequestHandler):

    def setup(self):
        print(self.client_address, 'connected!')
        #self.request.send(('hi ' + str(self.client_address) + '\n').encode('utf-8'))

        if len(clients) >= 2:
            self.request.send(b'NO')
            return
        else:
            self.request.send(b'OK')
        
        with clients_lock:
            clients.append(self.request)
        self.request.settimeout(3.0)

    def handle(self):
        global state2, recv_buffer

        #if len(clients) >= 2:
        #    return

        while True:
            try:
                data = self.request.recv(2048)

                if not data:
                   break

                recv_buffer += data

                while len(recv_buffer) >= 4:
                    # I = 4 bytes sem sinal (unsigned int)
                    msg_len = struct.unpack('>I', recv_buffer[:4])[0]
                    if len(recv_buffer) < 4 + msg_len:
                        break
                    msg = recv_buffer[4:4 + msg_len]
                    recv_buffer = recv_buffer[4 + msg_len:]
                    parseProtocolMSG(self, msg)

            except ConnectionResetError:
                break

            except socket.timeout:
                print(f"Client {self.client_address} timed out.")
                break

    def finish(self):
        print(self.client_address, 'disconnected!')

        with clients_lock:
            if self.request in clients:
                clients.remove(self.request)

        if hasattr(self, '_ID') and self._ID in players:
            del players[self._ID]
            packed = b'PLAYER DISC' + struct.pack('>H', self._ID)

            with clients_lock:
                for client in clients:
                    if client != self.request:
                        try:
                            client.sendall(struct.pack('>I', len(packed)) + packed)
                        except:
                            pass

server = socketserver.ThreadingTCPServer(('localhost', 5000), RequestHandler)
server.daemon_threads = True
server.allow_reuse_address = True
server.serve_forever()

