import pygame

import game_settings as gs
from game_object import GameObject, game_objects
from vec2 import Vec2


class Scorer(GameObject):
    def __init__(self, pos=Vec2(0, 0)):
        super().__init__(pos)
        self.score = 0
        self.size = (gs.WINDOW_WIDTH - 20, 80)

    def add(self, points):
        assert points >= 0
        self.score += points

    def draw(self, surface):
        rect = pygame.Rect(self.pos.x, self.pos.y, self.size[0], self.size[1])
        pygame.draw.rect(surface, gs.HUD_DEFAULT_COLOR, rect)
        text_surf = gs.FONT.render(
            str(self.score), True, gs.FONT_DEFAULT_COLOR)
        text_pos_x = rect.center[0] - text_surf.get_rect().center[0]
        text_pos_y = rect.center[1] - text_surf.get_rect().center[1]
        surface.blit(text_surf, [text_pos_x, text_pos_y])
