
import pygame
from Button import *
import Globals
import threading
import Client
from Client import *
import time

pygame.init()

screen = pygame.display.set_mode((Globals.SCREEN_WIDTH, Globals.SCREEN_HEIGHT))
screen.fill((125, 125, 125))

class MenuPrincipal:

    def __init__(self, screen):
        self.start_button_img = pygame.image.load("assets/start_button.png")
        self.command_help_button_img = pygame.image.load(
                                          "assets/command_help_button.png")
        self.quit_button_img = pygame.image.load("assets/quit_button.png")

        self.screen = screen

        self.start_button = Button((Globals.SCREEN_WIDTH -
                                   self.start_button_img.get_width()) / 2,
                              Globals.SCREEN_HEIGHT / 2.5, 
                                   self.start_button_img, 1)

        self.command_help_button = Button((Globals.SCREEN_WIDTH -
                                   self.command_help_button_img.get_width())
                                          / 2,
                               Globals.SCREEN_HEIGHT / 2,
                                          self.command_help_button_img, 1)

        self.quit_button = Button((Globals.SCREEN_WIDTH -
                                   self.quit_button_img.get_width()) / 2,
                               Globals.SCREEN_HEIGHT / 1.66,
                                  self.quit_button_img, 1)

    def mostrarMenuPrincipal(self):
        menuPrincipal.screen.fill(menu_background)

        menuPrincipal.start_button.draw(menuPrincipal.screen)
        menuPrincipal.command_help_button.draw(menuPrincipal.screen)
        menuPrincipal.quit_button.draw(menuPrincipal.screen)

        return "menu_principal"

class MenuGameMode:

    def __init__(self, screen):
        self.online_session_button_img = pygame.image.load(
                                       "assets/online_session_button.png")
        self.back_button_img = pygame.image.load("assets/back_button.png")

        self.screen = screen

        self.lan_button = Button((Globals.SCREEN_WIDTH -
                                  self.online_session_button_img.get_width()) 
                                    / 2,
                            Globals.SCREEN_HEIGHT / 2,
                                            self.online_session_button_img, 1)

        self.back_button = Button((Globals.SCREEN_WIDTH -
                                  self.back_button_img.get_width()) / 2,
                            Globals.SCREEN_HEIGHT / 1.66,
                                  self.back_button_img, 1)


    def mostrarMenuGameMode(self):
        menuGameMode.screen.fill(menu_background)

        menuGameMode.lan_button.draw(menuGameMode.screen)
        #menuGameMode.online_session_button.draw(menuGameMode.screen)
        menuGameMode.back_button.draw(menuGameMode.screen)

        return "menu_game_mode"

class MenuCommandHelp:

    def __init__(self, screen):
        self.help_panel_img = pygame.image.load("assets/help_panel.png")
        self.back_button_img = pygame.image.load("assets/back_button.png")

        self.screen = screen

        self.help_panel = Button((Globals.SCREEN_WIDTH -
                                 self.help_panel_img.get_width()) / 2,
                           Globals.SCREEN_HEIGHT / 6,
                                 self.help_panel_img, 1)

        self.back_button = Button((Globals.SCREEN_WIDTH -
                                 self.back_button_img.get_width()) / 2,
                           Globals.SCREEN_HEIGHT / 1.20,
                                  self.back_button_img, 1)

    def mostrarMenuDeComandos(self):
        menuCommandHelp.screen.fill(menu_background)

        menuCommandHelp.help_panel.draw(menuCommandHelp.screen)
        menuCommandHelp.back_button.draw(menuCommandHelp.screen)

        return "menu_command_help"

