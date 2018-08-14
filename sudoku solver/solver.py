#!/usr/bin/env python3
# (c) 2018 Hyeongjin Kim
# a script to solve (or attempt to solve) Sudoku

from module import *  # importing useful data structures from module
import ast  # used in evaluating a string repr of a list

__all__ = ["solve", "safesolve", "countsolve"]

squares = squares()  # list of 81 squares/points
peers = peers()  # dictionary of peers
boxes = boxes()  # dictionary of squares in boxes
_rows = 'ABCDEFGHI'
_columns = '123456789'

def kandidates(db):
    """Returns a dictionary of each 81 squares as key and a string of
    '123456789' if square is blank or the string of value itself
    if already filled in from initial clues.

    db: initial Sudoku dictionary processed from sudoku_data method
    result: dictionary
        key: string of points
        value: '123456789' or str(value) if filled
    """
    candList = dict()
    for point in squares:
        if db[point] != '0':
            candList[point] = str(db[point])
        else:
            candList[point] = '123456789'
    return candList

def isSolved(candidates):
    """Returns True if candidates dictionary corresponds
    to a dictionary of a solved Sudoku board else False if not solved.

    candidates: dictionary
    result: boolean
    """
    for point in candidates:
        if len(candidates[point]) != 1:  # a solved Sudoku must have a unique solution
            return False
    for column in columnsNum(candidates):
        if sum(column) != 45:
            return False
    for row in rowsNum(candidates):
        if sum(row) != 45:
            return False
    for box in boxesNum(candidates):
        if sum(box) != 45:
            return False
    return True

def eliminate(candidates):
    """Single Possibility Rule: Returns a dictionary of possible candidates (value)
    for each square (key) after eliminating impossible candidates by
    excluding any value from the square's SOLVED peers.

    candidates: dictionary
    result: dictionary
        key: string of points
        value: string of possible candidates
    """
    solvedPoints = [point for point in candidates if len(candidates[point]) == 1]  # list of solved points
    for point in solvedPoints:
        for peer in peers[point]:
            value = candidates[point]
            candidates[peer] = candidates[peer].replace(value,'')  # eliminating value from solved peer
    return candidates

def slicing(candidates):
    """Slicing Dicing / Hidden Singles Method: Returns a dictionary of
    possible candidates (value) for each square (key) by assigning a value, say x,
    to a square if such square is the only point within its box that contains x.

    candidates: dictionary
    result: dictionary
        key: string of points
        value: string of possible candidates
    """
    for point in candidates:
        for value in candidates[point]:
            values = ''  # string of all possible candidates in squares of point's box excluding itself
            for box in boxes[point]:
                values += candidates[box]
            if value not in values:  # point is the only square within box with value as its candidate(s)
                candidates[point] = value  # that point must be filled with value
    return candidates

def subgroupRowsExclusion(candidates):
    """Subgroup Exclusion by Row: Returns a dictionary of possible candidates (value)
    for each square (key) by eliminating possible candidates via subgroup exclusion.
    Given a subgroup (a group of two or three squares within SAME box), in this case by row,
    if a given candidate value, say x, within the subgroup does not appear in any of the candidates
    of the squares within the same row, then x cannot be one of the possible candidates for squares
    within the subgroup's box, of course excluding the subgroup squares themselves. The reverse is true
    if we look for candidate x within squares of same box and work our way through the squares in the row.
    Refer to README for further details, for this method is difficult to grasp.

    candidates: dictionary
    result: dictionary
        key: string of points
        value: string of possible candidates
    """
    for subrow in subgroupsRows().keys():  # subgroup is given as a string repr of list of three points
        subrowValues = ''  # the candidate numbers within subgroup points
        for subrowPoint in ast.literal_eval(subrow):  # ast.literal_eval to evaluate the string repr of list
            subrowValues += candidates[subrowPoint]
        rowgroupValues = ''  # the candidate numbers within points of same row as subgroup
        for rowgroupPoint in subgroupsRows()[subrow]:
            rowgroupValues += candidates[rowgroupPoint]
        # Construct a set of value(s) in subgroup but NOT in other squares within the same row
        values = set(map(int,subrowValues)).difference(set(map(int,rowgroupValues)))
        for value in values:
            for rowboxPoint in boxgroupsRows()[subrow]:
                # Remove such value(s) from candidates of squares within same box as subgroup
                candidates[rowboxPoint] = candidates[rowboxPoint].replace(str(value), '')

        # Iterate the process in reverse order
        boxgroupValues = ''  # the candidate numbers within points of same box as subgroup
        for boxgroupPoint in boxgroupsRows()[subrow]:
            boxgroupValues += candidates[boxgroupPoint]
        # Construct a set of value(s) in subgroup but NOT in other squares within the same box
        values = set(map(int,subrowValues)).difference(set(map(int,boxgroupValues)))
        for value in values:
            for subrowPoint in subgroupsRows()[subrow]:
                # Remove such value(s) from candidates of squares within same row as subgroup
                candidates[subrowPoint] = candidates[subrowPoint].replace(str(value), '')

    return candidates

