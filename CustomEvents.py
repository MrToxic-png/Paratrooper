import pygame

import init_pygame

assert init_pygame.get_pygame_init()

UPDATE_ANIMATION = pygame.USEREVENT + 1

pygame.time.set_timer(UPDATE_ANIMATION, 200)

SPAWN_NEW_AVIATION = pygame.USEREVENT + 2

pygame.time.set_timer(SPAWN_NEW_AVIATION, 1600)
