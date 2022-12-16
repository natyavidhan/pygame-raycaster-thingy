from raycaster import Raycaster
import pygame
import math

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.raycaster = Raycaster(self.screen)

        pygame.display.set_caption("Raycaster")
        self.clock = pygame.time.Clock()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(60)
            self.screen.fill((0, 0, 0))

            self.raycaster.cast_rays()

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()