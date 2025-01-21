import itertools
import os
from math import cos, radians, sin

import pygame

from init_pygame import width, fps, main_screen


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
    enemy_aviation_group = pygame.sprite.Group()
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


_flying_velocity = 180
_g_const = 10


class _AbstractHelicopter(pygame.sprite.Sprite):
    """Спрайт вертолета"""
    first_image: pygame.Surface | None = None
    second_image: pygame.Surface | None = None
    third_image: pygame.Surface | None = None
    height: int | None = None
    helicopter_velocity: int | None = None

    def __init__(self, *groups):
        super().__init__(*groups)
        list_of_booms = []
        for i in range(1, 11):
            list_of_booms.append(load_image(f'images/aviation_explosion/enemy_explosion_{i}.png'))
        self.boom_images = itertools.cycle(tuple(list_of_booms))
        self.image_cycle = itertools.cycle((self.first_image, self.second_image, self.third_image))
        self.image = self.first_image
        self.rect = self.image.get_rect()
        self.rect.y = self.height
        self.explosion_step = 0
        self.is_destroyed = False

    def update(self, *args, **kwargs):
        if not args:
            if self.is_destroyed:
                self.animate_destruction()
            else:
                self.animation()

    def animation(self):
        self.image = next(self.image_cycle)
        self.move()

    def move(self):
        displacement = self.helicopter_velocity // fps
        self.rect.x += displacement
        if not self.rect.colliderect(main_screen.get_rect()):
            self.kill()

    def destroy(self):
        self.is_destroyed = True
        self.explosion_step = 0
        self.image = next(self.boom_images)

    def animate_destruction(self):
        if self.explosion_step <= 8:
            self.image = next(self.boom_images)
            self.explosion_step += 1
        else:
            self.kill()


class HelicopterLeft(_AbstractHelicopter):
    first_image = load_image('images/aviation/helicopter_left_1.png')
    second_image = load_image('images/aviation/helicopter_left_2.png')
    third_image = load_image('images/aviation/helicopter_left_3.png')

    height = 50
    helicopter_velocity = _flying_velocity

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.helicopter_group,
                         SpriteGroups.left_helicopter_group,
                         SpriteGroups.enemy_aviation_group)
        self.rect.x = -self.rect.w


class HelicopterRight(_AbstractHelicopter):
    first_image = load_image('images/aviation/helicopter_right_1.png')
    second_image = load_image('images/aviation/helicopter_right_2.png')
    third_image = load_image('images/aviation/helicopter_right_3.png')

    height = 10
    helicopter_velocity = -_flying_velocity

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.helicopter_group,
                         SpriteGroups.right_helicopter_group,
                         SpriteGroups.enemy_aviation_group)
        self.rect.x = width


class _AbstractJet(pygame.sprite.Sprite):
    """Спрайт реактивного самолета"""
    first_image: pygame.Surface | None = None
    second_image: pygame.Surface | None = None
    third_image: pygame.Surface | None = None
    jet_velocity: int | None = None
    height = 10

    def __init__(self, *groups):
        super().__init__(*groups)
        list_of_booms = []
        for i in range(1, 11):
            list_of_booms.append(load_image(f'images/aviation_explosion/enemy_explosion_{i}.png'))
        self.boom_images = itertools.cycle(tuple(list_of_booms))
        self.image_cycle = itertools.cycle((self.first_image, self.second_image, self.third_image))
        self.image = self.first_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = self.height
        self.explosion_step = 0
        self.is_destroyed = False

    def update(self, *args, **kwargs):
        if not args:
            if self.is_destroyed:
                self.animate_destruction()
            else:
                self.animation()

    def animation(self):
        self.image = next(self.image_cycle)
        self.move()

    def move(self):
        displacement = self.jet_velocity // fps
        self.rect.x += displacement
        if not self.rect.colliderect(main_screen.get_rect()):
            self.kill()

    def destroy(self):
        self.is_destroyed = True
        self.explosion_step = 0
        self.image = next(self.boom_images)

    def animate_destruction(self):
        if self.explosion_step <= 8:
            self.image = next(self.boom_images)
            self.explosion_step += 1
        else:
            self.kill()


class JetLeft(_AbstractJet):
    first_image = load_image('images/aviation/jet_left_1.png')
    second_image = load_image('images/aviation/jet_left_2.png')
    third_image = load_image('images/aviation/jet_left_3.png')

    height = 50
    jet_velocity = _flying_velocity

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.jet_group,
                         SpriteGroups.left_jet_group,
                         SpriteGroups.enemy_aviation_group)
        self.rect.x = -self.rect.w


class JetRight(_AbstractJet):
    first_image = load_image('images/aviation/jet_right_1.png')
    second_image = load_image('images/aviation/jet_right_2.png')
    third_image = load_image('images/aviation/jet_right_3.png')

    jet_velocity = -_flying_velocity

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.jet_group,
                         SpriteGroups.right_jet_group,
                         SpriteGroups.enemy_aviation_group)
        self.rect.x = width


class _AbstractBomb(pygame.sprite.Sprite):
    """Спрайт бомбы, сбрасываемой самолетом"""
    bomb_image = load_image('images/bomb.png')

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.bomb_group)
        self.image = self.bomb_image
        self.rect = self.image.get_rect()
        self.start_point: tuple[int, int] | None = None
        self.horizontal_velocity: int | None = None

    def move(self):
        """Перемещение бомбы"""


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
                # Нужно будет переписать:
                # задать константы: скорость падения парашютиста с парашютом и без него
                # далее реализовать метод через вычисление: displacement = fps / (константная скорость)
                # и добавлять displacement к координатам
                # Потом удалить это ^^^^

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
        # Здесь тоже следует реализовать через displacement
        # Потом удалить это ^^^^
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
        self.end_gun_point = tuple(map(round, (self.gun_length * cos(radians(self.angle)) + self.center_x,
                                               self.gun_length * sin(radians(self.angle)) + self.center_y)))

        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, (255, 255, 255), (0, 55, 80, 60))
        # pygame.draw.aaline(self.image, (85, 255, 255), (self.center_x, self.center_y), end_gun_point)
        pygame.draw.line(self.image, (85, 255, 255), (self.center_x, self.center_y), self.end_gun_point, width=8)

        pygame.draw.rect(self.image, (255, 84, 255), (27, 35, 25, 20))
        pygame.draw.ellipse(self.image, (255, 84, 255), (27, 20, 25, 25))
        pygame.draw.rect(self.image, (85, 255, 255), (36, 30, 6, 6))

        # Многа циферок, подумай над моим предложением сделать две картинки png, которые будем блитать (к Сане)
        # Или выдели из кода эти циферки так, чтобы они стали читаемы (тоже к Сане)
        # Также если мы сделаем png, то решим (очень вероятно) проблему с острыми углами
        # Потом удалить это ^^^^

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
            collided_jets = pygame.sprite.spritecollide(self, SpriteGroups.enemy_aviation_group, False,
                                                        pygame.sprite.collide_mask)
            if collided_jets:
                for jet in collided_jets:
                    if not jet.is_destroyed:
                        jet.destroy()
                        self.kill()

    def move(self):
        self.rect.x -= (39 - self.bullet_spawn_point[0]) // 5
        self.rect.y -= (33 - self.bullet_spawn_point[1]) // 5

        # Тоже следует переделать через displacement, можешь попробовать поебаться с kx + b (к Сане)
        # Потом удалить это ^^^^


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
