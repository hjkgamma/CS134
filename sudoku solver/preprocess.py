#!/usr/bin/env python3
# (c) 2018 Hyeongjin Kim
# a script to read in data of Sudoku puzzles

def sudoku_data(filename='sudoku.txt'):
    """This method reads in Sudoku puzzles from txt file
    categorized by single line headings of the form
    'Grid [number]'. This returns a list of dictionaries,
    wherein each dictionary contains 81 keys for each square
    within the board and its corresponding value (0 is given
    blank squares).

    filename: txt file of Sudoku puzzles
    example of txt:
    Grid 01
    003020600
    900305001
    001806400
    008102900
    700000008
    006708200
    002609500
    800203009
    005010300
    result: list of dictionaries
    """
    file = open(filename, 'r')
    db = []
    result = []
    s = file.readlines()
    index = -1
    rows = 'ABCDEFGHI'
    columns = '123456789'
    for row in s:
        if row.strip()[0] == "G":
            index += 1
            db.append([])
            continue
        db[index].extend(row.strip())
    for e in db:
        temp = dict()
        for row,i in zip(rows,range(0,9)):
            for column,j in zip(columns,range(0,9)):
                temp[(row+column)] = str(e[9*i+j])
        result.append(temp)
    return result

def sudoku_process(string):
    db = []
    result = dict()
    rows = 'ABCDEFGHI'
    columns = '123456789'
    db.extend(string.strip())
    for row,i in zip(rows,range(0,9)):
        for column,j in zip(columns,range(0,9)):
            result[row+column] = str(db[9*i+j])
    return result