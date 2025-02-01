import sys

import pygame

from GameProcess import Game
from init_pygame import fps, main_screen


class MainWindow:
    def __init__(self):
        self.game = Game()

    def show_intro(self):
        image = pygame.image.load('assets/images/aviation/intro.png')
        main_screen.blit(image, (0, 0))
        pygame.display.flip()

        intro_sound = pygame.mixer.Sound('assets/audio/intro.ogg')
        intro_sound.play()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro_sound.stop()
                    break
                if event.key == pygame.K_i:
                    self.show_instructions()

    def show_instructions(self):
        pass

    def run(self):
        self.show_intro()
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                self.game.update(event)
                if event.type == pygame.QUIT:
                    self.terminate()
            self.game.update()
            pygame.display.flip()
            clock.tick(fps)

    def terminate(self):
        pygame.quit()
        sys.exit()
