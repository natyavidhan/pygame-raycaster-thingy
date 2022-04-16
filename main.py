import pygame
from PIL import Image

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

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for i in gameMap:
        pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], 8, 8))
    pygame.display.flip()
    clock.tick(60)

