import pygame

from Sprites import JetRight, JetLeft, Paratrooper, Bullet, SpriteGroups
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

        JetRight()
        JetLeft()
        Paratrooper()
        Bullet()

        while running:
            main_screen.fill((0, 0, 0))
            for event in pygame.event.get():
                SpriteGroups.main_group.update(event)
                if event.type == pygame.QUIT:
                    running = False
            SpriteGroups.main_group.update()
            SpriteGroups.main_group.draw(screen)
            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
