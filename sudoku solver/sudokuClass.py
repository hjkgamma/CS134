#!/usr/bin/env python3
# (c) 2018 Hyeongjin Kim
# a script for the Sudoku class

from module import squares

class Sudoku(object):
    """This is a Sudoku class that can be used to print
    out a Sudoku board.

    Internally data keeps track of a dictionary of each
    81 squares/points in the board and their corresponding number.
    """
    def __init__(self,db=None):
        self._rows = 'ABCDEFGHI'
        self._columns = '123456789'
        self.squares = squares()
        if db is not None:
            self._data = db
        else:
            self._data = dict((key,0) for key in self.squares)

    def __setitem__(self, key, value):
        assert 0 <= value <= 9, "The value must be between 1 and 9 (inclusive)."
        assert key in self.squares, "The value must be inside the Sudoku board!"
        self._data[key] = value

    def __getitem__(self, point):
        return self._data[point]

    def __eq__(self, other):
        return self._data == other._data

    def __str__(self):
        width = max([len(v) for v in self._data.values()]) + 3
        line = '-'*(width*3) + '+' + '-'*(width*3) + '+' + '-'*(width*3)
        string = ''
        for r in 'ABCDEFGHI':
            for c in '123456789':
                string += self[r + c].center(width)
                string += '|' if c in '36' else ''
            if r in 'CF':
                string += '\n'
                string += line
            string += '\n'
        return string