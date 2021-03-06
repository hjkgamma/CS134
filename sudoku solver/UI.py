#!/usr/bin/env python3
# (c) 2018 Hyeongjin Kim
# a basic user interface script for testing solver and solving Sudoku puzzles (possibly)

from sudokuClass import Sudoku
from module import *
from preprocess import sudoku_data, sudoku_process
from solver import *

def tester():
    """This method simply tests the solve method from solver script for 50 unsolved
    Sudoku puzzles databse.
    
    result: a count of solved Sudoku puzzles
    """
    count = 0
    database = sudoku_data()
    for db in database:
        count += countsolve(db)
    return "The solver has solved {} out of {} Sudoku puzzles!.".format(count,len(database))

if __name__ == '__main__':
    user = input("Would you like to see how many of 50 Sudoku puzzles I can solve? y/n ")
    while user not in 'yn':
        user = input("Would you like to see how many of 50 Sudoku puzzles I can solve? y/n ")
    if user is 'y':
        print(tester())
    user = input("Would you like to see if I can solve your Sudoku? y/n ")
    while user not in 'yn':
        user = input("Would you like to see if I can solve your Sudoku? y/n ")
    if user is 'y':
        user = input("Write your Sudoku in one line by row! ")
        sudoku = sudoku_process(str(user))
        sudoku = safesolve(sudoku)
        if sudoku is None:
            user = input("Sorry! I could not solve it. Do you want to see my attempt anyway? y/n ")
            while user not in 'yn':
                user = input("Sorry! I could not solve it. Do you want to see my attempt anyway? y/n ")
            if user is 'y':
                print(Sudoku(sudoku))
            else:
                print("Okay... bye...")
        else:
            print("I have solved the Sudoku puzzle!")
            print('\n')
            print(Sudoku(sudoku))
    else:
        print("Okay...bye...")
