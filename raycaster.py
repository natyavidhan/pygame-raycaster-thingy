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
            rays.append([l, i, angle])
        self.draw_walls(rays)


    def cast_ray(self, angle):
        l = 0
        while True:
            l += 0.25
            x = self.player.pos[0] + l * math.sin(math.radians(angle))
            y = self.player.pos[1] + l * math.cos(math.radians(angle))
            if not self.valid_pos((x, y)) or l > 1000:
                return l

    def draw_walls(self, rays: list[float], draw_rays = False):
        rays.sort(key=lambda x: x[0])
        SCALE = self.screen.get_width() / self.rays
        for i, ray in enumerate(rays):
            if draw_rays:
                pygame.draw.line(self.screen, (255, 255, 0), self.player.pos, (self.player.pos[0] + ray[0] * math.sin(math.radians(ray[1])), self.player.pos[1] + ray[0] * math.cos(math.radians(ray[1]))))            
            depth = max(ray[0], 0.0001)
            color = 255 / (1 + depth * depth * 0.0001)
            depth*=math.cos(math.radians(ray[2] - self.player.angle))
            h = 15000 / depth
            s_height = self.screen.get_height()
            s_width = self.screen.get_width()
            pygame.draw.rect(self.screen, (color, color, color), (ray[1] * SCALE, s_height / 2 - h / 2, SCALE+0.5, h))

    def map_value(self, var, min, max, new_min, new_max):
        return (var - min) / (max - min) * (new_max - new_min) + new_min

    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.cast_rays()
        self.screen.blit(pygame.transform.scale(self.map_img, (150, 150)), (0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.map_value(self.player.pos[0], 0, self.map_img.get_width(), 0, 150)), int(self.map_value(self.player.pos[1], 0, self.map_img.get_height(), 0, 150))), 5)