def subgroupColumnsExclusion(candidates):
    """Subgroup Exclusion by Column: Returns a dictionary of possible candidates (value)
    for each square (key) by eliminating possible candidates via subgroup exclusion.
    Given a subgroup (a group of two or three squares within SAME box), in this case by column,
    if a given candidate value, say x, within the subgroup does not appear in any of the candidates
    of the squares within the same column, then x cannot be one of the possible candidates for squares
    within the subgroup's box, of course excluding the subgroup squares themselves. The reverse is true
    if we look for candidate x within squares of same box and work our way through the squares in the column.
    Refer to README for further details, for this method is difficult to grasp.

    candidates: dictionary
    result: dictionary
        key: string of points
        value: string of possible candidates
    """
    for subcolumn in subgroupsColumns().keys():
        subcolumnValues = ''  # the candidate numbers within subgroup points
        for subcolumnPoint in ast.literal_eval(subcolumn):
            subcolumnValues += candidates[subcolumnPoint]
        columngroupValues = ''  # the candidate numbers within points of same column as subgroup
        for columngroupPoint in subgroupsColumns()[subcolumn]:
            columngroupValues += candidates[columngroupPoint]
        # Construct a set of value(s) in subgroup but NOT in other squares within the same column
        values = set(map(int,subcolumnValues)).difference(set(map(int,columngroupValues)))
        for value in values:
            for columnboxPoint in boxgroupsColumns()[subcolumn]:
                # Remove such value(s) from candidates of squares within same box as subgroup
                candidates[columnboxPoint] = candidates[columnboxPoint].replace(str(value), '')

        # Iterate the process in reverse order
        boxgroupValues = ''  # the candidate numbers within points of same box as subgroup
        for boxgroupPoint in boxgroupsColumns()[subcolumn]:
            boxgroupValues += candidates[boxgroupPoint]
        # Construct a set of value(s) in subgroup but NOT in other squares within the same box
        values = set(map(int,subcolumnValues)).difference(set(map(int,boxgroupValues)))
        for value in values:
            for subcolumnPoint in subgroupsColumns()[subcolumn]:
                # Remove such value(s) from candidates of squares within same column as subgroup
                candidates[subcolumnPoint] = candidates[subcolumnPoint].replace(str(value), '')
    return candidates

def nakedpairs(candidates):
    """Naked Pairs (Triplets, Quartets) Elimination: Returns a dictionary of possible candidates (value)
    for each square (key) by eliminating possible candidates via naked pairs principle.
    Given a region (row, column, or box) if a pair of numbers, say x and y, only appear in TWO squares,
    then no other squares within its region and POTENTIALLY other interacting region cannot have x and y
    as their possible candidates.
    This principle can apply for triplet, or even quartet, of numbers given that there are three or four
    squares, respectively, that have the same combination of numbers.
    Refer to README for further details, for this method will take more words to explain.

    candidates: dictionary
    result: dictionary
        key: string of points
        value: string of possible candidates
    """
    for row in rowify(candidates):  # convert candidates to be ordered by rows
        flipped = flipify(row)  # flip the dictionary so that its keys are the values and vice versa
        # Construct a dictionary of pair/triplet/quartet numbers corresponding to the points that have such combinations
        nakedrowpairs = {key:value for key,value in flipped.items() if len(value) > 1 and len(value) == len(key)}
        for pairNum,pairs in nakedrowpairs.items():
            rowReference = pairs[0][0]  # rowReference indicates which row the pair is in
            for point in rowDict()[rowReference]:
                for num in pairNum:
                    if point not in pairs:
                        candidates[point] = candidates[point].replace(num,'')

    # The same format of iteration applies for columns
    for column in columnify(candidates):
        flipped = flipify(column)
        nakedcolumnpairs = {key:value for key,value in flipped.items() if len(value)>1 and len(value) == len(key)}
        for pairNum,pairs in nakedcolumnpairs.items():
            columnReference = pairs[0][1]
            for point in columnDict()[columnReference]:
                for num in pairNum:
                    if point not in pairs:
                        candidates[point] = candidates[point].replace(num,'')

    # This is implemented for two reasons:
    # 1) The pair/triplet/quartet of numbers may not appear in the same
    #    row or column, that is they are adjacent diagonally.
    # 2) If the pair/triplet/quarter appear in a row or column and
    #    are in the same box, then the elimination principle should
    #    apply for squares within the same box, which was not implemented
    #    in the previous two iterations.
    for box in boxify(candidates):
        flipped = flipify(box)
        nakedboxpairs = {key:value for key,value in flipped.items() if len(value)>1 and len(value) == len(key)}
        for pairNum,pairs in nakedboxpairs.items():
            boxReference = pairs[0]
            for point in boxes[boxReference]:
                for num in pairNum:
                    if point not in pairs:
                        candidates[point] = candidates[point].replace(num,'')
    return candidates

def hiddenpairs(candidates):
    pass

def XWings(candidates):
    pass

def solve(db):
    """This function should run all of the previous functions to solve Sudoku.

    result: solved sudoku
    """
    candidates = kandidates(db)
    while not isSolved(candidates):
        candidates = eliminate(candidates)
        candidates = slicing(candidates)
        candidates = subgroupRowsExclusion(candidates)
        candidates = subgroupColumnsExclusion(candidates)
        candidates = nakedpairs(candidates)
    return candidates

def safesolve(db):
    """This function should run all of the previous functions to solve Sudoku.

    result: solved sudoku if solved else None
    """
    candidates = kandidates(db)
    for _ in range(30):
        candidates = eliminate(candidates)
        candidates = slicing(candidates)
        candidates = subgroupRowsExclusion(candidates)
        candidates = subgroupColumnsExclusion(candidates)
        candidates = nakedpairs(candidates)
    if not isSolved(candidates):
        return None
    else:
        return candidates

def countsolve(db):
    """This function should run all of the previous functions to solve Sudoku.

    result: 1 if sudoku is solved else 0
    """
    candidates = kandidates(db)
    for _ in range(30):
        candidates = eliminate(candidates)
        candidates = slicing(candidates)
        candidates = subgroupRowsExclusion(candidates)
        candidates = subgroupColumnsExclusion(candidates)
        candidates = nakedpairs(candidates)
    if not isSolved(candidates):
        return 0
    else:
        return 1