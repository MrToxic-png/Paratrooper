import itertools
import os
import random
from math import cos, radians, sin

import numpy
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
    image_sequence: tuple[pygame.Surface] | None = None
    height: int | None = None
    helicopter_velocity: int | None = None

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image_cycle = itertools.cycle(self.image_sequence)
        self.image = next(self.image_cycle)
        self.rect = self.image.get_rect()
        self.rect.y = self.height

        dropping_count = numpy.random.choice((0, 1, 2, 3), p=(0.3, 0.3, 0.3, 0.1))
        self.dropping_columns = set(random.sample(range(paratroopers_state.column_count), dropping_count))

    def update(self, *args, **kwargs):
        if args:
            event = args[0]
            if event.type == CustomEvents.UPDATE_ANIMATION:
                self.animation()
        if not args:
            self.move()

        column = paratroopers_state.get_nearest_column(self.rect.x)
        drop_paratrooper_conditions = (paratroopers_state.dropping_allowed,
                                       column in self.dropping_columns,
                                       paratroopers_state.get_diff_with_nearest_column(self.rect.x) <= 10,
                                       not paratroopers_state.any_flying_at_column(column))
        if all(drop_paratrooper_conditions):
            self.drop_paratrooper()
            self.dropping_columns.remove(column)

    def animation(self):
        """Анимация движения вертолета"""
        self.image = next(self.image_cycle)

    def move(self):
        """Передвижение вертолета"""
        displacement = self.helicopter_velocity / fps
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
        Paratrooper(ParatroopersState.get_nearest_column(self.rect.x), self.rect.y + self.rect.h)


class HelicopterLeft(_AbstractHelicopter):
    image_sequence = tuple(map(lambda number: load_image(f'images/aviation/helicopter_left_{number}.png'), (1, 2, 3)))

    height = 50
    helicopter_velocity = _flying_velocity

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.helicopter_group,
                         SpriteGroups.left_helicopter_group)
        self.rect.x = -self.rect.w


class HelicopterRight(_AbstractHelicopter):
    image_sequence = tuple(map(lambda number: load_image(f'images/aviation/helicopter_right_{number}.png'), (1, 2, 3)))

    height = 10
    helicopter_velocity = -_flying_velocity

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.helicopter_group,
                         SpriteGroups.right_helicopter_group)
        self.rect.x = width


class _AbstractJet(pygame.sprite.Sprite):
    """Спрайт реактивного самолета"""
    image_sequence: tuple[pygame.Surface] | None = None
    jet_velocity: int | None = None
    height = 10

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image_cycle = itertools.cycle(self.image_sequence)
        self.image = next(self.image_cycle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = self.height

    def update(self, *args, **kwargs):
        if args:
            event = args[0]
            if event.type == CustomEvents.UPDATE_ANIMATION:
                self.animation()
        if not args:
            self.move()

    def animation(self):
        """Анимация движения самолета"""
        self.image = next(self.image_cycle)

    def move(self):
        """Передвижение самолета"""
        displacement = self.jet_velocity / fps
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
    image_sequence = tuple(map(lambda number: load_image(f'images/aviation/jet_left_{number}.png'), (1, 2, 3)))
    jet_velocity = _flying_velocity

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.jet_group,
                         SpriteGroups.left_jet_group)
        self.rect.x = -self.rect.w


