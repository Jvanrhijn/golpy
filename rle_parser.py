import re
import itertools
import numpy as np


class Parser:

    def __init__(self, fpath):
        self._tags = {"b": 0, "o": 1}
        comments = ["#N", "#C", "#c", "#O", "#P", "#R", "#r"]
        # Read actual lines from the RLE file
        self._lines = None
        with open(fpath, "r") as f:
            self._lines = list(filter(lambda line: line[:2] not in comments, f.readlines()))
        # get dimensions & strip header
        self._rows, self._columns = self._dimensions()
        self._lines = self._lines[1:]
        # concatenate all lines
        self._lines = ''.join(list(itertools.chain.from_iterable([line.rstrip()
            for line in self._lines])))
        # Split lines on $
        self._lines = self._lines.split('$') 

    def parse(self):
        grid = np.zeros((self._rows, self._columns))
        for i, line in enumerate(self._lines[1:]):
            if '!' in line:
                line = line.split('!')[1]  # Ignore everything after final '!'
            grid[i, :] = self._array_from_line(line)
        return np.array(grid)

    def _dimensions(self):
        """Returns tuple (rows, columns)"""
        return tuple(int(x.split('=')[1]) for x in self._lines[0].split(','))[::-1]

    def _array_from_line(self, line):
        line = line.strip("$")
        multiplier = 1
        output = []
        # split line in counts and tags:
        line = [s for s in re.split(r"([a-z])|([0-9]+)", line) if s not in ['', None]]
        for char in line:
            if char not in self._tags.keys():
                multiplier = int(char)
            else:
                output.append(multiplier*[self._tags[char]])
                multiplier = 1
        output = list(itertools.chain.from_iterable(output)) 
        output += [0]*(self._columns - len(output))
        return np.array(output)
