# CS134
CS134 Sudoku Solver Project

Student Name: Hyeongjin Kim

Mentor: Dzung Pham

Project Title: Sudoku Solver


1. Describe (briefly) the files and folders found in this project.
   README - this file, an overview of the project
   Contract.pdf - project proposal
   module.py - a script of useful data structures in solving Sudoku
   preprocess.py - a script that reads in text files of Sudoku puzzles
   sudokuClass.py - a script for a class called Sudoku
   solver.py - a script of all functions that implement 
               various solving techniques in attempting 
               to solve Sudoku puzzle(s)
   UI.py - a script that allows for basic testing 
           and user-interface environment if ran
   sudoku.txt - a txt file of 50 unsolved Sudoku puzzles

2. Additional modules (beyond python3, pillow, matplotlib, requests, bs4)
   required by this software: None.

3. Demonstrable accomplishments of this project: 
   My project involved using knowledge from object-oriented programming
   to create my own Sudoku object, which I have done so in sudokuClass.py.
   Within the script, I have created various primitive methods, such as 
   __str__, that have helped me throughout the project.

   I have implemented various Sudoku solving techniques from the obtained
   knowledge of manipulating dictionaries.

   Ultimately, my project's goal was to solve Sudoku puzzles. I have managed
   to implement 4 main solving techniques, which I believe will allow me to
   solve around 80% of Sudoku puzzles from a range of difficulties.

   From a database of 50 unsolved Sudoku puzzles, my solver script has managed
   to solve 48 of them!

4. Documentation of how CS134c staff would use your software to produce the
   results:
   
   Run UI.py and enter 'y' for the first question and the script will
   run through my solving function from solver.py for all 50 unsolved
   sudoku puzzles from sudoku.txt and will print out the number of solved
   sudoku boards (please be patient, for this will take a few minutes).
   The expected result should be 48 Sudoku puzzles solved out of 50!

   You can also run UI.py and enter 'y' when asked for inputting your own
   Sudoku puzzle. Please note that the input must be a single line of all 81
   numbers within the Sudoku board in row order. For example the following
   Sudoku puzzle:
   
    0   0   3  | 0   2   0  | 6   0   0  
    9   0   0  | 3   0   5  | 0   0   1  
    0   0   1  | 8   0   6  | 4   0   0  
   ------------+------------+------------
   
    0   0   8  | 1   0   2  | 9   0   0  
    7   0   0  | 0   0   0  | 0   0   8  
    0   0   6  | 7   0   8  | 2   0   0  
    
   ------------+------------+------------
    0   0   2  | 6   0   9  | 5   0   0  
    8   0   0  | 2   0   3  | 0   0   9  
    0   0   5  | 0   1   0  | 3   0   0  
    
    should be given as:
    003020600900305001001806400008102900700000008...005010300

5. Additional comments:
   Helpful Facts:
   The Sudoku board is given in by the following format:

  A1   A2   A3 |  A4   A5   A6 |  A7   A8   A9 
  B1   B2   B3 |  B4   B5   B6 |  B7   B8   B9 
  C1   C2   C3 |  C4   C5   C6 |  C7   C8   C9 
---------------+---------------+---------------
  D1   D2   D3 |  D4   D5   D6 |  D7   D8   D9 
  E1   E2   E3 |  E4   E5   E6 |  E7   E8   E9 
  F1   F2   F3 |  F4   F5   F6 |  F7   F8   F9 
