import pygame, math
from PIL import Image

class Raycaster:
    def __init__(self, size, player, entities=None, fov=90, background="./assets/back.png"):
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, size)
        self.map = []
        self.map_img = None
        self.player = player
        self.clock = pygame.time.Clock()
        self.fov = fov
        self.rays = 240
        
    def load_map(self, map_file):
        img = Image.open(map_file)
        img = img.convert("RGBA")
        self.map = list(img.getdata())
        self.map_img = pygame.image.load(map_file)
    
    def valid_pos(self, pos):
        return self.map[int(pos[1]) * self.map_img.get_width() + int(pos[0])] == (0, 0, 0, 0)

    def cast_rays(self):
        angle = self.player.angle - self.fov / 2
        rays = []
        for i in range(self.rays):
            angle += self.fov / self.rays
            l = self.cast_ray(angle)
            rays.append([l, angle])
            # pygame.draw.line(self.screen, (255, 255, 0), self.player.pos, (self.player.pos[0] + l * math.sin(math.radians(angle)), self.player.pos[1] + l * math.cos(math.radians(angle))))
        self.draw_rays(rays)


    def cast_ray(self, angle):
        l = 0
        while True:
            l += 2
            x = self.player.pos[0] + l * math.sin(math.radians(angle))
            y = self.player.pos[1] + l * math.cos(math.radians(angle))
            if not self.valid_pos((x, y)):
                return l

    def draw_rays(self, rays: list[float]):
        rays.sort(key=lambda x: x[0])
        for i, ray in enumerate(rays):
            pygame.draw.line(self.screen, (255, 255, 0), self.player.pos, (self.player.pos[0] + ray[0] * math.sin(math.radians(ray[1])), self.player.pos[1] + ray[0] * math.cos(math.radians(ray[1]))))            

    def update(self):
        self.screen.blit(self.background, (0, 0))
        if self.map_img:
            self.screen.blit(self.map_img, (0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), self.player.pos, 5)
        # draw a line facing the player
        pygame.draw.line(self.screen, (255, 0, 0), self.player.pos, (self.player.pos[0] + 100 * math.sin(math.radians(self.player.angle)), self.player.pos[1] + 100 * math.cos(math.radians(self.player.angle))))
        self.cast_rays()