"""Поток противников можно разделить на волны
Каждую волну можно точно описать:
-Длительность волны
-Информация о всех вертолетах, каждый из которых в свою очередь будет хранить в себе информацию о том,
когда и где он сбросит парашютистов
-Информация о всех самолетах (самолеты тоже можно будет разделить на мини-волны) и о том, сбросят они бомбу или нет"""
from random import randint

import CustomEvents
from Sprites import HelicopterLeft, HelicopterRight, JetLeft, JetRight


class EnemyWave:
    max_helicopters = randint(8, 10)
    max_jet = randint(3, 5)

    def __init__(self, mini_waves, next_waves=1):
        self.mini_waves = mini_waves
        self.next_waves = next_waves
        self.helicopter_count = 0
        self.jet_count = 0
        self.jet_or_helicopter = True

    def update(self, *args, **kwargs):
        if self.mini_waves == 0:
            if self.next_waves != 0:
                return EnemyWave(self.next_waves)
        if args:
            event = args[0]
            if event.type == CustomEvents.SPAWN_NEW_AVIATION:
                if self.jet_or_helicopter and self.helicopter_count <= self.max_helicopters:
                    self.spawn_helicopter()
                    self.helicopter_count += 1
                else:
                    if self.helicopter_count > self.max_helicopters:
                        self.jet_or_helicopter = False
                        self.helicopter_count = 0
                        self.mini_waves -= 1
                    if self.jet_count <= self.max_jet:
                        self.spawn_jet()
                        self.jet_count += 1
                    else:
                        self.jet_or_helicopter = True
                        self.jet_count = 0
                        self.mini_waves -= 1

    def spawn_helicopter(self):
        if randint(0, 1) == 0:
            HelicopterLeft()
        else:
            HelicopterRight()

    def spawn_jet(self):
        if randint(0, 1) == 0:
            JetLeft()
        else:
            JetRight()
