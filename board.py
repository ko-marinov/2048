import itertools
import random


class Board:
    def __init__(self, rows, cols, iterable=None):
        self.rows = rows
        self.cols = cols
        self.m = [[0 for c in range(cols)] for r in range(rows)]

        if iterable != None:
            for n, (i, j) in enumerate(itertools.product(range(self.rows), range(self.cols))):
                self.m[i][j] = iterable[n]

    def val_spawner(self):
        return 2 * random.randint(0, 1)

    def pos_selector(self, select_from):
        return select_from[random.randint(0, len(select_from))]

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

    def spawn(self, val_spawner=None, pos_selector=None):
        if val_spawner is None:
            val_spawner = self.val_spawner
        if pos_selector is None:
            pos_selector = self.pos_selector
        empty_cells = []
        for i, j in itertools.product(range(self.rows), range(self.cols)):
            if self.m[i][j] == 0:
                empty_cells.append((i, j))

        if not empty_cells:
            print("GAME OVER")

        row, col = pos_selector(empty_cells)
        self.m[row][col] = val_spawner()

    '''
    Algorithm:
    1. Take line
    2. Collapse
    3. Replace line with collapsed one
    '''

    def left(self):
        # <--
        for row in range(self.rows):
            # create line
            line = [i for i in self.m[row][:]]
            # collapse
            result = self.collapse(line)
            # update row with result
            for col in range(self.cols):
                self.m[row][col] = result[col]

    def right(self):
        # -->
        for row in range(self.rows):
            # create line
            line = [i for i in self.m[row][:]]
            # collapse
            result = self.collapse(line[::-1])
            # update row with result
            for col in range(self.cols):
                self.m[row][col] = result[-1-col]

    def up(self):
        # ↑
        for col in range(self.cols):
            line = [self.m[i][col] for i in range(self.rows)]
            result = self.collapse(line)
            for row in range(self.rows):
                self.m[row][col] = result[row]

    def down(self):
        # ↓
        for col in range(self.cols):
            line = [self.m[i][col] for i in range(self.rows)]
            result = self.collapse(line[::-1])
            for row in range(self.rows):
                self.m[row][col] = result[-1-row]

    def collapse(self, line):
        # [0, 2, 2, 4] -> [2, 0, 2, 4] -> [4, 0, 0, 4] -> [4, 4, 0, 0]
        # [2, 4, 4, 2] -> [2, 4, 4, 2] -> [2, 8, 0, 2] -> [2, 8, 2, 0]
        # [2, 4, 2, 4] -> [2, 4, 2, 4] (not a move)

        target_cell = 0
        for i in range(1, len(line)):
            if line[i]:
                if line[target_cell] == 0:
                    line[target_cell], line[i] = line[i], line[target_cell]
                elif line[target_cell] == line[i]:
                    line[target_cell] *= 2
                    line[i] = 0
                    target_cell += 1
                else:
                    target_cell += 1
                    if i != target_cell:
                        line[target_cell], line[i] = line[i], line[target_cell]
        return line

    def test_collapse_algo(self):
        lines = [[0, 2, 2, 4], [2, 4, 4, 2], [2, 4, 2, 4], [2, 2, 2, 2],
                 [2, 2, 4, 4], [0, 0, 4, 2], [2, 0, 0, 2], [0, 2, 0, 2]]

        check = [[4, 4, 0, 0], [2, 8, 2, 0], [2, 4, 2, 4], [4, 4, 0, 0],
                 [4, 8, 0, 0], [4, 2, 0, 0], [4, 0, 0, 0], [4, 0, 0, 0]]
        for line, check in zip(lines, check):
            result = self.collapse(line)
            for i, v in enumerate(result):
                if v != check[i]:
                    print(
                        f"Board/test_collapse: {result} != {check} at pos {i}")
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
        board.spawn()
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
        board.left()

    def right():
        board.right()

    def up():
        board.up()

    def down():
        board.down()

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

    for i, move in enumerate(instructions):
        # do move
        move()
        # check board
        if not board.check_state(states[i]):
            print(f"\nState after {i}th instruction is uncorrect")
            print(f"Current:\n{board}")
            print(f"Expected:\n{Board(4, 4, states[i])}")
            return
    print(".", end="")
