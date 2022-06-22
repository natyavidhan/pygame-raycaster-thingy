import pygame, math, time
from PIL import Image

pygame.init()
pygame.font.init()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0 * math.pi / 180
        self.speed = 150

class Entity:
    def __init__(self, x, y, asset, handler):
        self.x = x
        self.y = y
        self.asset = asset
        self.img = pygame.image.load(asset)
        self.PIL_img = Image.open(asset)
        self.handler = handler

    def run(self, screen):
        self.handler(self)
        # img_w, img_h = self.img.get_size()
        # x = self.x - img_w / 2
        # screen.blit(self.img, (x, self.y))

class Raycaster:
    def __init__(
        self, size, mapFile, player, entities=None, fov=90, background="./raycaster/background.png"
    ):
        self.width, self.height = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pygame Raycaster")
        self.clock = pygame.time.Clock()
        self.running = True
        self.pxData = []
        self.player = player
        self.font = pygame.font.SysFont("comicsans", 20)

        if not entities:
            self.entities = []
        else:
            self.entities = entities

        self.fov = fov * math.pi / 180
        self.max_depth = 640
        self.casted_rays = 240
        self.STEPS = 1
        self.DEBUG = False
        self.TOPDOWN = False
        self.DV = (self.width/2) / math.tan(self.fov/2)

        self.mapfile = mapFile
        self.img = Image.open(mapFile)
        self.img = self.img.convert("RGB")
        self.img_height, self.img_width = self.img.size

        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(
            self.background, (self.width, self.height)
        )
        self.gamemap = pygame.image.load(mapFile)

    def loadMap(self):
        for i in range(self.img_width):
            self.pxData.append([])
            for j in range(self.img_height):
                self.pxData[i].append(self.img.getpixel((i, j)))

    def map_coords(self, x, y):
        if x < 0:
            x = x + self.img_width
        if y < 0:
            y = y + self.img_height
        if x > self.img_width - 1:
            x = x - self.img_width
        if y > self.img_height - 1:
            y = y - self.img_height
        return x, y

    def cast_rays(self):
        start_angle = self.player.angle - self.fov / 2
        rays = []

        for ray in range(self.casted_rays):
            for depth in range(int(self.max_depth / self.STEPS)):
                x = self.player.x - math.sin(start_angle) * (depth * self.STEPS)
                y = self.player.y + math.cos(start_angle) * (depth * self.STEPS)
                x, y = self.map_coords(x, y)
                if self.pxData[int(x) % self.img_width][int(y) % self.img_height] != (
                    0,
                    0,
                    0,
                ):
                    break
            depth += 0.0001
            if self.TOPDOWN:
                pygame.draw.line(self.screen, (255, 255, 255), (self.player.x, self.player.y),(x, y))


            start_angle += self.fov / self.casted_rays
            cdep = depth * self.STEPS
            color = list(self.pxData[int(x) % self.img_width][int(y) % self.img_height])
            color_dep = []
            for c in color:
                cc = c / ((1 + cdep * cdep * 0.0001))
                color_dep.append(cc)

            depth = cdep * math.cos(self.player.angle - start_angle)
            wall_height = 21000 / (depth)
            rays.append({"data": [wall_height, color_dep, ray, depth], "type": "wall"})
        # sort rays from shortest to longest
        rays.sort(key=lambda x: x["data"][0])
        return rays

    def load_entities(self):
        for entity in self.entities:
            entity.run(self.screen)
            if self.TOPDOWN:
                pygame.draw.circle(self.screen, (255, 255, 255), (entity.x, entity.y), 5)
                pygame.draw.line(self.screen, (255, 255, 0), (entity.x, entity.y), (self.player.x, self.player.y))

    def top_down_view(self):
        mapfile = pygame.image.load(self.mapfile)
        self.screen.blit(mapfile, (0, 0))
        pygame.draw.circle(self.screen, (255, 255, 255), (self.player.x, self.player.y), 5)


    def load_walls(self, rays):
        SCALE = (self.width) / self.casted_rays
        if not self.TOPDOWN:
            for ray in range(self.casted_rays):
                if rays[ray]["type"] == "wall":
                    wall_height, color_dep, num, depth = rays[ray]["data"]
                pygame.draw.rect(
                    self.screen,
                    tuple(color_dep),
                    (
                        num * SCALE,
                        (self.height / 2) - wall_height / 2,
                        SCALE + 1,
                        wall_height,
                    ),
                )

    def debug_screen(self, rays):
        player_val = f"Player: x: {self.player.x}, y: {self.player.y}, angle: {self.player.angle*180/math.pi%360}"
        fov_val = f"FOV: {self.fov * 180 / math.pi}"
        furthest_wall = f"Furthest wall: {rays[0]['data'][3]}"
        nearest_wall = f"Nearest wall: {rays[-1]['data'][3]}"
        rays_val = f"Rays: {self.casted_rays}"
        fps = f"FPS: {self.clock.get_fps()}"
        self.screen.blit(self.font.render(player_val, True, (255, 255, 255)), (10, 10))
        self.screen.blit(self.font.render(fov_val, True, (255, 255, 255)), (10, 30))
        self.screen.blit(
            self.font.render(furthest_wall, True, (255, 255, 255)), (10, 50)
        )
        self.screen.blit(
            self.font.render(nearest_wall, True, (255, 255, 255)), (10, 70)
        )
        self.screen.blit(self.font.render(rays_val, True, (255, 255, 255)), (10, 90))
        self.screen.blit(self.font.render(fps, True, (255, 255, 255)), (10, 110))

    def run(self):
        prev_time = time.time()
        while self.running:
            pxData = self.pxData

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            now = time.time()
            delta_time = now - prev_time
            prev_time = now

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.angle -= 2 * delta_time
            if keys[pygame.K_d]:
                self.player.angle += 2 * delta_time
            if keys[pygame.K_w]:
                nextX = (
                    self.player.x
                    + -math.sin(self.player.angle) * self.player.speed * delta_time
                )
                nextY = (
                    self.player.y
                    + math.cos(self.player.angle) * self.player.speed * delta_time
                )
                nextX, nextY = self.map_coords(nextX, nextY)

                if pxData[int(nextX) % self.img_width][
                    int(nextY) % self.img_height
                ] == (0, 0, 0):
                    self.player.x = nextX
                    self.player.y = nextY
            if keys[pygame.K_s]:
                nextX = (
                    self.player.x
                    + math.sin(self.player.angle) * self.player.speed * delta_time
                )
                nextY = (
                    self.player.y
                    + -math.cos(self.player.angle) * self.player.speed * delta_time
                )
                nextX, nextY = self.map_coords(nextX, nextY)
                if pxData[int(nextX) % self.img_width][
                    int(nextY) % self.img_height
                ] == (0, 0, 0):
                    self.player.x = nextX
                    self.player.y = nextY
            if keys[pygame.K_ESCAPE]:
                self.TOPDOWN = not self.TOPDOWN
            
            if self.TOPDOWN:
                self.top_down_view()
            rays = self.cast_rays()
            self.load_walls(rays)
            self.load_entities()
            if keys[pygame.K_x]:
                self.DEBUG = not self.DEBUG

            if self.DEBUG:
                self.debug_screen(rays)

            pygame.display.flip()
            self.clock.tick(120)
