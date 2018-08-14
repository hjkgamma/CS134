#!/usr/bin/env python3
# (c) 2018 Hyeongjin Kim
# a module of useful data structures for solving Sudoku
"""
This module file contains the various dictionaries and data structures
that I have created that will be useful in solving Sudoku puzzles
when implementing various solving techniques.
"""

__all__ = ["squares", "rowDict", "columnDict", "peers", "boxes", 
           "rowsNum", "columnsNum", "boxesNum", "boxgroupsRows", 
           "boxgroupsColumns", "subgroupsRows", "subgroupsColumns",
           "rowify", "columnify", "boxify", "flipify"]

_rows = 'ABCDEFGHI'
_columns = '123456789'
_values = [i for i in range(1,10)]

def squares():
    """Returns a list of all 81 squares/points of the Sudoku board
    for reference with 'ABDEFGHI' designated as the row and
    '123456789' designated as the column. For example, 'A1' is
    the most upper-left square and 'E5' is the center square of
    the Sudoku board.

    result: list
    """
    return [row + column for row in _rows for column in _columns]

def rowPoints():
    """Returns a list of 9 lists with each list containing 9 points
    for each row from 'ABCDEFGHI'.

    result: list

    >>> rowPoints()[0]
    ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
    """
    result = []
    for row in _rows:
        result.append([row + column for column in _columns])
    return result

def rowDict():
    """Returns a dictionary with key as the row-letter from 'ABDEFGHI' and
    the corresponding list of 9 squares/points from same row as the value.

    result: dictionary
        key: string from 'ABCDEFGHI'
        value: list of strings

    >>> rowDict()['G']
    ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9']
    """
    result = dict()
    for row in _rows:
        result[row] = result.get(row,[]) + [row + column for column in _columns]
    return result

def columnPoints():
    """Returns a list of 9 lists with each list containing 9 points
    for each column from '123456789'.

    result: list

    >>> columnPoints()[0]
    ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
    """
    result = []
    for column in _columns:
        result.append([row + column for row in _rows])
    return result

def columnDict():
    """Returns a dictionary with key as the column-number from '123456789'
    and the corresponding list of 9 squares/points from same column as the value.

    result: dictionary
        key: string from '123456789'
        value: list of strings

    >>> columnDict()['3']
    ['A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'I3']
    """
    result = dict()
    for column in _columns:
        result[column] = result.get(column,[]) + [row + column for row in _rows]
    return result

def boxPoints():
    """Returns a list of 9 lists of 9 squares in each 3x3 box/block in
    the Sudoku board. This iteration is done by row, so from left to right
    within each box.

    result: list

    >>> boxPoints()[0]
    ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
    """
    result = []
    for a in ['ABC', 'DEF', 'GHI']:
        for b in ['123','456','789']:
            result.append([i+j for i in a for j in b])
    return result

def boxPointsbyColumns():
    """Returns a list of 9 lists of 9 squares in each 3x3 box/block in
    the Sudoku board. This iteration is done by column, so from top to
    bottom in each box.

    result: list

    >>> boxPointsbyColumns()[8]
    ['G7', 'H7', 'I7', 'G8', 'H8', 'I8', 'G9', 'H9', 'I9']
    """
    result = []
    for a in ['123','456','789']:
        for b in ['ABC', 'DEF', 'GHI']:
            result.append([j+i for i in a for j in b])
    return result

def unitList():
    """Returns a list of all of the lists in rowPoints, columnPoints,
    and boxPoints.

    result: list
    """
    return(rowPoints() + columnPoints() + boxPoints())

def units():
    """Returns a dictionary of each 81 squares as key and a list
    of squares in rows, columns, and boxes that contain the key/square.

    result: dictionary
        key: string of points
        value: lists of rowPoints, columnPoints, and boxPoints

    >>> units()['E5']
    [['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'], ['A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'I5'], ['D4', 'D5', 'D6', 'E4', 'E5', 'E6', 'F4', 'F5', 'F6']]
    """
    units = dict()
    for square in squares():
        for unit in unitList():
            if square in unit:
                units[square] = units.get(square,[])
                units[square].append(unit)
    return units

def peers():
    """Returns a dictionary of each 81 squares as key and a set
    of 20 squares that each key interacts with, within the rowPoints,
    columnPoints, and boxPoints from units().

    result: dictionary
        key: string of points
        value: set of 20 peers
    """
    peers = dict()
    for point in squares():
        point_peers = set()
        for unit in units()[point]:
            for square in unit:
                if square != point:
                    point_peers.add(square)
        peers[point] = point_peers
    return peers

def boxes():
    """Returns a dictionary of each 81 squares as key and a set
    of all 8 other squares of the box that the key is in.

    result: dictionary
        key: string of points
        value: set of 8 squares in the box that contains key
    """
    boxes = dict()
    for point in squares():
        box_peers = set()
        for box in boxPoints():
            if point in box:
                box_peers = set(box).difference(set([point]))
        boxes[point] = box_peers
    return boxes

