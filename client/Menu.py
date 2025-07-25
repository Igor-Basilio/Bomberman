import pygame
from Button import *
from Globals import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((125, 125, 125))

class MenuPrincipal:

    def __init__(self, screen):
        self.start_button_img = pygame.image.load("start_button.png")
        self.command_help_button_img = pygame.image.load("command_help_button.png")
        self.quit_button_img = pygame.image.load("quit_button.png")

        self.screen = screen

        self.start_button = Button((SCREEN_WIDTH - self.start_button_img.get_width()) / 2, SCREEN_HEIGHT / 2.5, self.start_button_img, 1)
        self.command_help_button = Button((SCREEN_WIDTH - self.command_help_button_img.get_width())/ 2, SCREEN_HEIGHT / 2, self.command_help_button_img, 1)
        self.quit_button = Button((SCREEN_WIDTH - self.quit_button_img.get_width()) / 2, SCREEN_HEIGHT / 1.66, self.quit_button_img, 1)

class MenuGameMode:

    def __init__(self, screen):
        self.lan_button_img = pygame.image.load("lan_button.png")
        self.online_session_button_img = pygame.image.load("online_session_button.png")
        self.back_button_img = pygame.image.load("back_button.png")

        self.screen = screen

        self.lan_button = Button((SCREEN_WIDTH - self.lan_button_img.get_width()) / 2, SCREEN_HEIGHT / 2.5, self.lan_button_img, 1)
        self.online_session_button = Button((SCREEN_WIDTH - self.online_session_button_img.get_width()) / 2, SCREEN_HEIGHT / 2, self.online_session_button_img, 1)
        self.back_button = Button((SCREEN_WIDTH - self.back_button_img.get_width()) / 2, SCREEN_HEIGHT / 1.66, self.back_button_img, 1)

class MenuCommandHelp:

    def __init__(self, screen):
        self.help_panel_img = pygame.image.load("help_panel.png")
        self.back_button_img = pygame.image.load("back_button.png")

        self.screen = screen

        self.help_panel = Button((SCREEN_WIDTH - self.help_panel_img.get_width()) / 2, SCREEN_HEIGHT / 6, self.help_panel_img, 1)
        self.back_button = Button((SCREEN_WIDTH - self.back_button_img.get_width()) / 2, SCREEN_HEIGHT / 1.20, self.back_button_img, 1)

class MenuLobby:

    def __init__(self, screen):
        self.lobby_img = pygame.image.load("lobby.png")
        self.player_1_img = pygame.image.load("player_1.png")
        self.player_2_img = pygame.image.load("player_2.png")
        self.player_3_img = pygame.image.load("player_3.png")
        self.player_4_img = pygame.image.load("player_4.png")
        self.back_button_img = pygame.image.load("back_button.png")
        self.begin_button_img = pygame.image.load("begin_button.png")

        self.screen = screen

        self.lobby = Button((SCREEN_WIDTH - self.lobby_img.get_width()) / 2, SCREEN_HEIGHT / 14.5, self.lobby_img, 1)
        self.player_1 = Button((SCREEN_WIDTH - self.player_1_img.get_width()) / 2 - SCREEN_WIDTH / 3, SCREEN_HEIGHT / 3.4, self.player_1_img, 1)
        self.player_2 = Button((SCREEN_WIDTH - self.player_2_img.get_width()) / 2 - SCREEN_WIDTH / 3, SCREEN_HEIGHT / 2.4, self.player_2_img, 1)
        self.player_3 = Button((SCREEN_WIDTH - self.player_3_img.get_width()) / 2 - SCREEN_WIDTH / 3, SCREEN_HEIGHT / 1.86, self.player_3_img, 1)
        self.player_4 = Button((SCREEN_WIDTH - self.player_4_img.get_width()) / 2 - SCREEN_WIDTH / 3, SCREEN_HEIGHT / 1.52, self.player_4_img, 1)
        self.back_button = Button(SCREEN_WIDTH / 8, SCREEN_HEIGHT / 1.15, self.back_button_img, 1)
        self.begin_button = Button(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 1.15, self.begin_button_img, 1)

