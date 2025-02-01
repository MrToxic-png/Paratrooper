"""Основной игровой процесс достаточно объемный, поэтому его можно выделить в класс Game"""
import pygame

import CustomEvents
import Sprites
from Wave import EnemyWave
from init_pygame import main_screen


class Game:
    """Основной класс, контролирующий игровой процесс"""

    def __init__(self):
        self.high_score = None
        self.load_high_score()

        self.enemy_wave = EnemyWave()
        self.waiting_for_restart = False
        self.game_stopped = False

    def load_high_score(self):
        """Загрузка лучшего результата"""
        with open('assets/high_score.txt', encoding='utf-8') as file:
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

    @staticmethod
    def draw_endgame_text():
        """Отрисовка сообщения на перезапуск"""
        font = pygame.font.Font("assets/super-legend-boy.otf", 23)
        text = font.render('Press SPACE to restart', True, (255, 255, 255))
        main_screen.blit(text, (200, 200))

    def write_high_score(self):
        """Запись лучшего результата в файл"""
        with open('assets/high_score.txt', 'w', encoding='utf-8') as file:
            file.write(str(self.high_score))

    def draw(self):
        main_screen.fill((0, 0, 0))
        Sprites.SpriteGroups.main_group.draw(main_screen)
        self.draw_score()
        if self.waiting_for_restart:
            self.draw_endgame_text()
        pygame.display.flip()

    def update(self, *args):
        """Обработка событий"""
        if self.waiting_for_restart:
            if args:
                event = args[0]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.disable_waiting_for_restart()
                        Sprites.restart()
                        self.restart()
                    else:
                        return

        if args and args[0].type == CustomEvents.ENDGAME_HOLD:
            self.enable_waiting_for_restart()
            CustomEvents.switch_off_endgame_hold()

        else:
            self.draw()
            if Sprites.game_is_end() and not self.game_stopped:
                self.enemy_wave.stop_wave()
                CustomEvents.switch_on_endgame_hold()
                self.game_stopped = True
                self.write_high_score()
            self.enemy_wave.update(*args)

    def restart(self):
        """Начало новой игры"""
        Sprites.restart()
        self.enemy_wave = EnemyWave()
        self.game_stopped = False

    def enable_waiting_for_restart(self):
        """Устанавливает ожидание перезапуска игры"""
        self.waiting_for_restart = True

    def disable_waiting_for_restart(self):
        """Отключается ожидание перезапуска игры"""
        self.waiting_for_restart = False
