import numpy as np
from matplotlib import pyplot
from scipy.signal import convolve2d

glider = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]])

blinker = np.array([
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]])

glider_gun = np.array([
    [0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0]
])


class Game:
    def __init__(self, Size):
        self.board = np.zeros((Size, Size))

    def play(self):
        """Start a new game of life and play."""
        print("Playing life. Press ctrl + c to stop.")
        pyplot.ion()
        while True:
            self.move()
            self.show()
            pyplot.pause(0.0000005)

    def move(self):
        """Move the object for one step on the board. """
        STENCIL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        NeighbourCount = convolve2d(self.board, STENCIL, mode='same')

        for i in range(self.board.shape[0]):
            for j in range(self.board.shape[1]):
                self.board[i, j] = 1 if (
                    NeighbourCount[i, j] == 3 or (
                        NeighbourCount[i, j] == 2 and self.board[i, j]
                    )
                ) else 0

    def __setitem__(self, key, value):
        """Set the value of a particular position on the board. """
        self.board[key] = value

    def show(self):
        """Visualise the gameboard. """
        pyplot.clf()
        pyplot.matshow(self.board, fignum=0, cmap='binary')
        pyplot.show()

    def insert(self, pattern, coords):
        """
        Insert the pattern provided at a location
        centred at a given position.
        """
        x, y = coords
        reg_m, reg_n = pattern.grid.shape
        self.board[
            (x-reg_n//2):(x+reg_n//2+1), (y-reg_m//2):(y+reg_m//2+1)
        ] = pattern.grid


class Pattern:
    def __init__(self, pattern):
        self.grid = pattern
        self.shape = self.grid.shape
        self.nrows, self.ncols = self.shape

    def flip_vertical(self):
        """Returns a new Pattern whose rows are in reversed order. """
        return Pattern(self.grid[::-1, :])

    def flip_horizontal(self):
        """Returns a new Pattern whose columns are in reversed order. """
        return Pattern(self.grid[:, ::-1])

    def flip_diag(self):
        """Returns a new Pattern that is the transpose of the original. """
        new_pattern = np.zeros((self.ncols, self.nrows))
        for i in range(self.ncols):
            for j in range(self.nrows):
                new_pattern[i, j] = self.grid[j, i]
        return Pattern(new_pattern)

    def rotate(self, n):
        """
        Return a new Pattern which is the original pattern
        rotated through n right angles anticlockwise.
        """
        arr = self
        for _ in range(n):
            arr = arr.flip_diag().flip_vertical()
        return arr
