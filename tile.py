import pygame

import game_settings as gs
from game_object import GameObject
from vec2 import Vec2


class Tile(GameObject):

    def __init__(self, value, row, col, size):
        super().__init__(Vec2(size[0] * col, size[1] * row))
        self.value = value
        self.size = size

    def move_to(self, row, col, duration):
        dest = Vec2(self.size[0] * col, self.size[1] * row)
        self.animate_transition(dest, duration)

    def draw(self, surface):
        rect = pygame.Rect((self.gpos.x, self.gpos.y), self.size)
        pygame.draw.rect(surface, gs.TILE_COLORS[self.value], rect)
        text_surf = gs.FONT.render(
            str(self.value), True, gs.FONT_DEFAULT_COLOR)
        text_pos_x = rect.center[0] - text_surf.get_rect().center[0]
        text_pos_y = rect.center[1] - text_surf.get_rect().center[1]
        surface.blit(text_surf, [text_pos_x, text_pos_y])
