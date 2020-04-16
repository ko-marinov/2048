import sys
from collections import namedtuple

import pygame

import game_settings as gs
from board import Board, game_objects


class Grid:
    def __init__(self, rect):
        self.rect = rect

    def draw(self, game, board, surface):
        if game.check_game_over():
            self.draw_text_at_rect_center(
                surface, game.game_over_message, self.rect)
            return
        pygame.draw.rect(surface, gs.SCENE_BACKGROUND_COLOR, self.rect)
        for go in game_objects:
            go.draw(surface)

    def draw_text_at_rect_center(self, surface, text, rect, color=gs.FONT_DEFAULT_COLOR):
        text_surf = gs.FONT.render(text, True, color)
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
    gs.init()

    screen = pygame.display.set_mode(gs.WINDOWS_SIZE)

    # Create grid view
    grid = Grid(pygame.Rect(0, 0, gs.WINDOW_WIDTH, gs.WINDOW_HEIGHT))

    # Set up initial board
    board = Board(*gs.BOARD_CELL_SIZE)
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
        grid.draw(game, board, screen)
        pygame.display.flip()

        pygame.time.delay(gs.FRAME_MS)


if __name__ == "__main__":
    main()
