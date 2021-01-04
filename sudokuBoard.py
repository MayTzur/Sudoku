class SudokuError(Exception):
    """An application specific error."""
    pass

class SudokuBoard:
    """Sudoku Board representation."""
    def __init__(self, board):
        self.board = self.__create_board(board)

    def __create_board(self, board):
        """Created a list of lists (a matrix) to represent the Sudoku board to solve.
        Return the constructed board.
        """
        try:
            if len(board) != 9:
                raise SudokuError('Each sudoku puzzle must be 9 lines long.\nPlease try to select a level again...')
            else:
                for row in board:
                    if len(row) != 9:
                        raise SudokuError('Each line in the sudoku puzzle must be 9 chars long.\nPlease try to select a level again...')
                return board
        except SudokuError as e:
            print(e)
            