---------------+---------------+---------------
  G1   G2   G3 |  G4   G5   G6 |  G7   G8   G9 
  H1   H2   H3 |  H4   H5   H6 |  H7   H8   H9 
  I1   I2   I3 |  I4   I5   I6 |  I7   I8   I9 

   - There are nine rows (from A to I), nine columns (from 1 to 9), and nine 3x3 boxes.
   - Each point on the board will be referred as simply point or square.
   - A Sudoku board can only take in values from 1 to 9. However, when reading in unsolved
     Sudoku boards, a 0 on a square will indicate that the value is given as an unknown.
   - The initial non-zero values in a Sudoku puzzle are referred to as "clues".
   - A Sudoku puzzle is said to be solved if numbers from 1 to 9 only appear once in every
     row, column, and box; there cannot be any repetitions. This can be implemented by
     checking if each square has been filled and if the sum of numbers in each row,
     column, and box is 45. 
   - A proper Sudoku puzzle has a unique solution. A proper Sudoku puzzle involves some
     constraints in the minimum number of initial clues and the position of such clues.
   - A region is a general term of a row, column, or box.
   - interacting region: if a group of squares are within the same TWO regions.
     For example, both A1 and A2 are within the same row, that is row A, and the same box.
     Therefore, A1 and A2's interacting regions are their row and box. However, A1 and B2
     are within the same box BUT not in the same row OR column. Interacting region: box.

   Brief Outline of Project:
   In this project, I have implemented dictionaries to represent the Sudoku board with
   points as references (keys) and the possible candidate values (values). A Sudoku puzzle
   is potentially solved if each key refers to only one possible candidate value, for if
   there is only one possible candidate value, then it MUST be that value!

   Therefore, the project prominently involved implementing various Sudoku solving
   techniques to lead to the desired dictionary of one key - one value relationship.

   Explanation of Solving Techniques (from solver.py)

   Single Possibility Rule from eliminate(candidates):
   peers: each square "interacts" with 20 peers from its interacting row, column, and box.
          Every square cannot have the any of the number from the values in its peers, 
          or otherwise the Sudoku constraint of no-repetition will be violated.
   Therefore, given the initial clues, we can look at the peers of each square from
   initial clues (referred to as solvedPoints) and eliminate the initial clue's value
   from the possible candidates of its peers.

   Slicing Dicing / Hidden Singles Method from slicing(candidates):
   Given a box of nine squares, if a candidate value, say x, only appears in ONE of the
   squares within the box, say square A, then that implies that square A is the ONLY
   square within the box that CAN have x. Therefore, it must mean that square A is x.
   This method is useful because square A could have had various other values as its
   possible candidates, but we can logically deduce that it must be only x.

   Subgroup Exclusion from subgroupRowsExclusion(candidates) and 
   subgroupColumnsExclusion(candidates):
   subgroup: a group of three squares within a box that are also in the same row or column.
   For example, a subgroup could contain A1, A2, and A3, for they are in the same box
   and the same row. Therefore, each box has 6 subgroups, with 54 subgroups in total.
   The technique is that given a subgroup, if a candidate value, say x, only appears within
   the subgroup (say within A1 A2 A3 that both A1 and A2 contain x) but not from its
   region, say its row, then x CANNOT be in the squares within the subgroup's OTHER region,
   which would be, in this case, its box. Therefore, once again, say x only appears in A1
   A2 A3 within row A, that is none of A4, A5, A6, A7, A8, A9 has x in their possible
   candidate values. The method concludes that squares from the subgroup's box, that are 
   B1, B2, B3, C1, C2, and C3, CANNOT have x as only of their possible candidate values.
   The same rule applies for box to row, column to box, and box to column. 

   Naked Twins/Triplets/Quartets Elimination from nakedpairs(candidates):
   Given a region (row, column, or box) if a pair of numbers, say x and y, only appear in 
   TWO squares, then no other squares within its region and POTENTIALLY other interacting 
   region cannot have x and y as their possible candidates. This principle can apply for 
   triplet, or even quartet, of numbers given that there are three or four squares, 
   respectively, that have the same combination of numbers.

   For example, let us look at row A. Let us say that only A1 and A2 have a twin of numbers
   of x and y - that is both have only two possible candidates and they are BOTH x and y.
   It may be the case that there are x's and y's in other squares within row A, but the
   naked twins elimination principle logically deduces that none of the squares within
   row A other than A1 and A2 can have neither x nor y. The reasoning can be shown by
   considering two possible outcomes: either A1 is x and A2 is y or A1 is y and A2 is x.
   Therefore, from the no-repetition within same region rule, none of the other squares
   with row A can actually have either x or y as their possible candidates, for in both
   possible outcomes, x and y are used in A1 and A2, regardless of what the permutation is.
   In this case, however, since A1 and A2 are within the same box as well, x and y cannot
   be possible candidate values for squares within that box. Had A1 and A4 were the ones
   that had x and y, with no other squares in row A having the same combination of 
   candidate values, we can still deduce that none of the squares in row A can have x or y
   as their possible candidates, but the elimination with box squares does not apply.
