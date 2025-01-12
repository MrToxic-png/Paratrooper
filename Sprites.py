import itertools
import os

import pygame


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
    pass


class Paratrooper(pygame.sprite.Sprite):
    """Спрайт парашютиста"""
    pass


class Parachute(pygame.sprite.Sprite):
    """Спрайт парашюта"""
    pass


class Gun(pygame.sprite.Sprite):
    """Спрайт турели"""
    pass


class Bullet(pygame.sprite.Sprite):
    """Спрайт пули, которой турель стреляет"""
    pass
