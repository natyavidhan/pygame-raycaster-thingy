import pygame, math
from PIL import Image

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame Raycaster")
clock = pygame.time.Clock()
running = True
gameMap = []

mapimg = Image.open("map.png")
img_width, img_height = mapimg.size
for y in range(img_height):
    _y = y * 8
    for x in range(img_width):
        _x = x * 8
        val = mapimg.getpixel((x, y))
        if val == 0:
            gameMap.append([_x, _y])

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = math.pi
        self.speed = 3
        self.fov = math.pi / 3
    
    def draw(self):
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), 
                        (self.x - math.sin(self.angle) * 50,
                        self.y + math.cos(self.angle) * 50), 1)
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), 8)
        # draw the field of view
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y),
                        (self.x - math.sin(self.angle + self.fov) * 50,
                        self.y + math.cos(self.angle + self.fov) * 50), 1)
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y),
                        (self.x - math.sin(self.angle - self.fov) * 50,
                        self.y + math.cos(self.angle - self.fov) * 50), 1)

player = Player(320, 240)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for i in gameMap:
        pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], 8, 8))
    

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.angle -= 0.1
    if keys[pygame.K_d]:
        player.angle += 0.1
    if keys[pygame.K_w]:
        player.x += -math.sin(player.angle) * player.speed
        player.y += math.cos(player.angle) * player.speed
    if keys[pygame.K_s]:
        player.x += math.sin(player.angle) * player.speed
        player.y += -math.cos(player.angle) * player.speed
    
    fps = f"FPS: {round(clock.get_fps())}"
    screen.blit(pygame.font.SysFont("comicsans", 16).render(str(fps), True, (255, 255, 255)), (0, 0))
    
    player.draw()

    pygame.display.flip()
    clock.tick(60)

