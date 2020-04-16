import sys
from collections import namedtuple

import pygame

from board import Board, game_objects


class Grid:
    def __init__(self, rect):
        self.rect = rect
        self.size = (4, 4)
        self.font = pygame.font.SysFont(None, 20)

    def draw(self, game, board, surface):
        if game.check_game_over():
            self.draw_text_at_rect_center(
                surface, game.game_over_message, self.rect)
            return
        pygame.draw.rect(surface, (200, 200, 200), self.rect)
        for go in game_objects:
            go.draw(surface, self.font)

    def draw_text_at_rect_center(self, surface, text, rect, color=(255, 255, 255)):
        text_surf = self.font.render(text, True, color)
        text_pos_x = rect.center[0] - text_surf.get_rect().center[0]
        text_pos_y = rect.center[1] - text_surf.get_rect().center[1]
        surface.blit(text_surf, [text_pos_x, text_pos_y])


class Game:
    def __init__(self, board):
        self.board = board
        self.is_game_over = False
        self.game_over_message = ""

    def handle_input(self, event):
        board = self.board
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            board.move(Board.LEFT)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            board.move(Board.RIGHT)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            board.move(Board.UP)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            board.move(Board.DOWN)

    def check_game_over(self):
        if self.is_game_over:
            return True
        if self.board.is_deadend():
            self.game_over_message = "GAME OVER"
            self.is_game_over = True
            print("[ GAME OVER ]\n", self.board)
        if self.board.is_complete():
            self.game_over_message = "CONGRATULATIONS! YOU GET 2048!"
            self.is_game_over = True
            print("[ SUCCESS: 2048 ]\n", self.board)
        return self.is_game_over


def main():
    pygame.init()

    size = width, height = 400, 400
    black = 0, 0, 0
    frames_per_second = 60
    frame_delay_ms = 1000 // frames_per_second

    screen = pygame.display.set_mode(size)

    # Create grid view
    grid = Grid(pygame.Rect(0, 0, width, height))

    # Set up initial board
    board = Board(4, 4)
    board.spawn_random()
    board.spawn_random()

    # Init game
    game = Game(board)

    # Disable repeat
    pygame.key.set_repeat(0)

    ticks = pygame.time.get_ticks()
    while 1:
        # User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                sys.exit()
            game.handle_input(event)

        # Game logic
        last_ticks = ticks
        ticks = pygame.time.get_ticks()
        dtime = ticks - last_ticks
        for go in game_objects:
            go.update(dtime)

        # Render
        screen.fill(black)
        grid.draw(game, board, screen)
        pygame.display.flip()

        pygame.time.delay(frame_delay_ms)


if __name__ == "__main__":
    main()
