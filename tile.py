from os import listdir
from os.path import isfile, join

import pygame

import game_settings as gs
from game_object import GameObject
from vec2 import Vec2


class TileFactory:

    TILE_IMAGES = {}

    def load_tile_images(self):
        path = "data/images"
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        for f in onlyfiles:
            key = f.split(".")[0]
            TileFactory.TILE_IMAGES[key] = pygame.image.load(join(path, f))

    def __init__(self, tile_parent=None):
        self.tile_parent = tile_parent
        if not TileFactory.TILE_IMAGES:
            self.load_tile_images()

    def create(self, value, row, col):
        tile = Tile(value, row, col, gs.TILE_SIZE)
        tile.parent = self.tile_parent
        tile.image = TileFactory.TILE_IMAGES[str(value)]
        return tile


class Tile(GameObject):

    def __init__(self, value, row, col, size):
        super().__init__(Vec2(size[0] * col, size[1] * row))
        self.value = value
        self.size = Vec2(size)
        self.image = None

    def move_to(self, row, col, duration):
        dest = Vec2(self.size.x * col, self.size.y * row)
        self.animate_transition(dest, duration)

    def draw(self, surface):
        image_size = Vec2(self.image.get_size())
        dest = self.gpos + (self.size - image_size) / 2
        surface.blit(self.image, (dest.x, dest.y))
