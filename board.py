import itertools
import random

import pygame

import game_settings as gs
from game_object import GameObject
from vec2 import Vec2
from tile import Tile


class Board(GameObject):

    # Directions
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

    TILE_MOVE_DURATION_MS = 100

    def __init__(self, rows, cols, iterable=None):
        super().__init__((0, 0))
        self.rows = rows
        self.cols = cols
        self.m = [[0 for c in range(cols)] for r in range(rows)]
        self.tiles = [[None for c in range(cols)] for r in range(rows)]
        self.tiles_to_destroy = []
        self.tiles_to_spawn = []
        self.should_wait_for_move_finished = False

        if iterable != None:
            for n, (i, j) in enumerate(itertools.product(range(self.rows), range(self.cols))):
                val = iterable[n]
                if val:
                    self.m[i][j] = val
                    self.tiles[i][j] = Tile(val, i, j, gs.TILE_SIZE)
                    self.tiles[i][j].parent = self

    def val_spawner(self):
        return 2 * random.randint(1, 2)

    def pos_selector(self, select_from):
        return select_from[random.randint(0, len(select_from) - 1)]

    def __repr__(self):
        s = "Board:\n"
        for i in range(self.rows):
            for j in range(self.cols):
                s += f"{self.m[i][j]}, "
            s += "\n"
        return s

    def get_state(self):
        return list([self.m[i][j] for i, j in itertools.product(range(self.rows), range(self.cols))])

    def check_state(self, state):
        cur_state = self.get_state()
        for i in range(len(cur_state)):
            if cur_state[i] != state[i]:
                return False
        return True

    def is_deadend(self):
        m = self.m

        # check empty cells
        for i, j in itertools.product(range(self.rows), range(self.cols)):
            if m[i][j] == 0:
                return False

        # check adjacent cells
        for i, j in itertools.product(range(self.rows), range(self.cols - 1)):
            if m[i][j] == m[i][j+1]:
                return False
        for i, j in itertools.product(range(self.rows - 1), range(self.cols)):
            if m[i][j] == m[i+1][j]:
                return False
        return True

    def is_complete(self):
        for i, j in itertools.product(range(self.rows), range(self.cols)):
            if self.m[i][j] == 2048:
                return True
        return False

    def spawn(self, value, row, col):
        self.m[row][col] = value
        self.tiles[row][col] = Tile(value, row, col, gs.TILE_SIZE)
        self.tiles[row][col].parent = self

    def spawn_random(self, val_spawner=None, pos_selector=None):
        if val_spawner is None:
            val_spawner = self.val_spawner
        if pos_selector is None:
            pos_selector = self.pos_selector
        empty_cells = []
        for i, j in itertools.product(range(self.rows), range(self.cols)):
            if self.m[i][j] == 0:
                empty_cells.append((i, j))
        assert empty_cells
        row, col = pos_selector(empty_cells)
        self.spawn(val_spawner(), row, col)

    def delayed_call(self, duration, call):
        time_left = duration

        def delayed_call_process(dtime):
            nonlocal time_left
            time_left -= dtime
            if time_left <= 0:
                call()
                return "DONE"
            return "INPROGRESS"

        GameObject.next_proc_id += 1
        self.processes[GameObject.next_proc_id] = delayed_call_process

    def handle_post_move(self):
        for tile in self.tiles_to_destroy:
            tile.destroy()
        self.tiles_to_destroy.clear()
        for val, row, col in self.tiles_to_spawn:
            self.spawn(val, row, col)
        self.tiles_to_spawn.clear()
        self.spawn_random()
        self.should_wait_for_move_finished = False

    '''
    Algorithm:
    1. Take line
    2. Collapse
    3. Replace line with collapsed one
    '''

    def move(self, direction):
        if self.should_wait_for_move_finished:
            return
        lines = self.get_lines(direction)
        new_lines, moves = self.collapse(lines)
        self.handle_moves(moves, direction)
        self.update_lines(new_lines, direction)

    def get_lines(self, direction):
        lines = []
        if direction == Board.LEFT:
            for row in range(self.rows):
                lines.append([i for i in self.m[row][:]])
        elif direction == Board.RIGHT:
            for row in range(self.rows):
                lines.append([i for i in self.m[row][::-1]])
        elif direction == Board.UP:
            for col in range(self.cols):
                lines.append([self.m[i][col] for i in range(self.rows)])
        elif direction == Board.DOWN:
            for col in range(self.cols):
                lines.append([self.m[i][col]
                              for i in reversed(range(self.rows))])
        return lines

    def get_positions(self, direction):
        positions = []
        if direction == Board.LEFT:
            for row in range(self.rows):
                positions.append([(row, i) for i in range(self.cols)])
        elif direction == Board.RIGHT:
            for row in range(self.rows):
                positions.append([(row, i)
                                  for i in reversed(range(self.cols))])
        elif direction == Board.UP:
            for col in range(self.cols):
                positions.append([(i, col) for i in range(self.rows)])
        elif direction == Board.DOWN:
            for col in range(self.cols):
                positions.append([(i, col)
                                  for i in reversed(range(self.rows))])
        return positions

    def handle_moves(self, moves, direction):
        if direction == Board.LEFT:
            for row in range(self.rows):
                for move in moves[row]:
                    self.handle_move((row, move[0]), (row, move[1]))
        elif direction == Board.RIGHT:
            for row in range(self.rows):
                for move in moves[row]:
                    self.handle_move(
                        (row, self.cols - 1 - move[0]),
                        (row, self.cols - 1 - move[1]))
        elif direction == Board.UP:
            for col in range(self.cols):
                for move in moves[col]:
                    self.handle_move((move[0], col), (move[1], col))
        elif direction == Board.DOWN:
            for col in range(self.cols):
                for move in moves[col]:
                    self.handle_move(
                        (self.rows - 1 - move[0], col),
                        (self.rows - 1 - move[1], col))
        if self.should_wait_for_move_finished:
            self.delayed_call(Board.TILE_MOVE_DURATION_MS,
                              self.handle_post_move)

    def handle_move(self, cell_from, cell_to):
        self.should_wait_for_move_finished = True
        tiles = self.tiles
        tile1 = tiles[cell_from[0]][cell_from[1]]
        tile2 = tiles[cell_to[0]][cell_to[1]]
        tile1.move_to(cell_to[0], cell_to[1], Board.TILE_MOVE_DURATION_MS)
        tiles[cell_from[0]][cell_from[1]] = None
        if tile2 is not None:
            tiles[cell_to[0]][cell_to[1]] = None
            self.tiles_to_destroy.append(tile1)
            self.tiles_to_destroy.append(tile2)
            self.tiles_to_spawn.append(
                (tile1.value * 2, cell_to[0], cell_to[1]))
        else:
            tiles[cell_to[0]][cell_to[1]] = tile1

    def update_lines(self, new_lines, direction):
        if direction == Board.LEFT:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.m[row][col] = new_lines[row][col]
        elif direction == Board.RIGHT:
            for row in range(self.rows):
                for col in range(self.cols):
                    self.m[row][col] = new_lines[row][-1-col]
        elif direction == Board.UP:
            for col in range(self.cols):
                for row in range(self.rows):
                    self.m[row][col] = new_lines[col][row]
        elif direction == Board.DOWN:
            for col in range(self.cols):
                for row in range(self.rows):
                    self.m[row][col] = new_lines[col][-1-row]

    def collapse(self, lines):
        new_lines = []
        moves = []
        for line in lines:
            new_line, line_moves = self.collapse_one_line(line)
            new_lines.append(new_line)
            moves.append(line_moves)
        return new_lines, moves

    def collapse_one_line(self, line):
        # [0, 2, 2, 4] -> [2, 0, 2, 4] -> [4, 0, 0, 4] -> [4, 4, 0, 0]
        # [2, 4, 4, 2] -> [2, 4, 4, 2] -> [2, 8, 0, 2] -> [2, 8, 2, 0]
        # [2, 4, 2, 4] -> [2, 4, 2, 4] (not a move)
        moves = []
        target_cell = 0
        for i in range(1, len(line)):
            if line[i]:
                if line[target_cell] == 0:
                    # move to empty cell
                    line[target_cell], line[i] = line[i], line[target_cell]
                    moves.append((i, target_cell))
                elif line[target_cell] == line[i]:
                    # move and collapse
                    line[target_cell] *= 2
                    line[i] = 0
                    moves.append((i, target_cell))
                    target_cell += 1
                else:
                    # move to empty cell
                    target_cell += 1
                    if target_cell != i:
                        line[target_cell], line[i] = line[i], line[target_cell]
                        moves.append((i, target_cell))
        return line, moves

    def test_collapse_algo(self):
        lines = [[0, 2, 2, 4], [2, 4, 4, 2], [2, 4, 2, 4], [2, 2, 2, 2],
                 [2, 2, 4, 4], [0, 0, 4, 2], [2, 0, 0, 2], [0, 2, 0, 2]]

        check = [[4, 4, 0, 0], [2, 8, 2, 0], [2, 4, 2, 4], [4, 4, 0, 0],
                 [4, 8, 0, 0], [4, 2, 0, 0], [4, 0, 0, 0], [4, 0, 0, 0]]
        for line, check in zip(lines, check):
            new_line, _ = self.collapse_one_line(line)
            for i, v in enumerate(new_line):
                if v != check[i]:
                    print(
                        f"Board/test_collapse: {new_line} != {check} at pos {i}")
                    return
        print(".", end="")


