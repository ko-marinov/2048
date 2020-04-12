import sys
from collections import namedtuple

import pygame

from board import Board

Size = namedtuple('Size', ['w', 'h'])
Point = namedtuple('Point', ['x', 'y'])


class Grid:
    def __init__(self, rect, bg_color, border_color):
        self.rect = rect
        self.bg_color = bg_color
        self.border_color = border_color
        self.size = Size(4, 4)
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, board, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        cell_size = Size(self.rect.width // 4, self.rect.height // 4)
        for row in range(self.size.h):
            for col in range(self.size.w):
                pos = Point(row * cell_size.h, col * cell_size.w)
                pygame.draw.rect(surface, self.border_color,
                                 pygame.Rect(pos, cell_size), 4)
                text = self.font.render(
                    str(board.m[row][col]), True, pygame.color.THECOLORS["white"])
                surface.blit(text, [50 + col*100, 50 + row*100])


def main():
    pygame.init()

    size = width, height = 400, 400
    black = 0, 0, 0

    screen = pygame.display.set_mode(size)

    # Create grid view
    bg_color = pygame.color.THECOLORS['gray60']
    border_color = pygame.color.THECOLORS['gray17']
    grid = Grid(pygame.Rect(0, 0, width, height), bg_color, border_color)

    # Set up initial board
    board = Board(4, 4)
    board.spawn()
    board.spawn()

    # Disable repeat
    pygame.key.set_repeat(0)

    while 1:
        # User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                board.left()
                board.spawn()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                board.right()
                board.spawn()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                board.up()
                board.spawn()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                board.down()
                board.spawn()

        # Game logic

        # Render
        screen.fill(black)
        grid.draw(board, screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
