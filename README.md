# **PARATROOPER**

## Создатели:

* Осинкин Александр(_MrToxic-png_)
* _buj17_

## Идея:

Защищайте свою турель, стреляя по врагам.

Предотвратите высадку парашютистов и не дайте им достать до вашей башни.

## Управление
* Пробел - начать игру
* Стрелка вверх - выстрелить и остановить пушку
* Стрелка влево - повернуть пушку влево
* Стрелка вправо - повернуть пушку вправо

## Начисление очков за устранения
* Самолет / вертолет - 10 очков
* Парашютист - 5 очков
* Бомба - 30 очков
* Каждый выстрел стоит 1 очко

## Примененные технологии
* ### pygame - основная библиотека для игры
* ### numpy, random - используются вычисления случайных значений
* ### math - используется для работы с тригонометрией

## Структура проекта
* ### assets - директория для хранения изображений, звуков, пользовательского шрифта
* ### init_pygame - модуль для инициализации pygame
* ### Sprites - основной модуль с логикой спрайтов
* * SpriteGroups - класс, хранящий все существующие группы спрайтов
* * Helicopter - спрайт вертолета
* * Jet - спрайт самолета
* * Bomb - спрайт бомбы
* * Paratrooper - спрайт парашютиста
* * Parachute - спрайт парашюта
* * Gun - спрайт турели
* * Bullet - спрайт пули
* * Ground - спрайт поверхности
* * Explode, BombExplode, FallDeath - спрайты-анимации
* * ParatrooperState - класс, управляющий состоянием парашютистов
* ### CustomEvents - модуль, хранящий пользовательские события
* ### Wave - модуль, содержащий класс для реализации волн противников
* ### GameProcess - модуль, содержащий класс, управляющий игровым процессом
* ### MainWindow - модуль, содержащий одноименный класс, реализующий главное окно программы
* ### main - главный модуль для запуска программы

#### Ссылка на видео с игровым процессом:
https://disk.yandex.ru/i/fr6wbqCPoXcjQA