# TESTS
def test_board():
    # test collapse
    board = Board(4, 4)
    board.test_collapse_algo()

    # test spawn
    def create_val_spawner(val_seq):
        i = 0

        def spawner():
            nonlocal i
            i += 1
            return val_seq[i-1]
        return spawner

    def create_pos_selector(pos_seq):
        i = 0

        def selector(arr):
            nonlocal i
            i += 1
            return arr[pos_seq[i-1]]
        return selector

    states = [
        [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 4, 0, 0, 0, 0, 0, 4, 0, 0, 0, 2],
        [2, 0, 0, 2, 0, 4, 0, 0, 4, 0, 0, 4, 0, 0, 0, 2],
    ]

    board = Board(4, 4)
    val_seq = [2, 2, 2, 4, 4, 4]
    pos_seq = [0, 2, 13, 3, 8, 5]
    board.val_spawner = create_val_spawner(val_seq)
    board.pos_selector = create_pos_selector(pos_seq)
    for i in range(len(val_seq)):
        # do spawn
        board.spawn_random()
        # check board
        if not board.check_state(states[i]):
            print(f"\nState after {i}th instruction is uncorrect")
            print(f"Current:\n{board}")
            print(f"Expected:\n{Board(4, 4, states[i])}")
            return
    print(".", end="")

    # test board behaviour
    board_state = [2, 0, 4, 0, 2, 2, 0, 0, 4, 2, 2, 2, 8, 2, 2, 8]
    board = Board(4, 4, board_state)

    def left():
        board.move(Board.LEFT)

    def right():
        board.move(Board.RIGHT)

    def up():
        board.move(Board.UP)

    def down():
        board.move(Board.DOWN)

    instructions = [left, right, down, up, left, up, right, down]
    states = [
        [2, 4, 0, 0, 4, 0, 0, 0, 4, 4, 2, 0, 8, 4, 8, 0],
        [0, 0, 2, 4, 0, 0, 0, 4, 0, 0, 8, 2, 0, 8, 4, 8],
        [0, 0, 0, 0, 0, 0, 2, 8, 0, 0, 8, 2, 0, 8, 4, 8],
        [0, 8, 2, 8, 0, 0, 8, 2, 0, 0, 4, 8, 0, 0, 0, 0],
        [8, 2, 8, 0, 8, 2, 0, 0, 4, 8, 0, 0, 0, 0, 0, 0],
        [16, 4, 8, 0, 4, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 16, 4, 8, 0, 0, 4, 8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 8, 16]
    ]

    for i, instruction in enumerate(instructions):
        # do move
        instruction()
        # check board
        if not board.check_state(states[i]):
            print(f"\nState after {i}th instruction is uncorrect")
            print(f"Current:\n{board}")
            print(f"Expected:\n{Board(4, 4, states[i])}")
            return
    print(".", end="")
