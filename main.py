import init_pygame
from MainWindow import MainWindow

if __name__ == '__main__':
    if init_pygame.get_pygame_init():
        window = MainWindow()
        window.run()
