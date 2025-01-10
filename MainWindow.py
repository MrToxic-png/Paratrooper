import pygame

size = width, height = 800, 600
fps = 60
main_screen = pygame.display.set_mode((width, height))


class MainWindow:
    def __init__(self):
        pass

    def show_intro(self):
        print('show')
        image = pygame.image.load('images/intro.png')
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

        while running:
            main_screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            pygame.display.flip()
            clock.tick(fps)
        pygame.quit()
