import pygame

pygame.init()

size = width, height = 800, 600
fps = 30
main_screen = pygame.display.set_mode((width, height))


def get_pygame_init():
    return pygame.get_init()
