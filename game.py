import sys
from collections import namedtuple

import pygame

import game_settings as gs
from board import Board
from game_object import game_objects


class Grid:
    def __init__(self, rect):
        self.rect = rect

    def draw(self, game, surface):
        pygame.draw.rect(surface, gs.SCENE_BACKGROUND_COLOR, self.rect)
        for go in game_objects:
            go.draw(surface)
        if game.check_game_over():
            self.draw_game_over_message(
                surface, game.game_over_message, self.rect)

    def draw_game_over_message(self, surface, text, rect, color=gs.FONT_DEFAULT_COLOR):
        block_w, block_h = 240, 80
        block_x = rect.center[0] - block_w / 2
        block_y = rect.center[1] - block_h / 2
        pygame.draw.rect(surface, gs.HUD_DEFAULT_COLOR,
                         pygame.Rect(block_x, block_y, block_w, block_h))
        text_surf = gs.FONT_LARGE.render(text, True, color)
        text_pos_x = rect.center[0] - text_surf.get_rect().center[0]
        text_pos_y = rect.center[1] - text_surf.get_rect().center[1]
        surface.blit(text_surf, [text_pos_x, text_pos_y])


class Game:
    def start(self):
        self.is_game_over = False
        self.game_over_message = ""
        self.board = Board(*gs.BOARD_CELL_SIZE)
        self.board.spawn_random()
        self.board.spawn_random()

    def restart(self):
        self.save_high_score()
        for go in game_objects:
            go.destroy()
        self.start()

    def finish(self):
        self.save_high_score()

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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.is_game_over:
            self.restart()

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

    def save_high_score(self):
        self.board.scorer.save_high_score()


def is_exit_event(event):
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
        return True
    return False


def main():
    pygame.init()
    gs.init()

    screen = pygame.display.set_mode(gs.WINDOWS_SIZE)

    # Create grid view
    grid = Grid(pygame.Rect(0, 0, gs.WINDOW_WIDTH, gs.WINDOW_HEIGHT))

    # Init game
    game = Game()
    game.start()

    # Disable repeat
    pygame.key.set_repeat(0)

    ticks = pygame.time.get_ticks()
    while 1:
        # User input
        for event in pygame.event.get():
            if is_exit_event(event):
                game.finish()
                sys.exit()
            game.handle_input(event)

        # Game logic
        last_ticks = ticks
        ticks = pygame.time.get_ticks()
        dtime = ticks - last_ticks
        for go in game_objects:
            go.update(dtime)

        # Render
        grid.draw(game, screen)
        pygame.display.flip()

        pygame.time.delay(gs.FRAME_MS)


if __name__ == "__main__":
    main()
