import pygame, math
from PIL import Image

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1500, 640))
pygame.display.set_caption("Pygame Raycaster")
clock = pygame.time.Clock()
running = True
TILESIZE = 32

pxData = []
gameMap = []
img = Image.open("map.png")
for i in range(20):
    gameMap.append([])
    for j in range(20):
        gameMap[i].append(0 if img.getpixel((i, j)) == (0, 0, 0, 255) else 1)

img = img.resize((img.size[0] * TILESIZE, img.size[1] * TILESIZE))
for i in range(640):
    pxData.append([])
    for j in range(640):
        pxData[i].append(0 if img.getpixel((i, j)) == (0, 0, 0, 255) else 1)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = math.pi
        self.speed = 2
        self.fov = math.pi / 3
        self.max_depth = 1000
        self.casted_rays = 120
    
    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), 
                        (self.x - math.sin(self.angle) * 50,
                        self.y + math.cos(self.angle) * 50), 1)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 15)
        # draw the field of view
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y),
                        (self.x - math.sin(self.angle + self.fov/2) * 50,
                        self.y + math.cos(self.angle + self.fov/2) * 50), 1)
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y),
                        (self.x - math.sin(self.angle - self.fov/2) * 50,
                        self.y + math.cos(self.angle - self.fov/2) * 50), 1)
    
    def cast_rays(self):
        for i in range(self.casted_rays):
            angle = self.angle - self.fov / 2 + self.fov / self.casted_rays * i
            ray_x = self.x
            ray_y = self.y
            ray_length = 0
            while ray_length < self.max_depth:
                # print(ray_x, ray_y)
                ray_x += -math.sin(angle)
                ray_y += math.cos(angle)
                ray_length += 1
                if pxData[int(ray_x)][int(ray_y)] == 1:
                    break
            pygame.draw.line(screen, (0, 0, 255), (self.x, self.y),
                            (ray_x, ray_y), 1)



player = Player(320, 240)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    
    x, y = 0, 0
    for _y in gameMap:
        for _x in _y:
            if _x == 1:
                pygame.draw.rect(screen, (185, 185, 185), (x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE))
            x += 1
        x = 0
        y += 1

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.angle -= 0.05
    if keys[pygame.K_d]:
        player.angle += 0.05
    if keys[pygame.K_w]:
        nextX = player.x + -math.sin(player.angle) * player.speed
        nextY = player.y + math.cos(player.angle) * player.speed
        if nextY > 20 and nextY < 610 and nextX > 20 and nextX < 610:
            player.x = nextX
            player.y = nextY
    if keys[pygame.K_s]:
        nextX = player.x + math.sin(player.angle) * player.speed
        nextY = player.y + -math.cos(player.angle) * player.speed
        if player.y > 20 and player.y < 610 and player.x > 20 and player.x < 610:
            player.x = nextX
            player.y = nextY
    
    fps = f"FPS: {round(clock.get_fps())}"
    screen.blit(pygame.font.SysFont("comicsans", 16).render(str(fps), True, (255, 255, 255)), (0, 0))
    
    player.draw()
    player.cast_rays()

    pygame.display.flip()
    clock.tick(60)

