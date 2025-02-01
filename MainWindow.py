import sys

import pygame

from Sprites import SpriteGroups, soundpad
from Wave import EnemyWave
from init_pygame import width, height, fps, main_screen
from  GameProcess import Game
from GameProcess import Game
from init_pygame import fps, main_screen


class MainWindow:
    def __init__(self):
        self.game = Game()

    def show_intro(self):
        image = pygame.image.load('assets/images/aviation/intro.png')
        main_screen.blit(image, (0, 0))
        pygame.display.flip()

        soundpad.play(0)

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    soundpad.stop(0)
                    break
                if event.key == pygame.K_i:
                    self.show_instructions()

    def show_instructions(self):
        pass

    def run(self):
        self.show_intro()

        clock = pygame.time.Clock()

        wave = EnemyWave()

        while True:
            main_screen.fill((0, 0, 0))
            for event in pygame.event.get():
                SpriteGroups.main_group.update(event)
                self.game.update()
                wave.update(event)
                if event.type == pygame.QUIT:
                    self.terminate()
            SpriteGroups.main_group.update()
            wave.update()
            self.game.update()
            SpriteGroups.main_group.draw(main_screen)
            pygame.display.flip()
            clock.tick(fps)

    def terminate(self):
        pygame.quit()
        sys.exit()
