from raycaster import Raycaster
import pygame
import math

class Player:
    def __init__(self, pos, angle, speed):
        self.pos = pos
        self.angle = angle
        self.speed = speed

    def move(self, dist):
        dx = dist * math.sin(math.radians(self.angle))
        dy = dist * math.cos(math.radians(self.angle))
        return (self.pos[0] + dx, self.pos[1] + dy)

class Game:
    def __init__(self):
        self.player = Player([10, 10], 0, 0.5)
        self.raycaster = Raycaster((640, 320), self.player, fov=90)
        self.raycaster.load_map("./assets/map.png")
        self.running = True
        

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.set_caption("FPS: " + str(round(self.raycaster.clock.get_fps())))

            delta_time = self.raycaster.clock.tick(600) / 10

            new_pos = (self.player.pos[0], self.player.pos[1])
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                new_pos = self.player.move(self.player.speed * delta_time)
            if keys[pygame.K_s]:
                new_pos = self.player.move(-self.player.speed * delta_time)
            if keys[pygame.K_a]:
                self.player.angle += 0.5
            if keys[pygame.K_d]:
                self.player.angle -= 0.5
            
            if self.raycaster.valid_pos(new_pos):
                self.player.pos = new_pos

            self.raycaster.update()
            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
