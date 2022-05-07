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

    def draw(self, screen):
        pygame.draw.line(
            screen,
            (255, 255, 255),
            (self.x, self.y),
            (self.x - math.sin(self.angle) * 50, self.y + math.cos(self.angle) * 50),
            1,
        )
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 15)


class Raycaster:
    def __init__(self, mapFile, player, fov=90):
        self.screen = pygame.display.set_mode((1280, 640))
        pygame.display.set_caption("Pygame Raycaster")
        self.clock = pygame.time.Clock()
        self.running = True
        self.TILESIZE = 32
        self.pxData = []
        self.gameMap = []
        self.player = player

        self.fov = fov * math.pi / 180
        self.max_depth = 640
        self.casted_rays = 120
        self.STEPS = 1

        self.img = Image.open(mapFile)
        self.large_img = Image.new("RGBA", (640, 640), (0, 0, 0, 255))
        self.background = pygame.image.load("background.png")

    def loadMap(self):
        for i in range(20):
            self.gameMap.append([])
            for j in range(20):
                self.gameMap[i].append(
                    0 if self.img.getpixel((i, j)) == (0, 0, 0, 255) else 1
                )
                for k in range(self.TILESIZE):
                    for l in range(self.TILESIZE):
                        self.large_img.putpixel(
                            (i * self.TILESIZE + k, j * self.TILESIZE + l),
                            self.img.getpixel((i, j)),
                        )

        for i in range(640):
            self.pxData.append([])
            for j in range(640):
                self.pxData[i].append(
                    1 if self.large_img.getpixel((i, j)) == (255, 255, 255, 255) else 0
                )

    def cast_rays(self):
        start_angle = self.player.angle - self.fov / 2
        rays = []
        SCALE = (640) / self.casted_rays
        for ray in range(self.casted_rays):
            for depth in range(int(self.max_depth / self.STEPS)):
                x = self.player.x - math.sin(start_angle) * (depth * self.STEPS)
                y = self.player.y + math.cos(start_angle) * (depth * self.STEPS)
                if self.pxData[int(x)][int(y)] == 1:
                    break
            depth += 0.0001  # to prevent division by zero
            pygame.draw.line(
                self.screen, (255, 0, 0), (self.player.x, self.player.y), (x, y), 1
            )
            start_angle += self.fov / self.casted_rays
            cdep = depth * self.STEPS
            color = 255 / ((1 + cdep * cdep * 0.0001))

            depth *= math.cos(self.player.angle - start_angle)
            wall_height = 21000 / (depth)  # * self.STEPS)

            pygame.draw.rect(
                self.screen,
                (color, color, color),
                (
                    640 + ray * SCALE,
                    (640 / 2) - wall_height / 2,
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
            self.screen.blit(self.background, (640, 0))

            x, y = 0, 0
            for _y in self.gameMap:
                for _x in _y:
                    if _x == 1:
                        pygame.draw.rect(
                            self.screen,
                            (185, 185, 185),
                            (
                                y * self.TILESIZE,
                                x * self.TILESIZE,
                                self.TILESIZE,
                                self.TILESIZE,
                            ),
                        )
                    x += 1
                x = 0
                y += 1

            delta_time = interp(self.clock.get_fps(), [0, 120], [2, 0.5])

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
                if pxData[int(nextX)][int(nextY)] == 0:
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
                if pxData[int(nextX)][int(nextY)] == 0:
                    self.player.x = nextX
                    self.player.y = nextY

            fps = f"FPS: {round(self.clock.get_fps())}"
            self.screen.blit(
                pygame.font.SysFont("comicsans", 16).render(
                    str(fps), True, (255, 255, 255)
                ),
                (0, 0),
            )

            self.player.draw(self.screen)
            pygame.draw.line(self.screen, (0, 0, 0), (639, 0), (639, 640), 3)
            self.cast_rays()

            pygame.display.flip()
            self.clock.tick(120)
