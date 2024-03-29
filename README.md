# Nonogram solver
## Project description
Terminal-based automatic nonogram solver. Takes numbers (hints) from nonogram board as input and applies logic to solve puzzle.

A nonogram is a puzzle in which there is a hidden image in a rectangular grid that is revealed when the puzzle is completed. Each row and column is neighbored by a series of numbers indicating lengths of the continuous sequences of colored/painted squares that must appear in that line. Each sequence must be satisfied and separated by at least one unmarked square.

## How to run
`python nonogram_solver.py`

The program will ask the following two queries:
```
Enter row values, rows separated by commas
Enter col values, cols separated by commas
```
For the first query, input all numbers appearing to the left of the board. Separate numbers on the same row by a space, and mark a new row of numbers with a comma. <br />
For the second query, input all numbers appearing on the top of the board. Separate numbers in the same column by a space, and mark a new column of numbers with a comma.

## Examples
```
python nonogram_solver.py
Enter row values, rows separated by commas:
6 3,5 2,4 2 2,3 2 1,3 3 1,2 4 1,2 6,1 4 1 1,1 4 1 1,3 4 1,2 1 1 1 1,3 2,2 4,1 5,1 7,1 10
Enter col values, cols separated by commas:
9 1,7 1 2,5 5 1,3 3 2 1,2 7 1,1 5 2,4 2 2,2 3 2 3,4 2 2 4,1 4 1 4,1 1 5,2 9

              9 7 5 3 2 1 4 2 4 1 1 2
              1 1 5 3 7 5 2 3 2 4 1 9
                2 1 2 1 2 2 2 2 1 5
                    1       3 4 4
              ________________________

6 3        |  # # # # # # . . # # # .
5 2        |  # # # # # . . # # . . .
4 2 2      |  # # # # . . . # # . # #
3 2 1      |  # # # . . . . . # # . #
3 3 1      |  # # # . . # # # . # . .
2 4 1      |  # # . . # # # # . # . .
2 6        |  # # . . # # # # # # . .
1 4 1 1    |  # . . # # # # . # . . #
1 4 1 1    |  # . # # # # . # . . . #
3 4 1      |  . . # # # . # # # # . #
2 1 1 1 1  |  . # # . # . # . # . . #
3 2        |  . . # # # . . . . . # #
2 4        |  . . # # . . . . # # # #
1 5        |  . # . . . . . # # # # #
1 7        |  . # . . . # # # # # # #
1 10       |  # . # # # # # # # # # #


Enter row values, rows separated by commas:
1 1,3 3,1 8 1,12,4 5,4 4,2 1 3,3 1 1 3,4 4,3 2 4,2 3,1 2 2 1,4
Enter col values, cols separated by commas:
4 5,1 9,5 3,5 1 1,4 1 2,2 1 1,3 1 1,4 1 2,5 2 1,10,2 9,3 4

            4 1 5 5 4 2 3 4 5 102 3
            5 9 3 1 1 1 1 1 2   9 4
                  1 2 1 1 2 1
            ________________________

1 1      |  # . . . . . . . . . # .
3 3      |  # # # . . . . . . # # #
1 8 1    |  # . # # # # # # # # . #
12       |  # # # # # # # # # # # #
4 5      |  . # # # # . # # # # # .
4 4      |  . # # # # . . # # # # .
2 1 3    |  # # . # . . . . # # # .
3 1 1 3  |  # # # . # . . # . # # #
4 4      |  # # # # . . . . # # # #
3 2 4    |  # # # . . # # . # # # #
2 3      |  # # . . . . . . . # # #
1 2 2 1  |  . # . # # . . # # . # .
4        |  . . . . # # # # . . . .


Enter row values, rows separated by commas:
5,9,10,14 3,22,3 19,24,26,26,27,4 21,3 21,4 22,3 20 1,3 20 1,3 19 1,2 19 1,2 18 1,2 3 3 8 1,2 3 3 3 3 1,2 2 3 3 3,2 2 3 2 3,1 2 3 2 3,2 1 2 3 2 3,4 2 3 2 2,2 2 2 2,3 3 3 3
Enter col values, cols separated by commas:
10,18,12 2,11 1,10 1,4 4 1,9,17,20 1,27,27,18,24 1,24,24,15,15,14,15,18 1,24,24,15,20 1,22,21,8,4,8

                10181211104 9 172027271824242415151415182424152022218 4 8
                    2 1 1 4     1       1             1       1
                          1
                __________________________________________________________

5            |  . . . . . . . # # # # # . . . . . . . . . . . . . . . . .
9            |  . . . . # # # # # # # # # . . . . . . . . . . . . . . . .
10           |  . . . # # # # # # # # # # . . . . . . . . . . . . . . . .
143          |  . . . # # # # # # # # # # # # # # . . # # # . . . . . . .
22           |  . . # # # # # # # # # # # # # # # # # # # # # # . . . . .
3 19         |  . . # # # . # # # # # # # # # # # # # # # # # # # . . . .
24           |  . . # # # # # # # # # # # # # # # # # # # # # # # # . . .
26           |  . # # # # # # # # # # # # # # # # # # # # # # # # # # . .
26           |  . # # # # # # # # # # # # # # # # # # # # # # # # # # . .
27           |  . # # # # # # # # # # # # # # # # # # # # # # # # # # # .
4 21         |  . # # # # . . # # # # # # # # # # # # # # # # # # # # # .
3 21         |  . # # # . . . # # # # # # # # # # # # # # # # # # # # # .
4 22         |  # # # # . . . # # # # # # # # # # # # # # # # # # # # # #
3 201        |  # # # . . . . # # # # # # # # # # # # # # # # # # # # . #
3 201        |  # # # . . . . # # # # # # # # # # # # # # # # # # # # . #
3 191        |  # # # . . . . # # # # # # # # # # # # # # # # # # # . . #
2 191        |  # # . . . . . # # # # # # # # # # # # # # # # # # # . . #
2 181        |  # # . . . . . . # # # # # # # # # # # # # # # # # # . . #
2 3 3 8 1    |  # # . . . . . . # # # . # # # . . . # # # # # # # # . . #
2 3 3 3 3 1  |  # # . . . . . . # # # . # # # . . . . # # # . # # # . . #
2 2 3 3 3    |  # # . . . . . . . # # . # # # . . . . # # # . # # # . . .
2 2 3 2 3    |  # # . . . . . . . # # . # # # . . . . . # # . # # # . . .
1 2 3 2 3    |  . # . . . . . . . # # . # # # . . . . . # # . # # # . . .
2 1 2 3 2 3  |  . # # . . # . . . # # . # # # . . . . . # # . # # # . . .
4 2 3 2 2    |  . # # # # . . . . # # . # # # . . . . . # # . . # # . . .
2 2 2 2      |  . . . . . . . . . # # . . # # . . . . . # # . . # # . . .
3 3 3 3      |  . . . . . . . . # # # . # # # . . . . # # # . # # # . . .
```