class JetRight(_AbstractJet):
    image_sequence = tuple(map(lambda number: load_image(f'images/aviation/jet_right_{number}.png'), (1, 2, 3)))
    jet_velocity = -_flying_velocity

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.jet_group,
                         SpriteGroups.right_jet_group)
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
    divs_image_sequence = tuple(map(lambda number: f'images/divs/div_{number}.png', (1, 2)))

    no_parachute_speed = 180
    with_parachute_speed = 105

    def __init__(self, column: int, y: int):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.enemies_group,
                         SpriteGroups.paratrooper_group)
        self.image_cycle = itertools.cycle(self.divs_image_sequence)
        self.image = self.paratrooper_image
        self._column = column
        self.rect = self.image.get_rect()
        self.rect.x = paratroopers_state.get_column_x(column)
        self.rect.y = y
        self.is_moving = True
        self.falling_velocity = self.no_parachute_speed
        self.parachute = None
        self.parachute_used = False
        self.open_parachute_y = random.randint(325, 375)

        paratroopers_state.update()

    @property
    def in_air(self):
        """Возвращает булево значение: находится ли парашютист в воздухе"""
        return self.is_moving

    @property
    def column(self):
        return self._column

    def update(self, *args, **kwargs):
        if not args:
            if self.rect.y >= 580:
                self.animation()
            elif self.is_moving:
                self.move()

    def animation(self):
        """Анимация парашютиста (пригодится на сцене взбирания парашютистов)"""

    def move(self):
        """Падение парашютиста"""
        colliding_other_paratroopers = any(
            map(lambda paratrooper: self is not paratrooper and pygame.sprite.collide_rect(self, paratrooper),
                SpriteGroups.paratrooper_group))
        if pygame.sprite.spritecollideany(self, SpriteGroups.ground_group) or colliding_other_paratroopers:
            self.is_moving = False
            if self.parachute is not None:
                self.kill_parachute()
            else:
                paratroopers_state.kill_column(self.column)
            paratroopers_state.update()

        if self.is_moving:
            displacement = self.falling_velocity / fps
            self.rect.y += displacement
            if self.rect.y >= self.open_parachute_y and not self.parachute_used:
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

    def die(self):
        dead_x, dead_y = self.rect.x, self.rect.y
        self.kill()
        FallDeath(dead_x, dead_y)

    def open_parachute(self):
        """Раскрытие парашюта"""
        if self.parachute_used:
            return

        assert self.parachute is None
        self.parachute = Parachute(self)
        self.parachute_used = True

    def kill_parachute(self):
        """Убирает спрайт парашюта"""
        if self.parachute:
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
        self.speed = Paratrooper.with_parachute_speed

        self.host = host

    def update(self, *args, **kwargs):
        if not args:
            pass

    def move(self):
        """Передвижение парашюта"""
        displacement = self.speed / fps
        self.rect.y += displacement

    def destroy(self):
        """Уничтожение парашюта"""
        self.host.kill_parachute()
        self.host.set_no_parachute_speed()


