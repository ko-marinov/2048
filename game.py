import sys

from collections import namedtuple

import pygame

Size = namedtuple('Size', ['w', 'h'])
Point = namedtuple('Point', ['x', 'y'])

class Grid:
    def __init__(self, rect, bg_color, border_color):
        self.rect = rect
        self.bg_color = bg_color
        self.border_color = border_color
        self.size = Size(4, 4)

    def draw(self, surface):
        border_width = min(self.rect.width, self.rect.height) * 0.05
        pygame.draw.rect(surface, self.bg_color, self.rect)#, int(border_width))
        cell_size = Size(self.rect.width // 4, self.rect.height // 4)
        for i in range(self.size.w):
            for j in range(self.size.h):
                pos = Point(i * cell_size.w, j * cell_size.h)
                pygame.draw.rect(surface, self.border_color, pygame.Rect(pos, cell_size), 4)



class Tile:
    def __init__(self, value):
        self.value = value


class Board:
    def __init__(self, rows, cols):
        self.m = [[Tile(0) for c in range(cols)] for r in range(rows)]

    '''
    Algorithm:
    1. Take line
    2. Collapse
    3. Replace line with collapsed one
    '''

    def left(self):
        # <--
        pass

    def right(self):
        pass

    def top(self):
        pass

    def bottom(self):
        pass

    def collapse(self, line):
        # [0, 2, 2, 4] -> [2, 0, 2, 4] -> [4, 0, 0, 4] -> [4, 4, 0, 0]
        # [2, 4, 4, 2] -> [2, 4, 4, 2] -> [2, 8, 0, 2] -> [2, 8, 2, 0]

        target_cell = 0
        for i in range(1, len(line)):
            if line[i].value:
                if line[target_cell].value == 0:
                    line[target_cell].value, line[i].value = line[i].value, line[target_cell].value
                elif line[target_cell].value == line[i].value:
                    line[target_cell].value *= 2
                    line[i].value = 0
                    target_cell += 1
                else:
                    target_cell += 1
                    if i != target_cell:
                        line[target_cell].value, line[i].value = line[i].value, line[target_cell].value
        return line


def main():
    pygame.init()

    size = width, height = 400, 400
    speed = [2, 2]
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    bg_color = pygame.color.THECOLORS['gray60']
    border_color = pygame.color.THECOLORS['gray17']
    grid = Grid(pygame.Rect(0, 0, width, height), bg_color, border_color)

    while 1:
        # User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q: sys.exit()

        # Physics

        # Render
        screen.fill(black)
        grid.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()