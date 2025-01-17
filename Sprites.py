import itertools
import os
from asyncio import wait_for

import pygame

from init_pygame import width


def load_image(filename: str | os.PathLike, colorkey=None) -> pygame.Surface:
    """Функция для получения изображения из файла"""
    fullname = filename
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class SpriteGroups:
    """Основные группы спрайтов, выделенные для игры"""
    main_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()
    helicopter_group = pygame.sprite.Group()
    left_helicopter_group = pygame.sprite.Group()
    right_helicopter_group = pygame.sprite.Group()
    jet_group = pygame.sprite.Group()
    parachute_group = pygame.sprite.Group()
    paratrooper_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()


class Helicopter(pygame.sprite.Sprite):
    """Спрайт вертолета"""
    first_image: pygame.Surface | None = None
    second_image: pygame.Surface | None = None
    third_image: pygame.Surface | None = None
    height: int | None = None

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image_cycle = itertools.cycle((self.first_image, self.second_image, self.third_image))
        self.image = self.first_image
        self.rect = self.image.get_rect()
        self.rect.y = self.height

    def update(self, *args, **kwargs):
        pass
        if not args:
            self.animation()

    def animation(self):
        self.image = next(self.image_cycle)
        self.move()

    def move(self):
        return


class HelicopterLeft(Helicopter):
    first_image = load_image('images/aviation/helicopter_left_1.png')
    second_image = load_image('images/aviation/helicopter_left_2.png')
    third_image = load_image('images/aviation/helicopter_left_3.png')

    height = 50

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect.x = -73

    def move(self):
        self.rect.x += 3
        if self.rect.x > 900:
            self.rect.x = -73


class HelicopterRight(Helicopter):
    first_image = load_image('images/aviation/helicopter_right_1.png')
    second_image = load_image('images/aviation/helicopter_right_2.png')
    third_image = load_image('images/aviation/helicopter_right_3.png')

    height = 10

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect.x = 800

    def animation(self):
        self.image = next(self.image_cycle)
        self.rect.x -= 3
        if self.rect.x < -173:
            self.rect.x = 800


class Jet(pygame.sprite.Sprite):
    """Спрайт реактивного самолета"""
    first_image: pygame.Surface | None = None
    second_image: pygame.Surface | None = None
    third_image: pygame.Surface | None = None
    height: int | None = None

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image_cycle = itertools.cycle((self.first_image, self.second_image, self.third_image))
        self.image = self.first_image
        self.rect = self.image.get_rect()
        self.rect.y = self.height

    def update(self, *args, **kwargs):
        pass
        if not args:
            self.animation()

    def animation(self):
        self.image = next(self.image_cycle)
        self.move()

    def move(self):
        return


class JetLeft(Jet):
    first_image = load_image('images/aviation/jet_left_1.png')
    second_image = load_image('images/aviation/jet_left_2.png')
    third_image = load_image('images/aviation/jet_left_3.png')

    height = 50

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect.x = -73

    def move(self):
        self.rect.x += 4
        if self.rect.x > 900:
            self.rect.x = -73


class JetRight(Jet):
    first_image = load_image('images/aviation/jet_right_1.png')
    second_image = load_image('images/aviation/jet_right_2.png')
    third_image = load_image('images/aviation/jet_right_3.png')

    height = 10

    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect.x = 800

    def animation(self):
        self.image = next(self.image_cycle)
        self.rect.x -= 4
        if self.rect.x < -173:
            self.rect.x = 800


class Bomb(pygame.sprite.Sprite):
    """Спрайт бомбы, сбрасываемой самолетом"""
    bomb_image = load_image('images/bomb.png')
    list_of_explosions = []
    for i in range(1, 10):
        list_of_explosions.append('images/bomb_explosion/explode_' + str(i) + '.png')

    height = 10

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image_cycle = itertools.cycle(tuple(self.list_of_explosions))
        self.image = self.bomb_image
        self.rect = self.image.get_rect()
        self.rect.x = 20
        self.rect.y = self.height

    def update(self, *args, **kwargs):
        if not args:
            if self.rect.y >= 590:
                self.animation()
            else:
                self.move()

    def animation(self):
        pass

    def move(self):
        self.rect.y += 5


class Paratrooper(pygame.sprite.Sprite):
    """Спрайт парашютиста"""
    paratrooper_image = load_image('images/trooper.png')
    list_of_divs = []
    for i in range(1, 3):
        list_of_divs.append('images/divs/div_' + str(i) + '.png')

    height = 30

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image_cycle = itertools.cycle(tuple(self.list_of_divs))
        self.image = self.paratrooper_image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = self.height

    def update(self, *args, **kwargs):
        if not args:
            if self.rect.y >= 580:
                self.animation()
            else:
                self.move()

    def animation(self):
        pass

    def move(self):
        if self.rect.y <= 300:
            self.rect.y += 5
        else:
            self.rect.y += 3


class Parachute(pygame.sprite.Sprite):
    """Спрайт парашюта"""
    parachute_image = load_image('images/para.png')

    height = 0

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.parachute_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = self.height

    def update(self, *args, **kwargs):
        if not args:
            if self.rect.y >= 550:
                self.kill()
            else:
                self.move()

    def animation(self):
        pass

    def move(self):
        if self.rect.y <= 270:
            self.rect.y += 5
        else:
            self.rect.y += 3


class Gun(pygame.sprite.Sprite):
    """Спрайт турели"""
    def __init__(self, *groups):
        super().__init__(*groups)
        self.angle = 0
        self.image = pygame.Surface((80, 115), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 360, 460

    def draw(self):
        pygame.draw.rect(self.image, (255, 255, 255), (0, 55, 80, 60))
        pygame.draw.line(self.image, (85, 255, 255), (39, 33), (39, 5), width=5)
        pygame.draw.rect(self.image, (255, 84, 255), (27, 35, 25, 20))
        pygame.draw.ellipse(self.image, (255, 84, 255), (27, 25, 25, 20))
        pygame.draw.rect(self.image, (85, 255, 255), (36, 30, 6, 6))

    def update(self, *args, **kwargs):
        pass
        if not args:
            self.draw()

    def animation(self):
        pass

    def move(self):
        pass


class Bullet(pygame.sprite.Sprite):
    """Спрайт пули, которой турель стреляет"""
    parachute_image = load_image('images/bullet.png')

    height = 600

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = self.parachute_image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = self.height

    def update(self, *args, **kwargs):
        if not args:
            if self.rect.y <= 0:
                self.kill()
            else:
                self.move()

    def animation(self):
        pass

    def move(self):
        self.rect.x += 2
        self.rect.y -= 4
