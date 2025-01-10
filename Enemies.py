from random import randrange

import LoadImages
import pygame


class Helicopter(pygame.sprite.Sprite):
    pass


class HelicopterLeft(Helicopter):
    first_image = LoadImages.load_image('images/helicopter_left_1.png')
    second_image = LoadImages.load_image('images/helicopter_left_2.png')
    third_image = LoadImages.load_image('images/helicopter_left_3.png')

    def __init__(self, group):
        super().__init__(group)
        self.num_of_sprite = 0
        self.image = HelicopterLeft.first_image
        self.rect = self.image.get_rect()
        self.rect.x = randrange(0, 1)
        self.rect.y = randrange(10, 50)

    def update(self, *args):
        pass
        self.animation()

    def animation(self):
        if self.num_of_sprite % 3 == 0:
            self.image = self.first_image
        elif self.num_of_sprite % 3 == 1:
            self.image = self.second_image
        else:
            self.image = self.third_image
        self.num_of_sprite += 1


class HelicopterRight(Helicopter):
    pass
