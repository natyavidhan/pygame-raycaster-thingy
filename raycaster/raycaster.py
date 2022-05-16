import pygame, math
from PIL import Image
from numpy import interp

pygame.init()
pygame.font.init()


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 315 * math.pi / 180
        self.speed = 3

class Raycaster:
    def __init__(self, size, mapFile, player, fov=90, background="./raycaster/background.png"):
        self.width, self.height = size
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Pygame Raycaster")
        self.clock = pygame.time.Clock()
        self.running = True
        self.pxData = []
        self.player = player

        self.fov = fov * math.pi / 180
        self.max_depth = 640
        self.casted_rays = 240
        self.STEPS = 1

        self.img = Image.open(mapFile)
        self.img = self.img.convert("RGB")
        self.img_height, self.img_width = self.img.size

        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
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
        if x > self.img_width-1:
            x = x - self.img_width
        if y > self.img_height-1:
            y = y - self.img_height
        return x, y

    def cast_rays(self):
        start_angle = self.player.angle - self.fov / 2
        rays = []
        SCALE = (self.width) / self.casted_rays

        for ray in range(self.casted_rays):
            for depth in range(int(self.max_depth / self.STEPS)):
                x = self.player.x - math.sin(start_angle) * (depth * self.STEPS)
                y = self.player.y + math.cos(start_angle) * (depth * self.STEPS)
                x, y = self.map_coords(x, y)
                if self.pxData[int(x)%self.img_width][int(y)%self.img_height] != (0, 0, 0):
                    break
            depth += 0.0001
            
            start_angle += self.fov / self.casted_rays
            cdep = depth * self.STEPS
            color = list(self.pxData[int(x)%self.img_width][int(y)%self.img_height])
            color_dep = []
            for c in color:
                cc = c / ((1 + cdep * cdep * 0.0001))
                color_dep.append(cc)

            depth *= math.cos(self.player.angle - start_angle)
            wall_height = 21000 / (depth)

            pygame.draw.rect(
                self.screen,
                tuple(color_dep),
                (
                    ray * SCALE,
                    (self.height / 2) - wall_height / 2,
                    SCALE + 1,
                    wall_height,
                ),
            )


    def run(self):
        while self.running:
            pxData = self.pxData

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            delta_time = self.clock.tick(120) / 10 + 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.player.angle -= 0.05 * delta_time
            if keys[pygame.K_d]:
                self.player.angle += 0.05 * delta_time
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

                if pxData[int(nextX)%self.img_width][int(nextY)%self.img_height] == (0, 0, 0):
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
                if pxData[int(nextX)%self.img_width][int(nextY)%self.img_height] ==  (0, 0, 0):
                    self.player.x = nextX
                    self.player.y = nextY


            self.cast_rays()

            fps = f"FPS: {round(self.clock.get_fps())}"
            self.screen.blit(
                pygame.font.SysFont("comicsans", 16).render(
                    str(fps), True, (255, 255, 255)
                ),
                (0, 0),
            )

            pygame.display.flip()
            self.clock.tick(120)
