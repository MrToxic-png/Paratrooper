import pygame
from Enemies import HelicopterLeft
from init_pygame import width, height, fps, main_screen


class MainWindow:
    def __init__(self):
        pass

    def show_intro(self):
        pass

    def run(self):
        clock = pygame.time.Clock()
        running = True
        screen = pygame.display.set_mode((width, height))

        all_sprites = pygame.sprite.Group()

        for _ in range(20):
            HelicopterLeft(all_sprites)

        while running:
            main_screen.fill((0, 0, 0))
            for event in pygame.event.get():
                all_sprites.update(event)
                if event.type == pygame.QUIT:
                    running = False
            all_sprites.update()
            all_sprites.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
