import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rle_parser import Parser


class Grid:

    def __init__(self, state, periodic=False):
        self._grid = state
        self._rows, self._columns = state.shape
        if periodic:
            self._neighbors = self._neighbors_periodic
        else:
            self._neighbors = self._neighbors_dead_boundary

    @classmethod
    def init_random(cls, side):
        grid = np.random.randint(0, high=2, size=(side, side))
        return cls(grid)

    def evolve(self):
        # periodic boundary conditions
        neighbors = self._neighbors()
        self._grid = np.logical_or(neighbors == 3, 
                np.logical_and(self._grid == 1, neighbors == 2)).astype(int)

    def array(self):
        return self._grid

    def _neighbors_periodic(self):
        neighbors = np.roll(self._grid, 1, axis=0)\
                 +  np.roll(self._grid, -1, axis=0)\
                 +  np.roll(self._grid, 1, axis=1)\
                 +  np.roll(self._grid, -1, axis=1)\
                 +  np.roll(np.roll(self._grid, 1, axis=0), 1, axis=1)\
                 +  np.roll(np.roll(self._grid, -1, axis=0), -1, axis=1)\
                 +  np.roll(np.roll(self._grid, 1, axis=0), -1, axis=1)\
                 +  np.roll(np.roll(self._grid, -1, axis=0), 1, axis=1)
        return neighbors
    
    def _neighbors_dead_boundary(self):
        neighbors = np.pad(self._grid, ((0, 0), (1, 0)), mode='constant')[:, :-1]\
                 +  np.pad(self._grid, ((0, 0), (0, 1)), mode='constant')[:, 1:]\
                 +  np.pad(self._grid, ((1, 0), (0, 0)), mode='constant')[:-1, :]\
                 +  np.pad(self._grid, ((0, 1), (0, 0)), mode='constant')[1:, :]\
                 +  np.pad(self._grid, ((1, 0), (1, 0)), mode='constant')[:-1, :-1]\
                 +  np.pad(self._grid, ((1, 0), (0, 1)), mode='constant')[:-1, 1:]\
                 +  np.pad(self._grid, ((0, 1), (1, 0)), mode='constant')[1:, -1:]\
                 +  np.pad(self._grid, ((0, 1), (0, 1)), mode='constant')[1:, 1:]
        return neighbors


def update(frame, grid, im):
    grid.evolve()
    im.set_array(1 - grid.array())
    return im,


if __name__ == "__main__":
    if len(sys.argv) < 2:
        exit(1)

    # initialize game of life
    pattern = Parser(sys.argv[1]).parse()
    grid = Grid(pattern, periodic=False)
    #grid = Grid.init_random(int(sys.argv[1]))

    # setup animation
    fig, ax = plt.subplots(1)
    im = plt.imshow(grid.array(), animated=True, cmap='gray')

    # animate
    ani = FuncAnimation(fig, lambda i: update(i, grid, im), interval=100, blit=True)
    plt.show()