class Gun(pygame.sprite.Sprite):
    """Спрайт турели"""
    static_gun_part = load_image('images/gun/static_gun_part.png')
    base_rect_image = load_image('images/gun/base_rect.png')
    left_angle = 190
    right_angle = 350
    center_x, center_y = 39, 33
    gun_length = 35
    pink_part_x = 27
    rect_part_pink_y = 35

    angle_velocity = 150

    def __init__(self):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.gun_group)
        self.is_alive = True
        self.is_first = True
        self.is_moving = 0
        self.angle = 270
        self.image = pygame.Surface((80, 115), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 360, 460
        self.end_gun_point = tuple(map(round, (self.gun_length * cos(radians(self.angle)) + self.center_x,
                                               self.gun_length * sin(radians(self.angle)) + self.center_y)))

    def draw(self):
        blue_color = (85, 255, 255)
        self.image.fill((0, 0, 0))
        if self.is_alive:
            pygame.draw.line(self.image, blue_color, (self.center_x, self.center_y), self.end_gun_point, width=8)
            self.image.blit(self.static_gun_part, (0, 0))
        self.image.blit(self.base_rect_image, (0, 0))

    def update(self, *args, **kwargs):
        if args:
            event = args[0]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.is_moving = 1
                if event.key == pygame.K_LEFT:
                    self.is_moving = -1
                if event.key == pygame.K_UP:
                    self.is_moving = 0
                    Bullet(*self.end_gun_point, self.angle)
                if event.key == pygame.K_w:
                    self.destroy()

        if not args:
            self.angle += (self.angle_velocity / fps) * self.is_moving
            if self.is_moving == 1 and self.angle >= self.right_angle:
                self.is_moving = 0
                self.angle = self.right_angle
            if self.is_moving == -1 and self.angle <= self.left_angle:
                self.is_moving = 0
                self.angle = self.left_angle
            if self.is_alive:
                self.update_end_gun_point()
                self.draw()
        self.angle %= 360

    def destroy(self):
        """У пушки тоже должна быть анимация уничтожения с вызовом класса Explode"""
        self.is_alive = False
        self.draw()
        explode_x, explode_y = self.pink_part_x + 340, self.rect_part_pink_y + 420
        Explode(explode_x, explode_y)

    def update_end_gun_point(self):
        """Обновление координат крайней точки"""
        self.end_gun_point = tuple(map(round, (self.gun_length * cos(radians(self.angle)) + self.center_x,
                                               self.gun_length * sin(radians(self.angle)) + self.center_y)))


class Bullet(pygame.sprite.Sprite):
    """Спрайт пули, которой турель стреляет"""
    parachute_image = load_image('images/bullet.png')
    bullet_velocity = 300

    def __init__(self, bullet_spawn_x: int, bullet_spawn_y: int, angle: int):
        super().__init__(SpriteGroups.main_group,
                         SpriteGroups.bullet_group)
        self.image = self.parachute_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = bullet_spawn_x + 360
        self.rect.y = bullet_spawn_y + 460
        self.angle = angle

    def update(self, *args, **kwargs):
        if not args:
            if not self.rect.colliderect(main_screen.get_rect()):
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
        displacement_x = self.bullet_velocity * cos(radians(self.angle)) / fps
        displacement_y = self.bullet_velocity * sin(radians(self.angle)) / fps
        self.rect.x += displacement_x
        self.rect.y += displacement_y


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
    death_images = tuple(map(lambda number: load_image(f'images/die_animation/skull_{number}.png'),
                             range(1, 4)))

    def __init__(self, x: int, y: int):
        super().__init__(SpriteGroups.main_group, SpriteGroups.explode_group)
        self.image_iter = iter(self.death_images)
        self.image = next(self.image_iter)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x - 13, y - 30

    def update(self, *args, **kwargs):
        if args:
            event = args[0]
            if event.type == CustomEvents.UPDATE_ANIMATION:
                try:
                    self.image = next(self.image_iter)
                except StopIteration:
                    self.kill()


class ParatroopersState:
    """Класс, хранящий и управляющий информацией о парашютистах"""

    # Координаты x, по которым будут выравниваться парашютисты
    _left_side_cords_x = [45, 81, 117, 153, 189, 225, 261, 297, 333]  # Слева от пушки
    _right_side_cords_x = [465, 501, 537, 573, 609, 645, 681, 717, 753]  # Справа от пушки
    columns_cords = _left_side_cords_x + _right_side_cords_x
    column_count = len(columns_cords)

    def __init__(self):
        self.left_on_ground_count = 0
        self.right_on_ground_count = 0
        self.paratrooper_columns = [[] for _ in range(18)]
        self._dropping_allowed = True

    @property
    def dropping_allowed(self):
        """Возвращает булево значение: можно ли еще сбрасывать парашютиста или нет"""
        return self._dropping_allowed

    @classmethod
    def get_column_x(cls, column: int):
        """Возвращает координату x для определенного столбца"""
        return cls.columns_cords[column]

    @classmethod
    def get_nearest_column(cls, x: int):
        """Возвращает ближайший столбец для данного x"""
        return cls.columns_cords.index(min(cls.columns_cords, key=lambda column_x: abs(x - column_x)))

    @classmethod
    def get_diff_with_nearest_column(cls, x: int):
        """Возвращает расстояние до ближайшего столбца"""
        return abs(x - min(cls.columns_cords, key=lambda column_x: abs(x - column_x)))

    def update(self):
        """Полностью обновляет информацию о парашютистах"""
        for column in self.paratrooper_columns:
            column.clear()
        self.left_on_ground_count = 0
        self.right_on_ground_count = 0

        for paratrooper in SpriteGroups.paratrooper_group.sprites():
            paratrooper: Paratrooper
            self._add_paratrooper(paratrooper)
            if not paratrooper.in_air:
                if paratrooper.column < 9:
                    self.left_on_ground_count += 1
                else:
                    self.right_on_ground_count += 1

        if self.left_on_ground_count >= 4 or self.right_on_ground_count >= 4:
            self._stop_dropping()
        else:
            self._continue_dropping()

        for column in self.paratrooper_columns:
            column.sort(key=lambda paratrooper: paratrooper.rect.y, reverse=True)

    def get_blowing_group(self) -> list[Paratrooper, Paratrooper, Paratrooper, Paratrooper] | None:
        """Возвращает список из четырех парашютистов, которые будут штурмовать пушку, если это возможно
        Порядок парашютистов в списке соответствует порядку подхода парашютистов к пушке"""
        if not self.player_lost():
            return None

        blowing_group = []
        paratrooper_columns_copy = list(map(list.copy, self.paratrooper_columns))

        if self.left_on_ground_count >= 4:
            left_columns = paratrooper_columns_copy[:9]
            while True:
                leftest_column = left_columns.pop()
                while leftest_column:
                    paratrooper = leftest_column.pop()
                    blowing_group.append(paratrooper)
                    if len(blowing_group) == 4:
                        return blowing_group

        if self.right_on_ground_count >= 4:
            # Список переворачивается для эффективного извлечения через pop
            right_columns = paratrooper_columns_copy[9:][::-1]
            while True:
                leftest_column = right_columns.pop()
                while leftest_column:
                    paratrooper = leftest_column.pop()
                    blowing_group.append(paratrooper)
                    if len(blowing_group) == 4:
                        return blowing_group

    def kill_column(self, column: int):
        """Уничтожает всех парашютистов на земле на определенном столбце
        (Должно вызываться тогда, когда парашютист приземляется без парашюта)"""
        for paratrooper in self.paratrooper_columns[column]:
            paratrooper.kill()
        death_y_cord = 555
        FallDeath(self.get_column_x(column), death_y_cord)

    def player_lost(self):
        """Возвращает булево значение, проигрывает ли игрок:
        Игрок уже заведомо проигрывает, если на одной из сторон находится не менее 4 приземленных парашютистов
        (то есть сброс парашютистов остановлен), и при этом в воздухе не находится ни одного парашютиста"""
        return not self._any_paratrooper_in_air() and not self.dropping_allowed

    def any_flying_at_column(self, column: int):
        """Возвращает булево значение: есть ли летящие парашютисты в столбце или нет"""
        return any(map(lambda paratrooper: paratrooper.in_air, self.paratrooper_columns[column]))

    def _add_paratrooper(self, paratrooper: Paratrooper):
        """Добавляет парашютиста в определенный столбец"""
        self.paratrooper_columns[paratrooper.column].append(paratrooper)

    def _stop_dropping(self):
        """Остановить сброс парашютистов"""
        self._dropping_allowed = False

    def _continue_dropping(self):
        """Возобновить сброс парашютистов"""
        self._dropping_allowed = True

    def _any_paratrooper_in_air(self):
        """Возвращает булево значение: находится ли хотя бы один из парашютистов в воздухе"""
        return any(map(lambda column: any(map(lambda paratrooper: paratrooper.in_air, column)),
                       self.paratrooper_columns))


# Данные спрайты существуют в единственном экземпляре с начала игры, поэтому их можно сразу инициализировать
gun = Gun()
ground = Ground()

paratroopers_state = ParatroopersState()
