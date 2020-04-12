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

    def draw(self, game, board, surface):
        if game.check_game_over():
            text = self.font.render("GAME OVER", True, (255, 255, 255))
            surface.blit(text, [self.rect.width // 2, self.rect.height // 2])
            return
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


class Game:
    def __init__(self, board):
        self.board = board
        self.is_game_over = False

    def handle_input(self, event):
        board = self.board
        prev_state = board.get_state()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            board.left()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            board.right()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            board.up()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            board.down()
        if not board.check_state(prev_state):
            board.spawn()

    def check_game_over(self):
        if self.is_game_over:
            return True
        self.is_game_over = self.board.is_deadend()
        if self.is_game_over:
            print("[ GAME OVER ]\n", self.board)
        return self.is_game_over


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

    # Init game
    game = Game(board)

    # Disable repeat
    pygame.key.set_repeat(0)

    while 1:
        # User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                sys.exit()
            game.handle_input(event)

        # Game logic

        # Render
        screen.fill(black)
        grid.draw(game, board, screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
