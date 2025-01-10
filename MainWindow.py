import pygame

size = width, height = 800, 600
fps = 60
main_screen = pygame.display.set_mode((width, height))


class MainWindow:
    def __init__(self):
        pass

    def show_intro(self):
        pass

    def run(self):
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
