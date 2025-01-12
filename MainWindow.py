import pygame

from Sprites import HelicopterLeft, HelicopterRight, JetRight, JetLeft
from init_pygame import width, height, fps, main_screen


class MainWindow:
    def __init__(self):
        pass

    def show_intro(self):
        image = pygame.image.load('images/aviation/intro.png')
        main_screen.blit(image, (0, 0))
        pygame.display.flip()

    def run(self):
        self.show_intro()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break

        clock = pygame.time.Clock()
        running = True
        screen = pygame.display.set_mode((width, height))

        all_sprites = pygame.sprite.Group()

        JetRight(all_sprites)
        JetLeft(all_sprites)

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
