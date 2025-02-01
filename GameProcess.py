"""Основной игровой процесс достаточно объемный, поэтому его можно выделить в класс Game"""
import pygame

import Sprites
from Wave import EnemyWave
from init_pygame import main_screen


class Game:
    """Основной класс, контролирующий игровой процесс"""

    def __init__(self):
        self.high_score = None
        self.load_high_score()

        self.enemy_wave = EnemyWave()

    def load_high_score(self):
        """Загрузка лучшего результата"""
        with open('assets/high_score.txt') as file:
            self.high_score = int(file.read())

    def update_high_score(self):
        """Обновление лучшего результата"""
        self.high_score = max(Sprites.gun.score, self.high_score)

    def draw_score(self):
        """Отрисовка счета"""
        self.update_high_score()

        score_font = pygame.font.Font("assets/super-legend-boy.otf", 23)
        if Sprites.gun.score != 0:
            score_text = score_font.render(str(Sprites.gun.score), True, (255, 84, 255))
            main_screen.blit(score_text, (200, 577))
        high_score_text = score_font.render(str(self.high_score), True, (255, 255, 255))
        text1 = score_font.render("SCORE:", True, (255, 255, 255))
        text2 = score_font.render("HI-SCORE:", True, (255, 255, 255))
        main_screen.blit(text1, (0, 577))
        main_screen.blit(text2, (470, 577))
        main_screen.blit(high_score_text, (655, 577))

    def draw(self):
        main_screen.fill((0, 0, 0))
        Sprites.SpriteGroups.main_group.draw(main_screen)
        self.draw_score()
        pygame.display.flip()

    def update(self, *args):
        """Обработка событий"""
        self.draw()
        if Sprites.game_is_end():
            self.enemy_wave.stop_wave()
        self.enemy_wave.update(*args)

    def restart(self):
        """Начало новой игры"""
        self.enemy_wave = EnemyWave()
        Sprites.restart()
