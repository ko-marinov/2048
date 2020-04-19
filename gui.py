import pygame

from game_object import GameObject
import game_settings as gs
from vec2 import Vec2

gui_elements = []


class GuiBase(GameObject):
    def __init__(self, pos=Vec2(0, 0), size=Vec2(100, 100), visible=True):
        super().__init__(pos)
        self.size = size
        self.visible = visible

    def register(self):
        gui_elements.append(self)

    def destroy(self):
        gui_elements.remove(self)

    def draw(self, surface):
        if self.visible:
            self.draw_gui(surface)

    def draw_gui(self, surface):
        pass


class MessageBox(GuiBase):
    def __init__(self, message):
        super().__init__()
        self.lines = message.split("\n")

    def draw_gui(self, surface):
        text_surfs = []
        total_h = 0
        total_w = 0
        line_gap = 3
        for line in self.lines:
            text = gs.FONT_LARGE.render(
                line, True, gs.FONT_DEFAULT_COLOR)
            total_h += text.get_rect().h + line_gap
            total_w = max(total_w, text.get_rect().w)
            text_surfs.append(text)

        # message block
        padding = 10
        rect_w = total_w + 2 * padding
        rect_h = total_h - line_gap + 2 * padding
        rect_x = (gs.WINDOW_WIDTH - rect_w) // 2
        rect_y = (gs.WINDOW_HEIGHT - rect_h) // 2
        rect = pygame.Rect(rect_x, rect_y, rect_w, rect_h)
        pygame.draw.rect(surface, gs.HUD_DEFAULT_COLOR, rect)

        # draw lines
        text_y = rect_y + padding
        for text in text_surfs:
            text_x = rect_x + (rect_w - text.get_rect().w) // 2
            surface.blit(text, (text_x, text_y))
            text_y += text.get_rect().h + line_gap
