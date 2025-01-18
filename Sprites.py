import itertools
import os
from math import cos, radians, sin

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
    left_jet_group = pygame.sprite.Group()
    right_jet_group = pygame.sprite.Group()
    parachute_group = pygame.sprite.Group()
    paratrooper_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    gun_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    ground_group = pygame.sprite.Group()


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

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.helicopter_group,
                         SpriteGroups.left_helicopter_group)
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

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.helicopter_group,
                         SpriteGroups.right_helicopter_group)
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

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.jet_group,
                         SpriteGroups.left_jet_group)
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

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.jet_group,
                         SpriteGroups.right_jet_group)
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

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.bomb_group)
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

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.paratrooper_group)
        self.image_cycle = itertools.cycle(tuple(self.list_of_divs))
        self.image = self.paratrooper_image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = self.height

        self.parachute = Parachute(self)

    def update(self, *args, **kwargs):
        if not args:
            if self.rect.y >= 580:
                self.animation()
            else:
                self.move()

    def animation(self):
        pass

    def move(self):
        if self.parachute is not None:
            if pygame.sprite.spritecollideany(self, SpriteGroups.ground_group):
                self.parachute.kill()
                self.parachute = None
            else:
                self.rect.y += 3
                self.parachute.move()


class Parachute(pygame.sprite.Sprite):
    """Спрайт парашюта"""
    parachute_image = load_image('images/para.png')

    height = 0

    def __init__(self, host: Paratrooper):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.parachute_group)
        self.image = self.parachute_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = self.height

        self.host = host

    def update(self, *args, **kwargs):
        if not args:
            pass

    def animation(self):
        pass

    def move(self):
        self.rect.y += 3


class Gun(pygame.sprite.Sprite):
    """Спрайт турели"""
    left_angle = 190
    right_angle = 350
    center_x, center_y = 39, 33
    gun_length = 35

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.gun_group)
        self.is_moving = 0
        self.angle = 270
        self.image = pygame.Surface((80, 115), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.second_x = 39
        self.second_y = 5
        self.rect.x, self.rect.y = 360, 460

    def draw(self):
        self.end_gun_point = tuple(map(lambda x: round(x), (self.gun_length * cos(radians(self.angle)) + self.center_x,
                                                            self.gun_length * sin(
                                                                radians(self.angle)) + self.center_y)))

        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 55, 80, 60))
        # pygame.draw.aaline(self.image, (85, 255, 255), (self.center_x, self.center_y), end_gun_point)
        pygame.draw.line(self.image, (85, 255, 255), (self.center_x, self.center_y), self.end_gun_point, width=8)

        pygame.draw.rect(self.image, (255, 84, 255), (27, 35, 25, 20))
        pygame.draw.ellipse(self.image, (255, 84, 255), (27, 20, 25, 25))
        pygame.draw.rect(self.image, (85, 255, 255), (36, 30, 6, 6))

    def update(self, *args, **kwargs):
        if args and args[0].type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.is_moving = 1
            if keys[pygame.K_LEFT]:
                self.is_moving = -1
            if keys[pygame.K_UP]:
                self.is_moving = 0
                Bullet(self.end_gun_point)

        if not args:
            self.angle += 3 * self.is_moving
            if self.is_moving == 1 and self.angle >= self.right_angle:
                self.is_moving = 0
                self.angle = self.right_angle
            if self.is_moving == -1 and self.angle <= self.left_angle:
                self.is_moving = 0
                self.angle = self.left_angle
            self.draw()
        self.angle %= 360


class Bullet(pygame.sprite.Sprite):
    """Спрайт пули, которой турель стреляет"""
    parachute_image = load_image('images/bullet.png')

    height = 600

    def __init__(self, bullet_spawn_point):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.bullet_group)
        self.bullet_spawn_point = bullet_spawn_point
        self.image = self.parachute_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = self.bullet_spawn_point[0] + 360
        self.rect.y = self.bullet_spawn_point[1] + 460

    def update(self, *args, **kwargs):
        if not args:
            if self.rect.y <= 0:
                self.kill()
            else:
                self.move()

    def move(self):
        self.rect.x -= (39 - self.bullet_spawn_point[0]) // 5
        self.rect.y -= (33 - self.bullet_spawn_point[1]) // 5


class Ground(pygame.sprite.Sprite):
    """Плоскость, на которую приземляются парашютисты"""
    ground_image = pygame.Surface((width, 2), pygame.SRCALPHA, 32)
    pygame.draw.rect(ground_image, (130, 236, 232), (0, 0, width, 2))

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.ground_group)
        self.image = self.ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 0, 575


# Данные спрайты существуют в единственном экземпляре с начала игры, поэтому их можно сразу инициализировать
gun = Gun()
ground = Ground()
