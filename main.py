from raycaster import Raycaster
import pygame
import math

class Player:
    def __init__(self, pos, angle, speed):
        self.pos = pos
        self.angle = angle
        self.speed = speed

    def move(self, dist):
        self.pos[0] += math.sin(math.radians(self.angle)) * dist
        self.pos[1] += math.cos(math.radians(self.angle)) * dist

class Game:
    def __init__(self):
        self.player = Player([10, 10], 0, 0.1)
        self.raycaster = Raycaster((640, 320), self.player, fov=90)
        self.raycaster.load_map("./assets/map.png")
        self.running = True
        

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(self.player.speed)
            if keys[pygame.K_s]:
                self.player.move(-self.player.speed)
            if keys[pygame.K_a]:
                self.player.angle += 0.5
            if keys[pygame.K_d]:
                self.player.angle -= 0.5

            self.raycaster.update()
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()