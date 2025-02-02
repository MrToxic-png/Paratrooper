import pygame

import init_pygame

assert init_pygame.get_pygame_init()

UPDATE_ANIMATION = pygame.USEREVENT + 1
pygame.time.set_timer(UPDATE_ANIMATION, 200)

SPAWN_NEW_AVIATION = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_NEW_AVIATION, 1800)

CD_NEW_WAVE = pygame.USEREVENT + 3
pygame.time.set_timer(CD_NEW_WAVE, 3600)

ENDGAME_HOLD = pygame.USEREVENT + 4
pygame.time.set_timer(ENDGAME_HOLD, 0)

LOSE_ANIMATION = pygame.USEREVENT + 5
pygame.time.set_timer(LOSE_ANIMATION, 600)


def switch_on_endgame_hold():
    """Включает отсчет в 5 секунд после уничтожения пушки"""
    pygame.time.set_timer(ENDGAME_HOLD, 5000)


def switch_off_endgame_hold():
    """Выключает отсчет в 5 секунд после уничтожения пушки"""
    pygame.time.set_timer(ENDGAME_HOLD, 0)
