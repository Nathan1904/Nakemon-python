import pygame

from player import Player
from dialog import DialogBox
from map import MapManager
from sound import SoundManager


class Game:
    def __init__(self):

        # définir si notre jeu à commencer ou non
        self.is_playing = False

        # Creer la fenêtre du jeu

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Nakemon-Aventure")

        # importer la bannière

        # générer un joueur

        self.player = Player()

        self.map_manager = MapManager(self.screen, self.player)

        self.dialog_box = DialogBox()

        # gérer les sons

        self.sound_manager = SoundManager()

        self.banner = pygame.image.load('../background/banner.png')
        self.banner = pygame.transform.scale(self.banner, (800, 600))
        self.banner_rect = self.banner.get_rect()
        # importer le boutton pour lancer la partie
        self.play_button = pygame.image.load('../background/start.png')
        self.play_button = pygame.transform.scale(self.play_button, (400, 150))
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = self.screen.get_width() / 4.2
        self.play_button_rect.y = self.screen.get_height() / 2
        # creer un menu pause
        self.pause_btn = pygame.image.load('../background/Pause-Button.png')
        self.pause_btn = pygame.transform.scale(self.pause_btn, (40, 40))
        self.pause_btn_rect = self.pause_btn.get_rect()
        self.pause_btn_rect.x = self.screen.get_width() / 2.1
        self.pause_btn_rect.y = 1
        self.x_souris, self.y_souris = 0, 0
        self.etat = False
        self.pause_image = pygame.image.load('../background/pauseimg.png')
        self.pause_image = pygame.transform.scale(self.pause_image, (500, 500))
        self.pause_image_rect = self.pause_image.get_rect()
        self.pause_image_rect.x = self.screen.get_width() / 5.4
        self.pause_image_rect.y = 1
        self.play_button2 = pygame.image.load ("../background/play_now.png")
        self.play_button2 = pygame.transform.scale(self.play_button2,(135,60))
        self.play_button2_rect = self.play_button2.get_rect()
        self.play_button2_rect.x = self.screen.get_width()/2.4111
        self.play_button2_rect.y =self.screen.get_height()/2.4
        # self.pause_btn_rect = pygame.Rect(542, 501, 84, 82)
        # self.image_btn = self.pause_btn.subsurface(self.pause_btn_rect)
        # self.image_btn = pygame.transform.scale(self.image_btn, (50, 50))
        # boucle qui va maintenir la fenêtre ouverte

    def handleinput(self):

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()

        elif pressed[pygame.K_LEFT]:
            self.player.move_left()

        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()

    def update(self):
        self.map_manager.upadate()

    def menu_pause(self):
        if self.etat:
            # affichage du menu de pause
            self.screen.blit(self.pause_image, self.pause_image_rect)
            self.screen.blit(self.play_button2,self.play_button2_rect)
        else:
            pass

    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.handleinput()
            self.update()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            self.menu_pause()
            if self.is_playing:
                # self.sound_manager.play('launch')
                self.screen
                self.screen.blit(self.pause_btn, self.pause_btn_rect)
            else:
                # ajouter lécran de bienvenue
                self.screen.blit(self.banner, (0, 0))
                self.screen.blit(self.play_button, self.play_button_rect)

            # vérifier si le jeu à commencer
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.map_manager.check_npc_collisions(self.dialog_box)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # vérification pour savoir si la souris est en collison avec le boutton jouer
                    if self.play_button_rect.collidepoint(event.pos):
                        self.sound_manager.play('launch')
                        # mettre le jeu en mode lancer
                        self.is_playing = True
                    if self.pause_btn_rect.collidepoint(event.pos):
                        # self.x_souris, self.y_souris = pygame.mouse.get_pos()
                        # print(self.x_souris, self.y_souris)
                        self.etat = True
                    if self.play_button2_rect.collidepoint(event.pos):
                        self.etat= False

            clock.tick(60)

        pygame.quit()
