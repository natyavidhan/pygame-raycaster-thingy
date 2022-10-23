from raycaster import Raycaster
import pygame

class Game:
    def __init__(self):
        self.raycaster = Raycaster((640, 320), (0, 0), fov=90)
        self.raycaster.load_map("./assets/map.png")
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.raycaster.update()

if __name__ == "__main__":
    game = Game()
    game.run()