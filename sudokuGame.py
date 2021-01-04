from sudokuBoard import SudokuBoard
from tkinter import *

class SudokuGame:
    """A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    """
    def __init__(self, board):
        self.start_puzzle = SudokuBoard(board).board
        self.mistakesNum = IntVar()
        self.mistakesNum = 0

    def reset_mistakesNum(self):
        self.mistakesNum = 0

    def start(self):
        """Run whenever the user starts a game.

        self.game_over: set to False, when the user fills the entire board we will set it to True.
        self.puzzel: create a copy of the puzzle.
        self.mistakesNum: set the number of mistakes to zero.
        """
        self.game_over = False
        self.puzzel = []

        for i in range(9):
            self.puzzel.append([])
            for j in range(9):
                self.puzzel[i].append(self.start_puzzle[i][j])

    def change_mistakesNum(self):
        """Increases the number of user errors in one"""
        self.mistakesNum += 1

    def getGagNum(self, num):
        """Auxiliary function for checking the block"""
        if num <= 2:
            return {'min': 0, 'max': 2}
        elif num <= 5:
            return {'min': 3, 'max': 5}
        else:
            return {'min': 6, 'max': 8}

    def checkBlock(self, row, col, num):
        """If the value entered already exists in the block return true, otherwise false"""
        gag_r = self.getGagNum(row)
        gag_c = self.getGagNum(col)

        return num in [self.puzzel[r][c] for r in range(gag_r['min'], gag_r['max'] + 1) for c in range(gag_c['min'], gag_c['max'] + 1)]

    def checkRow(self, row, num):
        """If the value entered already exists in the row return true, otherwise false"""
        return num in [self.puzzel[row][c] for c in range(9)]

    def checkCol(self, col, num):
        """If the value entered already exists in the column return true, otherwise false"""
        return num in [self.puzzel[r][col] for r in range(9)]

    def checkNewContent(self, row, col, num):
        """If the new value does not appear in the column / row / block return true, otherwise false"""
        if self.checkRow(row, num):
            return False
        elif self.checkCol(col, num):
            return False
        elif self.checkBlock(row, col, num):
            return False
        return True

    def check_solution(self):
        return self.check_all_rows() and self.check_all_columns()

    def check_all_rows(self):
        for row in range(9):
            temp = []
            for col in range(9):
                if self.puzzel[row][col] in temp:
                    return False
                temp.append(self.puzzel[row][col])
        return True

    def check_all_columns(self):
        for col in range(9):
            temp = []
            for row in range(9):
                if self.puzzel[row][col] in temp:
                    return False
                temp.append(self.puzzel[row][col])
        return True

    def check_if_over(self):
        """Check that the entire board (all rows, columns, and each 3x3 square) is full

        If the entire board is successfully full OR if mistakes number is 3 -
            set self.game_over to True AND return True
        otherwise - set self.game_over to False AND return False
        """
        if self.mistakesNum == 3:
            self.game_over = True
            return True

        for row in range(9):
            if not self.check_row(row):
                return False
        for col in range(9):
            if not self.check_column(col):
                return False
        for row in range(3):
            for col in range(3):
                if not self.check_square(row, col):
                    return False
        self.game_over = True
        return True

    def check_block(self, block):
        """If the block is equal to numbers 1 through 9 return True, otherwise False"""
        return set(block) == set(range(1,10))

    def check_row(self, row):
        """Iterates over each row of the puzzle with the user inputs"""
        return self.check_block(self.puzzel[row])

    def check_column(self, column):
        """Iterates over each column of the puzzle with the user inputs"""
        return self.check_block([self.puzzel[row][column] for row in range(9)])

    def check_square(self, row, column):
        """Iterates over each 3x3 square of the puzzle with the user inputs"""
        return self.check_block([self.puzzel[r][c]
        for r in range(row * 3, (row + 1) * 3)
        for c in range(column * 3, (column + 1) * 3)])
    
