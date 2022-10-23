import pygame
from PIL import Image

class Raycaster:
    def __init__(self, size, player, entities=None, fov=90, background="./assets/back.png"):
        self.screen = pygame.display.set_mode(size)
        self.background = pygame.image.load(background)
        self.background = pygame.transform.scale(self.background, size)
        self.map = []

    def load_map(self, map_file):
        img = Image.open(map_file)
        img = img.convert("RGBA")
        self.map = list(img.getdata())
        print(self.map)

    def update(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.update()
