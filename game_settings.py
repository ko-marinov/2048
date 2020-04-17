import pygame


# window size
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
WINDOWS_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# board size
BOARD_WIDTH = 400
BOARD_HEIGHT = 400
BOARD_SIZE = (BOARD_WIDTH, BOARD_HEIGHT)
BOARD_CELL_SIZE = (4, 4)

# tile size
TILE_WIDTH = BOARD_WIDTH // BOARD_CELL_SIZE[0]
TILE_HEIGHT = BOARD_HEIGHT // BOARD_CELL_SIZE[1]
TILE_SIZE = (TILE_WIDTH, TILE_HEIGHT)

# time
FPS = 60
FRAME_MS = 1000 // FPS

# colors
SCENE_BACKGROUND_COLOR = (200, 200, 200)
TILE_COLORS = {
    0: (128, 128, 128),
    2: (128, 0, 0),
    4: (0, 128, 0),
    8: (0, 0, 128),
    16: (128, 0, 128),
    32: (128, 128, 0),
    64: (0, 128, 128),
    128: (128, 255, 0),
    256: (128, 0, 255),
    512: (0, 128, 255),
    1024: (255, 128, 0),
    2048: (255, 0, 128),
    4096: (0, 255, 128),
    9192: (0, 0, 0)
}

# fonst
FONT = None
FONT_DEFAULT_COLOR = (255, 255, 255)
FONT_NAME = "data/fonts/Roboto-Medium.ttf"
FONT_SIZE = 32


def init():
    # GameSettings.BOARD_SIZE = (
    #    GameSettings.BOARD_WIDTH, GameSettings.BOARD_HEIGHT)

    # GameSettings.TILE_SIZE = (
    #    GameSettings.TILE_WIDTH, GameSettings.TILE_HEIGHT)

    #GameSettings.FRAME_DURATION = 1000 // GameSettings.FPS

    global FONT
    FONT = pygame.font.Font(FONT_NAME, FONT_SIZE)
