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
        self._parent_rect = None

    def register(self):
        gui_elements.append(self)

    def destroy(self):
        gui_elements.remove(self)

    @property
    def parent_rect(self):
        if self._parent_rect is None:
            return pygame.Rect((0, 0), gs.WINDOWS_SIZE)
        return self._parent_rect

    @parent_rect.setter
    def parent_rect(self, rect):
        self._parent_rect = rect

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
        h_padding = 25
        v_padding = 15
        rect_w = total_w + 2 * h_padding
        rect_h = total_h - line_gap + 2 * v_padding
        rect_x = self.parent_rect.x + (self.parent_rect.w - rect_w) // 2
        rect_y = self.parent_rect.y + (self.parent_rect.h - rect_h) // 2
        block = pygame.Surface((rect_w, rect_h), pygame.SRCALPHA)
        block.fill(gs.HUD_DEFAULT_COLOR)
        surface.blit(block, (rect_x, rect_y))

        # draw lines
        text_y = rect_y + v_padding
        for text in text_surfs:
            text_x = rect_x + (rect_w - text.get_rect().w) // 2
            surface.blit(text, (text_x, text_y))
            text_y += text.get_rect().h + line_gap
