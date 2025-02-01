"""Поток противников можно разделить на волны
Каждую волну можно точно описать:
-Длительность волны
-Информация о всех вертолетах, каждый из которых в свою очередь будет хранить в себе информацию о том,
когда и где он сбросит парашютистов
-Информация о всех самолетах (самолеты тоже можно будет разделить на мини-волны) и о том, сбросят они бомбу или нет"""
from random import randint

import CustomEvents
from Sprites import HelicopterLeft, HelicopterRight, JetLeft, JetRight, paratroopers_state, SpriteGroups


class EnemyWave:
    max_helicopters = randint(8, 10)
    max_jet = randint(3, 5)

    def __init__(self):
        self.helicopter_count = 0
        self.jet_count = 0
        self.jet_or_helicopter = True
        self.is_new_stage = False
        self.count = 0
        self.wave_stopped = False

    def update(self, *args):
        SpriteGroups.main_group.update(*args)
        if self.wave_stopped:
            return

        if args:
            event = args[0]
            if event.type == CustomEvents.SPAWN_NEW_AVIATION and not self.is_new_stage:
                if self.jet_or_helicopter and self.helicopter_count <= self.max_helicopters:
                    self.spawn_helicopter()
                    self.helicopter_count += 1
                else:
                    if self.helicopter_count > self.max_helicopters:
                        self.jet_or_helicopter = False
                        self.helicopter_count = 0
                        self.is_new_stage = True
                        self.max_jet = randint(3, 5)
                    elif self.jet_count <= self.max_jet:
                        self.spawn_jet()
                        self.jet_count += 1
                    else:
                        self.jet_or_helicopter = True
                        self.jet_count = 0
                        self.is_new_stage = True
                        self.max_helicopters = randint(8, 10)
            if event.type == CustomEvents.CD_NEW_WAVE and self.is_new_stage:
                self.count += 1
                if self.count != 1:
                    self.count = 0
                    self.is_new_stage = False

    def spawn_helicopter(self):
        if randint(0, 1) == 0:
            HelicopterLeft()
        else:
            HelicopterRight()

    def spawn_jet(self):
        if paratroopers_state.player_lost():
            return

        if randint(0, 1) == 0:
            JetLeft()
        else:
            JetRight()

    def stop_wave(self):
        self.wave_stopped = True
