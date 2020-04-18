import os

import pygame

import game_settings as gs
from game_object import GameObject, game_objects
from vec2 import Vec2


class Scorer(GameObject):
    def __init__(self, pos=Vec2(0, 0)):
        super().__init__(pos)
        self.score = 0
        self.high_score = 0
        self.size = (gs.WINDOW_WIDTH - 20, 80)
        self.load_high_score()

    def add(self, points):
        assert points >= 0
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score

    def load_high_score(self):
        filename = "data/data"
        if not os.path.isfile(filename):
            return
        with open(filename) as f:
            self.high_score = int(f.read())

    def save_high_score(self):
        with open("data/data", "w") as f:
            f.write(str(self.high_score))

    def draw(self, surface):
        # score block
        block_w = self.size[0] / 2 - 5
        rect = pygame.Rect(self.pos.x, self.pos.y, block_w, self.size[1])
        self.draw_block(surface, rect, self.score, "SCORE")

        # high score block
        block_x = self.pos.x + block_w + 10
        rect = pygame.Rect(block_x, self.pos.y, block_w, self.size[1])
        self.draw_block(surface, rect, self.high_score, "HIGH SCORE")

    def draw_block(self, surface, rect, value, text):
        pygame.draw.rect(surface, gs.HUD_DEFAULT_COLOR, rect)
        text_surf = gs.FONT_LARGE.render(
            str(value), True, gs.FONT_DEFAULT_COLOR)
        text_pos_x = rect.center[0] - text_surf.get_rect().center[0]
        text_pos_y = rect.center[1] - text_surf.get_rect().h * 0.65
        surface.blit(text_surf, [text_pos_x, text_pos_y])
        text_surf = gs.FONT_SMALL.render(
            str(text), True, gs.FONT_DEFAULT_COLOR)
        text_pos_x = rect.center[0] - text_surf.get_rect().center[0]
        text_pos_y = rect.center[1] + text_surf.get_rect().h * 0.8
        surface.blit(text_surf, [text_pos_x, text_pos_y])
