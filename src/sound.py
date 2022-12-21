import pygame


class SoundManager:
    def __init__(self):
        self.sounds = {

            'launch': pygame.mixer.Sound("../sons/One_Piece_ .mp3"
                                         ),
            'hxh': pygame.mixer.Sound("../sons/HXH.mp3"),

            'sanji': pygame.mixer.Sound("../sons/sanji.mp3")

        }

    def play(self, name):
        self.sounds[name].play(loops=500)
