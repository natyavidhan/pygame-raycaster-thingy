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

    def load_map(self, map_file):
        img = Image.open(map_file)
        img = img.convert("RGBA")
        self.map = list(img.getdata())
        self.map_img = pygame.image.load(map_file)

    def update(self):
        self.screen.blit(self.background, (0, 0))
        if self.map_img:
            self.screen.blit(self.map_img, (0, 0))
        pygame.draw.circle(self.screen, (255, 0, 0), self.player.pos, 5)
        # draw a line facing the player
        pygame.draw.line(self.screen, (255, 0, 0), self.player.pos, (self.player.pos[0] + 100 * math.sin(math.radians(self.player.angle)), self.player.pos[1] + 100 * math.cos(math.radians(self.player.angle))))