current_screen = "menu_principal"
menu_background = (125, 125, 125)

menuPrincipal = MenuPrincipal(screen)
menuGameMode = MenuGameMode(screen)
menuCommandHelp = MenuCommandHelp(screen)
menuLobby = MenuLobby(screen)

def mostrarMenuPrincipal():
    menuPrincipal.screen.fill(menu_background)

    menuPrincipal.start_button.draw(menuPrincipal.screen)
    menuPrincipal.command_help_button.draw(menuPrincipal.screen)
    menuPrincipal.quit_button.draw(menuPrincipal.screen)

    return "menu_principal"

def mostrarMenuGameMode():
    menuGameMode.screen.fill(menu_background)

    menuGameMode.lan_button.draw(menuGameMode.screen)
    menuGameMode.online_session_button.draw(menuGameMode.screen)
    menuGameMode.back_button.draw(menuGameMode.screen)

    return "menu_game_mode"

def mostrarMenuDeComandos():
    menuCommandHelp.screen.fill(menu_background)

    menuCommandHelp.help_panel.draw(menuCommandHelp.screen)
    menuCommandHelp.back_button.draw(menuCommandHelp.screen)

    return "menu_command_help"

def mostrarMenuLobby():
    menuLobby.screen.fill(menu_background)

    menuLobby.lobby.draw(menuLobby.screen)
    menuLobby.player_1.draw(menuLobby.screen)
    
    #   TODO MOSTRAR INFORMAÇÕES DO JOGADOR 1 (FAZER INTEGRAÇÃO)

    menuLobby.player_2.draw(menuLobby.screen)

    #   TODO MOSTRAR INFORMAÇÕES DO JOGADOR 2 (FAZER INTEGRAÇÃO)

    menuLobby.player_3.draw(menuLobby.screen)

    #   TODO MOSTRAR INFORMAÇÕES DO JOGADOR 3 (FAZER INTEGRAÇÃO)

    menuLobby.player_4.draw(menuLobby.screen)

    #   TODO MOSTRAR INFORMAÇÕES DO JOGADOR 4 (FAZER INTEGRAÇÃO)

    menuLobby.back_button.draw(menuLobby.screen)
    menuLobby.begin_button.draw(menuLobby.screen)

    return "menu_lobby"

mostrarMenuPrincipal()

clock = pygame.time.Clock()

while True:

    clock.tick(60)

    if current_screen == "menu_principal":

        if menuPrincipal.start_button.draw(menuPrincipal.screen):
            current_screen = mostrarMenuGameMode()

        elif menuPrincipal.command_help_button.draw(menuPrincipal.screen):
            current_screen = mostrarMenuDeComandos()

        elif menuPrincipal.quit_button.draw(menuPrincipal.screen):
            pygame.quit()
            exit()

    if current_screen == "menu_game_mode":
        
        if menuGameMode.lan_button.draw(menuGameMode.screen):
            current_screen = mostrarMenuLobby()

        elif menuGameMode.online_session_button.draw(menuGameMode.screen):
            current_screen = mostrarMenuLobby()

        elif menuGameMode.back_button.draw(menuGameMode.screen):
            current_screen = mostrarMenuPrincipal()

    if current_screen == "menu_command_help":

        if menuCommandHelp.back_button.draw(menuCommandHelp.screen):
            current_screen = mostrarMenuPrincipal()

    if current_screen == "menu_lobby":

        if menuLobby.back_button.draw(menuLobby.screen):
            #   TODO FAZER A INTEGRAÇÃO DE DESCONEXÃO DO JOGADOR CASO ELE CLIQUE NO BOTÃO DE VOLTAR
            current_screen = mostrarMenuGameMode()

        pass
        #   TODO elif menuLobby.begin_button.draw(menuLobby.screen) and >>>>>>>NUMERO_DE_JOGADORES == 4?<<<<<<<<:
        #   TODO FAZER A INTEGRAÇÃO DO INÍCIO DA PARTIDA QUANDO CLICAR NO BOTÃO COMEÇAR E QUANDO HOUVEREM 4 JOGADORES CONECTADOS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    
