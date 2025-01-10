import itertools
from random import randrange

import LoadImages
import pygame


class Helicopter(pygame.sprite.Sprite):
    first_image: pygame.Surface | None = None
    second_image: pygame.Surface | None = None
    third_image: pygame.Surface | None = None

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image_cycle = itertools.cycle((self.first_image, self.second_image, self.third_image))
        self.image = self.first_image
        self.rect = self.image.get_rect()


class HelicopterLeft(Helicopter):
    first_image = LoadImages.load_image('images/helicopter_left_1.png')
    second_image = LoadImages.load_image('images/helicopter_left_2.png')
    third_image = LoadImages.load_image('images/helicopter_left_3.png')

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect.x = -100
        self.rect.y = randrange(10, 50)

    def update(self, *args):
        pass
        if not args:
            self.animation()

    def animation(self):
        self.image = next(self.image_cycle)
        self.rect.x += 3


class HelicopterRight(Helicopter):
    first_image = LoadImages.load_image('images/helicopter_right_1.png')
    second_image = LoadImages.load_image('images/helicopter_right_2.png')
    third_image = LoadImages.load_image('images/helicopter_right_3.png')

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect.x = 900
        self.rect.y = randrange(10, 50)

    def update(self, *args):
        pass
        if not args:
            self.animation()

    def animation(self):
        self.image = next(self.image_cycle)
        self.rect.x -= 3
