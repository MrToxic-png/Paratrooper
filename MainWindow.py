import sys

import pygame

from Sprites import JetRight, Paratrooper, SpriteGroups, HelicopterLeft
from init_pygame import width, height, fps, main_screen


class MainWindow:
    def __init__(self):
        pass

    def show_intro(self):
        image = pygame.image.load('images/aviation/intro.png')
        main_screen.blit(image, (0, 0))
        pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                self.terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break
                if event.key == pygame.K_i:
                    self.show_instructions()

    def show_instructions(self):
        pass

    def run(self):
        self.show_intro()

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((width, height))

        JetRight()
        HelicopterLeft()
        Paratrooper()

        while True:
            main_screen.fill((0, 0, 0))
            for event in pygame.event.get():
                SpriteGroups.main_group.update(event)
                if event.type == pygame.QUIT:
                    self.terminate()
            SpriteGroups.main_group.update()
            SpriteGroups.main_group.draw(screen)
            pygame.display.flip()
            clock.tick(fps)

    def terminate(self):
        pygame.quit()
        sys.exit()
