import itertools
import os
from math import cos, radians, sin

import pygame

import CustomEvents
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

    explode_group = pygame.sprite.Group()


_flying_velocity = 180
_g_const = 210


class _AbstractHelicopter(pygame.sprite.Sprite):
    """Спрайт вертолета"""
    first_image: pygame.Surface | None = None
    second_image: pygame.Surface | None = None
    third_image: pygame.Surface | None = None
    height: int | None = None
    helicopter_velocity: int | None = None

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image_cycle = itertools.cycle((self.first_image, self.second_image, self.third_image))
        self.image = self.first_image
        self.rect = self.image.get_rect()
        self.rect.y = self.height
        self.explosion_step = 0
        self.is_destroyed = False

    def update(self, *args, **kwargs):
        if not args:
            self.animation()

    def animation(self):
        """Анимация движения вертолета"""
        self.image = next(self.image_cycle)
        self.move()

    def move(self):
        """Передвижение вертолета"""
        displacement = self.helicopter_velocity // fps
        self.rect.x += displacement
        if not self.rect.colliderect(main_screen.get_rect()):
            self.kill()

    def destroy(self):
        """Уничтожение вертолета"""
        explode_x, explode_y = self.rect.x, self.rect.y
        self.kill()
        Explode(explode_x, explode_y)

    def drop_paratrooper(self):
        """Сброс парашютиста"""


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
        self.image_cycle = itertools.cycle((self.first_image, self.second_image, self.third_image))
        self.image = self.first_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = self.height
        self.explosion_step = 0
        self.is_destroyed = False

    def update(self, *args, **kwargs):
        if not args:
            self.animation()

    def animation(self):
        """Анимация движения самолета"""
        self.image = next(self.image_cycle)
        self.move()

    def move(self):
        """Передвижение самолета"""
        displacement = self.jet_velocity // fps
        self.rect.x += displacement
        if not self.rect.colliderect(main_screen.get_rect()):
            self.kill()

    def destroy(self):
        """Уничтожение самолета"""
        explode_x, explode_y = self.rect.x, self.rect.y
        self.kill()
        Explode(explode_x, explode_y)

    def drop_bomb(self):
        """Сброс бомбы"""


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
        self.current_x: float | None = None
        self.current_y: float | None = None
        self.horizontal_velocity: int | None = None
        self.vertical_velocity = 0

    def move(self):
        """Перемещение бомбы"""
        vertical_velocity_delta = _g_const / fps
        self.vertical_velocity += vertical_velocity_delta

        vertical_displacement = self.vertical_velocity / fps
        horizontal_displacement = self.horizontal_velocity / fps

        self.current_x += horizontal_displacement
        self.current_y += vertical_displacement

        self.rect.x = self.current_x
        self.rect.y = self.current_y

    def update(self, *args, **kwargs):
        if not args:
            self.move()

    def destroy(self):
        """Уничтожение бомбы"""
        explode_x, explode_y = self.rect.x, self.rect.y
        self.kill()
        BombExplode(explode_x, explode_y)


class Bomb(_AbstractBomb):
    """Спрайт бомбы, сбрасываемой самолетом"""

    def __init__(self, way: str, x: int, y: int):
        super().__init__()

        velocity_dict = {'left': -_flying_velocity, 'right': _flying_velocity}
        if way not in velocity_dict:
            raise ValueError('way argument must be "left" or "right"')

        self.horizontal_velocity = velocity_dict[way]
        self.current_x = x
        self.current_y = y


class Paratrooper(pygame.sprite.Sprite):
    """Спрайт парашютиста"""
    paratrooper_image = load_image('images/trooper.png')
    list_of_divs = []
    for i in range(1, 3):
        list_of_divs.append('images/divs/div_' + str(i) + '.png')

    height = 30

    no_parachute_speed = 150
    with_parachute_speed = 90

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.paratrooper_group)
        self.image_cycle = itertools.cycle(tuple(self.list_of_divs))
        self.image = self.paratrooper_image
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = self.height
        self.is_moving = True
        self.falling_velocity = self.no_parachute_speed
        self.parachute = None
        self.parachute_used = False

    def update(self, *args, **kwargs):
        if not args:
            if self.rect.y >= 580:
                self.animation()
            else:
                self.move()

    def animation(self):
        """Анимация парашютиста (пригодится на сцене взбирания парашютистов)"""

    def move(self):
        """Падение парашютиста"""
        if pygame.sprite.spritecollideany(self, SpriteGroups.ground_group):
            self.is_moving = False
            if self.parachute is not None:
                self.kill_parachute()
            else:
                # Дорабатываем логику свободного падения
                pass

        if self.is_moving:
            displacement = self.falling_velocity // fps
            self.rect.y += displacement
            if self.rect.y >= 375 and not self.parachute_used:
                self.open_parachute()
                self.set_parachute_speed()
            if self.parachute:
                self.parachute.move()
            # ^ Заметка: Высота раскрытия парашюта не фиксированное число, дальше решим, как сделаем

    def destroy(self):
        """Уничтожение парашютиста"""
        self.kill_parachute()
        explode_x, explode_y = self.rect.x, self.rect.y
        self.kill()
        Explode(explode_x, explode_y)

    def open_parachute(self):
        """Раскрытие парашюта"""
        if self.parachute_used:
            return

        assert self.parachute is None
        self.parachute = Parachute(self)
        self.parachute_used = True

    def kill_parachute(self):
        """Убирает спрайт парашюта"""
        self.parachute.kill()
        self.parachute = None

    def set_no_parachute_speed(self):
        self.falling_velocity = self.no_parachute_speed

    def set_parachute_speed(self):
        self.falling_velocity = self.with_parachute_speed


