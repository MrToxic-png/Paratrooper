"""Модуль, в котором реализуется класс главного окна приложения"""

import sys

import pygame

from GameProcess import Game
from init_pygame import fps, main_screen
from Soundpad import soundpad


class MainWindow:
    """Класс главного окна"""
    def __init__(self):
        self.game = Game()

    def show_intro(self):
        """Метод, показывающий стартовое окно"""
        image = pygame.image.load("assets/images/aviation/intro.png")
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

    def run(self):
        """Запуск игры"""
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

    @staticmethod
    def terminate():
        """Прерывание выполнения"""
        pygame.quit()
        sys.exit()
