import pygame


class Soundpad:
    intro_sound = pygame.mixer.Sound('assets/audio/intro.ogg')
    outro_sound = pygame.mixer.Sound('assets/audio/outro.ogg')

    shot_sound = pygame.mixer.Sound('assets/audio/shot.ogg')
    crash_sound = pygame.mixer.Sound('assets/audio/crash.ogg')

    def __init__(self):
        self.all_sounds = [self.intro_sound, self.outro_sound, self.crash_sound, self.shot_sound]

    def play(self, sound):
        pygame.mixer.Sound.play(self.all_sounds[sound])

    def stop(self, sound):
        pygame.mixer.Sound.stop(self.all_sounds[sound])



soundpad = Soundpad()