class Parachute(pygame.sprite.Sprite):
    """Спрайт парашюта"""
    parachute_image = load_image('images/para.png')

    def __init__(self, host: Paratrooper):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.parachute_group)
        self.image = self.parachute_image
        self.rect = self.image.get_rect()
        self.rect.x = host.rect.x - self.rect.w // 2 + host.rect.w // 2
        self.rect.y = host.rect.y - 30
        self.speed = 90

        self.host = host

    def update(self, *args, **kwargs):
        if not args:
            pass

    def move(self):
        """Передвижение парашюта"""
        displacement = self.speed // fps
        self.rect.y += displacement

    def destroy(self):
        """Уничтожение парашюта"""
        self.host.kill_parachute()
        self.host.set_no_parachute_speed()


class Gun(pygame.sprite.Sprite):
    """Спрайт турели"""
    left_angle = 190
    right_angle = 350
    center_x, center_y = 39, 33
    gun_length = 35
    white_rect_x, white_rect_y = 0, 55
    pink_part_x = 27
    rect_part_pink_y = 35

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.gun_group)
        self.is_moving = 0
        self.angle = 270
        self.image = pygame.Surface((80, 115), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 360, 460

    def draw(self):
        white_color = (255, 255, 255)
        blue_color = (85, 255, 255)
        pink_color = (255, 84, 255)
        self.end_gun_point = tuple(map(round, (self.gun_length * cos(radians(self.angle)) + self.center_x,
                                               self.gun_length * sin(radians(self.angle)) + self.center_y)))

        self.image.fill((0, 0, 0))
        pygame.draw.rect(self.image, white_color, (self.white_rect_x, self.white_rect_y, 80, 60))
        # pygame.draw.aaline(self.image, (85, 255, 255), (self.center_x, self.center_y), end_gun_point)
        pygame.draw.line(self.image, blue_color, (self.center_x, self.center_y), self.end_gun_point, width=8)

        pygame.draw.rect(self.image, pink_color, (self.pink_part_x, self.rect_part_pink_y, 25, 20))
        pygame.draw.ellipse(self.image, pink_color, (self.pink_part_x, self.rect_part_pink_y - 15, 25, 25))
        pygame.draw.rect(self.image, blue_color, (self.center_x - 3, self.center_y - 3, 6, 6))

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
            self.angle += 5 * self.is_moving
            if self.is_moving == 1 and self.angle >= self.right_angle:
                self.is_moving = 0
                self.angle = self.right_angle
            if self.is_moving == -1 and self.angle <= self.left_angle:
                self.is_moving = 0
                self.angle = self.left_angle
            self.draw()
        self.angle %= 360

    def destroy(self):
        """У пушки тоже должна быть анимация уничтожения с вызовом класса Explode"""


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

            collided_enemies = pygame.sprite.spritecollide(self, SpriteGroups.enemies_group, False,
                                                           pygame.sprite.collide_mask)
            if collided_enemies:
                collided_enemy = collided_enemies[0]
                collided_enemy.destroy()
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


class Explode(pygame.sprite.Sprite):
    """Спрайт с анимацией взрыва"""
    explode_images = tuple(map(lambda number: load_image(f'images/aviation_explosion/enemy_explosion_{number}.png'),
                               range(1, 11)))

    def __init__(self, x: int, y: int):
        super().__init__(SpriteGroups.main_group, SpriteGroups.explode_group)
        self.image_iter = iter(self.explode_images)
        self.image = next(self.image_iter)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, *args, **kwargs):
        if args:
            event = args[0]
            if event.type == CustomEvents.UPDATE_ANIMATION:
                try:
                    self.image = next(self.image_iter)
                except StopIteration:
                    self.kill()


class BombExplode(pygame.sprite.Sprite):
    """Спрайт с анимацией взрыва бомбы"""
    explode_images = tuple(map(lambda number: load_image(f'images/bomb_explosion/explode_{number}.png'),
                               range(1, 10)))

    def __init__(self, x: int, y: int):
        super().__init__(SpriteGroups.main_group, SpriteGroups.explode_group)
        self.image_iter = iter(self.explode_images)
        self.image = next(self.image_iter)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def update(self, *args, **kwargs):
        if args:
            event = args[0]
            if event.type == CustomEvents.UPDATE_ANIMATION:
                try:
                    self.image = next(self.image_iter)
                except StopIteration:
                    self.kill()


class FallDeath(pygame.sprite.Sprite):
    """Спрайт с анимацией смерти от падения
    реализация должна быть примерно похожа на Explode"""


# Данные спрайты существуют в единственном экземпляре с начала игры, поэтому их можно сразу инициализировать
gun = Gun()
ground = Ground()
