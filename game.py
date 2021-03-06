import sys
from enum import Enum

import pygame

import game_settings as gs
from board import Board
from game_object import game_objects
from gui import gui_elements, MessageBox


GameState = Enum("GameState", "PLAY LOSE WIN PLAYAFTERWIN")


class Game:
    def start(self):
        self.active_message_box = None
        self.board = Board(*gs.BOARD_CELL_SIZE)
        self.board.spawn_random()
        self.board.spawn_random()
        self.state = GameState.PLAY

    def restart(self):
        self.close_active_message()
        self.save_high_score()
        for go in game_objects:
            go.destroy()
        for gui in gui_elements:
            gui.destroy()
        self.start()

    def continue_game(self):
        self.close_active_message()
        self.state = GameState.PLAYAFTERWIN

    def finish(self):
        self.save_high_score()

    def update(self, dtime):
        self.update_state()
        for go in game_objects:
            go.update(dtime)

    def close_active_message(self):
        self.active_message_box.destroy()
        self.active_message_box = None

    def handle_input(self, event):
        if self.state == GameState.PLAY or self.state == GameState.PLAYAFTERWIN:
            board = self.board
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                board.move(Board.LEFT)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                board.move(Board.RIGHT)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                board.move(Board.UP)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                board.move(Board.DOWN)
        elif self.state == GameState.LOSE:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.restart()
        elif self.state == GameState.WIN:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.continue_game()

    def update_state(self):
        if self.state != GameState.LOSE and self.board.is_deadend():
            self.active_message_box = MessageBox("GAME OVER")
            self.active_message_box.parent_rect = self.board.get_rect()
            self.state = GameState.LOSE
        if self.state == GameState.PLAY and self.board.is_complete():
            self.active_message_box = MessageBox(
                "CONGRATS!\nYOU GET 2048!")
            self.active_message_box.parent_rect = self.board.get_rect()
            self.state = GameState.WIN

    def save_high_score(self):
        self.board.scorer.save_high_score()


def is_exit_event(event):
    if event.type == pygame.QUIT:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
        return True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_F4 and event.mod & pygame.KMOD_ALT:
        return True
    return False


def render_all(surface):
    surface.fill(gs.SCENE_BACKGROUND_COLOR)
    for go in game_objects:
        go.draw(surface)
    for gui in gui_elements:
        gui.draw(surface)


def main():
    pygame.init()
    gs.init()

    screen = pygame.display.set_mode(gs.WINDOWS_SIZE)

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
        game.update(dtime)

        # Render
        render_all(screen)
        pygame.display.flip()

        pygame.time.delay(gs.FRAME_MS)


if __name__ == "__main__":
    main()
