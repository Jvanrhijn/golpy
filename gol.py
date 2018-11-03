import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rle_parser import Parser


class Grid:

    def __init__(self, state):
        self._grid = state
        self._rows, self._columns = state.shape

    @classmethod
    def init_random(cls, side):
        grid = np.random.randint(0, high=2, size=(side, side))
        return cls(grid)

    def evolve(self):
        # periodic boundary conditions
        neighbors = np.roll(self._grid, 1, axis=0)\
                 +  np.roll(self._grid, -1, axis=0)\
                 +  np.roll(self._grid, 1, axis=1)\
                 +  np.roll(self._grid, -1, axis=1)\
                 +  np.roll(np.roll(self._grid, 1, axis=0), 1, axis=1)\
                 +  np.roll(np.roll(self._grid, -1, axis=0), -1, axis=1)\
                 +  np.roll(np.roll(self._grid, 1, axis=0), -1, axis=1)\
                 +  np.roll(np.roll(self._grid, -1, axis=0), 1, axis=1)
        self._grid = np.logical_or(neighbors == 3, 
                np.logical_and(self._grid == 1, neighbors == 2)).astype(int)

    def array(self):
        return self._grid


def update(frame, grid, im):
    grid.evolve()
    im.set_array(1 - grid.array())
    return im,


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(1)

    # initialize game of life
    pattern = Parser(sys.argv[1]).parse()
    grid = Grid(pattern)
    #grid = Grid.init_random(int(sys.argv[1]))

    # setup animation
    fig, ax = plt.subplots(1)
    im = plt.imshow(grid.array(), animated=True, cmap='gray')

    # animate
    ani = FuncAnimation(fig, lambda i: update(i, grid, im), interval=100, blit=True)
    plt.show()

