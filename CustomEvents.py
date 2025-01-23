import pygame

import init_pygame

assert init_pygame.get_pygame_init()

UPDATE_ANIMATION = pygame.USEREVENT + 1

pygame.time.set_timer(UPDATE_ANIMATION, 200)
