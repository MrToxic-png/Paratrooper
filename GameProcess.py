"""Основной игровой процесс достаточно объемный, поэтому его можно выделить в класс Game"""
import pygame

from init_pygame import main_screen


class Game:
    """Основной класс, контролирующий игровой процесс"""

    score = 0

    def __init__(self):
        pass

    def draw_score(self):
        score_font = pygame.font.Font("assets/super-legend-boy.otf", 23)
        if self.score != 0:
            score_text = score_font.render(str(self.score), True, (255, 84, 255))
            main_screen.blit(score_text, (200, 577))
        text1 = score_font.render("SCORE:", True, (255, 255, 255))
        text2 = score_font.render("HI-SCORE:", True, (255, 255, 255))
        main_screen.blit(text1, (0, 577))
        main_screen.blit(text2, (470, 577))

    def update(self, event=None):
        """Обработка событий"""
        if not event:
            self.draw_score()