class MenuLobby:

    def __init__(self, screen):

        self.lobby_img = pygame.image.load("assets/lobby.png")
        self.player_1_img = pygame.image.load("assets/player_1.png")
        self.player_2_img = pygame.image.load("assets/player_2.png")
        self.player_3_img = pygame.image.load("assets/player_3.png")
        self.player_4_img = pygame.image.load("assets/player_4.png")
        self.back_button_img = pygame.image.load("assets/back_button.png")
        self.begin_button_img = pygame.image.load("assets/begin_button.png")

        self.screen = screen
        
        self.lobby = Button((Globals.SCREEN_WIDTH -
                             self.lobby_img.get_width()) / 2,
                            Globals.SCREEN_HEIGHT / 14.5, self.lobby_img, 1)

        self.player_1_pos = ((Globals.SCREEN_WIDTH -
                            self.player_1_img.get_width()) / 2 -
                            Globals.SCREEN_WIDTH / 3,
                            Globals.SCREEN_HEIGHT / 3.4)

        self.player_1 = Button(self.player_1_pos[0], self.player_1_pos[1],
                               self.player_1_img, 1)


        self.player_2_pos = ((Globals.SCREEN_WIDTH -
                            self.player_2_img.get_width()) / 2 -
                            Globals.SCREEN_WIDTH / 3,
                            Globals.SCREEN_HEIGHT / 2.4)

        self.player_2 = Button(self.player_2_pos[0],
                               self.player_2_pos[1], self.player_2_img, 1)


        self.player_3_pos = ((Globals.SCREEN_WIDTH -
                            self.player_3_img.get_width()) / 2 -
                            Globals.SCREEN_WIDTH / 3,
                            Globals.SCREEN_HEIGHT / 1.86)

        self.player_3 = Button(self.player_3_pos[0], 
                               self.player_3_pos[1], self.player_3_img, 1)

        self.player_4_pos = ((Globals.SCREEN_WIDTH -
                            self.player_4_img.get_width()) / 2 -
                            Globals.SCREEN_WIDTH / 3,
                            Globals.SCREEN_HEIGHT / 1.52)

        self.player_4 = Button(self.player_4_pos[0],
                               self.player_4_pos[1], self.player_4_img, 1)

        self.back_button = Button(Globals.SCREEN_WIDTH / 8,
                            Globals.SCREEN_HEIGHT / 1.15,
                                  self.back_button_img, 1)

        self.begin_button = Button(Globals.SCREEN_WIDTH / 2,
                            Globals.SCREEN_HEIGHT / 1.15,
                                   self.begin_button_img, 1)

        self.player1ConnectedPos = (self.player_1_pos[0] + self
                                    .player_1_img.get_width() + 7,
                                    self.player_1_pos[1] + 7)

        self.player2ConnectedPos = (self.player_2_pos[0] + self
                                    .player_2_img.get_width() + 7,
                                    self.player_2_pos[1] + 7)

        self.player3ConnectedPos = (self.player_3_pos[0] + self
                                    .player_3_img.get_width() + 7,
                                    self.player_3_pos[1] + 7)

        self.player4ConnectedPos = (self.player_4_pos[0] + self
                                    .player_4_img.get_width() + 7,
                                    self.player_4_pos[1] + 7)

        self.playerPositions = (self.player1ConnectedPos, 
                                self.player2ConnectedPos,
                                self.player3ConnectedPos,
                                self.player4ConnectedPos)

    def mostrarMenuLobby(self):
        menuLobby.screen.fill(menu_background)

        menuLobby.lobby.draw(menuLobby.screen)
        menuLobby.player_1.draw(menuLobby.screen)

        GREEN = (0, 255, 0)
        RED   = (255, 0, 0)
    
        for p in Globals.connectedPlayers:
           if(p[0] == True):
               pygame.draw.rect(screen, GREEN, (self.playerPositions[p[2] - 1][0], 
                                self.playerPositions[p[2] - 1][1], 30, 30))
           else:
               pygame.draw.rect(screen, RED, (self.playerPositions[p[2] - 1][0], 
                                self.playerPositions[p[2] - 1][1], 30, 30))

        if(getPosition(ID) is not None):
            pygame.draw.rect(screen,
                             BLACK, 
                            (self.playerPositions[getPosition(Client.ID) - 1][0], 
                            self.playerPositions[getPosition(Client.ID) - 1][1],
                             30, 30), 5)
            
        menuLobby.player_2.draw(menuLobby.screen)


        menuLobby.player_3.draw(menuLobby.screen)


        menuLobby.player_4.draw(menuLobby.screen)


        menuLobby.back_button.draw(menuLobby.screen)
        menuLobby.begin_button.draw(menuLobby.screen)

        return "menu_lobby"
    
current_screen  = "menu_principal"
menu_background = (125, 125, 125)

menuPrincipal   = MenuPrincipal(screen)
menuGameMode    = MenuGameMode(screen)
menuCommandHelp = MenuCommandHelp(screen)
menuLobby       = MenuLobby(screen)

menuPrincipal.mostrarMenuPrincipal()

clock = pygame.time.Clock()

if __name__ == "__main__":

    Globals.background = Client.drawBackground()
    firstTime = True

    while True:

        clock.tick(60)
        events = pygame.event.get()

        if current_screen == "menu_principal":

            if menuPrincipal.start_button.draw(menuPrincipal.screen):
                current_screen = menuGameMode.mostrarMenuGameMode()

            elif menuPrincipal.command_help_button.draw(menuPrincipal.screen):
                current_screen = menuCommandHelp.mostrarMenuDeComandos()

            elif menuPrincipal.quit_button.draw(menuPrincipal.screen):
                pygame.quit()
                exit()

        if current_screen == "menu_game_mode":
            
            if menuGameMode.lan_button.draw(menuGameMode.screen):

                Globals.thisClientSocket = Client.connectToServer()

                Client.checkNumClients(Globals.thisClientSocket)

                if firstTime:
                    Globals.thisListeningThread = threading.Thread(
                            target=Client.recv_updates,
                            args=(Globals.thisClientSocket, 
                                  ))
                    firstTime = False
                    Globals.thisListeningThread.start()

                current_screen = menuLobby.mostrarMenuLobby()
                Client.playerJoined(Globals.thisClientSocket)
                
                connectedPlayers = getLobbyData() 

            elif menuGameMode.back_button.draw(menuGameMode.screen):
                current_screen = menuPrincipal.mostrarMenuPrincipal()

        if current_screen == "menu_command_help":

            if menuCommandHelp.back_button.draw(menuCommandHelp.screen):
                current_screen = menuPrincipal.mostrarMenuPrincipal()

        if current_screen == "menu_lobby":

            if menuLobby.back_button.draw(menuLobby.screen):

                Client.disconnectFromServer(Globals.thisClientSocket)
                Globals.thisClientSocket = None
                current_screen = menuGameMode.mostrarMenuGameMode()
                Globals.thisListeningThread.join(timeout=0.1)
                Globals.thisListeningThread = None
                del Client.playerDict[Client.ID]
                firstTime = True
                Globals.removePlayer(Client.ID)
             
            elif menuLobby.begin_button.draw(menuLobby.screen):
                current_screen = "game"

            if current_screen == "menu_lobby":
                menuLobby.mostrarMenuLobby()

        if current_screen == "game" and Globals.thisListeningThread is not None:
            Client.drawGame(events, Globals.thisClientSocket,
                            Globals.thisListeningThread)

        for event in events:

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
    