def boxgroupsRows():
    """Returns a dictionary of each 27 row subgroups as key and
    a set of all 6 other squares of the box that the key is in.

    result: dictionary
        key: string repr of list of 3 points in row subgroup
        value: set of 6 other squares in the box that contains key
    """
    boxgroups = dict()
    for box in boxPoints():
        for i in range(0,6+1,3):
            subrow = box[i:i+3]
            boxgroups[str(subrow)] = set(box).difference(set(subrow))
    return boxgroups

def boxgroupsColumns():
    """Returns a dictionary of each 27 column subgroups as key and
    a set of all 6 other squares of the box that the key is in.

    result: dictionary
        key: string repr of list of 3 points in column subgroup
        value: set of 6 other squares in the box that contains key
    """
    boxgroups = dict()
    for box in boxPointsbyColumns():
        for i in range(0,6+1,3):
            subcolumn = box[i:i+3]
            boxgroups[str(subcolumn)] = set(box).difference(set(subcolumn))
    return boxgroups

def subgroupsRows():
    """Returns a dictionary of each 27 row subgroups as key and
    a set of all 6 other squares of the row that the key is in.

    result: dictionary
        key: string repr of list of 3 points in row subgroup
        value: set of 6 other squares in the row that contains key
    """
    subgroups = dict()
    for row in rowPoints():
        for i in range(0,6+1,3):
            subrow = row[i:i+3]
            subgroups[str(subrow)] = set(row).difference(set(subrow))
    return subgroups

def subgroupsColumns():
    """Returns a dictionary of each 27 column subgroups as key and
    a set of all 6 other squares of the column that the key is in.

    result: dictionary
        key: string repr of list of 3 points in column subgroup
        value: set of 6 other squares in the column that contains key
    """
    subgroups = dict()
    for column in columnPoints():
        for i in range(0,6+1,3):
            subcolumn = column[i:i+3]
            subgroups[str(subcolumn)] = set(column).difference(set(subcolumn))
    return subgroups

def rowsNum(candidates):
    """Returns a list of 9 lists of the values of each square in
    the row given a dictionary of points as key and possible candidates
    as value.

    candidates: dictionary of points as key and possible values as value
    result: dictionary
        key: string of points
        value: string of possible candidate values
    """
    rows = [[int(candidates[point]) for point in row] for row in rowPoints()]
    return rows

def columnsNum(candidates):
    """Returns a list of 9 lists of the values of each square in
    the column given a dictionary of points as key and possible candidates
    as value.

    candidates: dictionary of points as key and possible values as value
    result: dictionary
        key: string of points
        value: string of possible candidate values
    """
    columns = [[int(candidates[point]) for point in column] for column in columnPoints()]
    return columns

def boxesNum(candidates):
    """Returns a list of 9 lists of the values of each square in
    the box given a dictionary of points as key and possible candidates
    as value.

    candidates: dictionary of points as key and possible values as value
    result: dictionary
        key: string of points
        value: string of possible candidate values
    """
    boxes = [[int(candidates[point]) for point in box] for box in boxPoints()]
    return boxes

def rowify(candidates):
    """Returns a list of 9 dictionaries of points as key and their possible
    candidates as value, ordered by row.

    candidates: dictionary of points as key and possible values as value
    result: a list ordered by row containing dictionaries
        dictionary's key: string of points
        dictionary's value: string of possible candidate values
    """
    result = []
    for row in rowPoints():
        temp = dict()
        for point in row:
            temp[point] = candidates[point]
        result.append(temp)
    return result

def columnify(candidates):
    """Returns a list of 9 dictionaries of points as key and their possible
    candidates as value, ordered by column.

    candidates: dictionary of points as key and possible values as value
    result: a list ordered by column containing dictionaries
        dictionary's key: string of points
        dictionary's value: string of possible candidate values
    """
    result = []
    for column in columnPoints():
        temp = dict()
        for point in column:
            temp[point] = candidates[point]
        result.append(temp)
    return result

def boxify(candidates):
    """Returns a list of 9 dictionaries of points as key and their possible
    candidates as value, ordered by box. The first list refers to the most
    upper-left box, the third list as the most upper-right box, and so forth.

    candidates: dictionary of points as key and possible values as value
    result: a list ordered by box containing dictionaries
        dictionary's key: string of points
        dictionary's value: string of possible candidate values
    """
    result = []
    for box in boxPoints():
        temp = dict()
        for point in box:
            temp[point] = candidates[point]
        result.append(temp)
    return result

def flipify(db):
    """Returns a flipped dictionary with original dictionary's value as the
    flipped dictionary's key and vice versa.

    db: dictionary
    result: flipped dictionary
    """
    flipped = dict()
    for k,v in db.items():
        flipped[v] = flipped.get(v,[]) + [k]
    return flipped

# The following code tests these tools when run as a script:
if __name__ == '__main__':
    from doctest import testmod
    testmod()
