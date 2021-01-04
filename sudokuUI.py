from tkinter import *
from constants import *
from constants import _x, _y
import requests
from sudokuGame import SudokuGame

class DifficaltyUI(Frame):
    def __init__(self, root):
        self.parent = root
        Frame.__init__(self, root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.var = IntVar()

    def deleteFrame(self):
        self.destroy()

    def initDiffUI(self):
        self.pack()

        Label(self, text="Choose your game difficulty:", pady=18, font=MSG_FONT,
              bg=BG_COLOR).pack(
            side=TOP)
        Radiobutton(self, text="easy", font=MSG_FONT, variable=self.var, value=1, bg=BG_COLOR,
                    command=self.difficulty_selection).pack(anchor=W)
        Radiobutton(self, text="medium", font=MSG_FONT, variable=self.var, value=2, bg=BG_COLOR,
                    command=self.difficulty_selection).pack(anchor=W)
        Radiobutton(self, text="hard", font=MSG_FONT, variable=self.var, value=3, bg=BG_COLOR,
                    command=self.difficulty_selection).pack(anchor=W)
        Radiobutton(self, text="random", font=MSG_FONT, variable=self.var, value=4, bg=BG_COLOR,
                    command=self.difficulty_selection).pack(anchor=W)

    def difficulty_selection(self):
        if self.var.get() == 1:
            x = requests.get(URL + 'easy')
        elif self.var.get() == 2:
            x = requests.get(URL + 'medium')
        elif self.var.get() == 3:
            x = requests.get(URL + 'hard')
        elif self.var.get() == 4:
            x = requests.get(URL + 'random')
        x = x.json()
        game = SudokuGame(x["board"])
        game.start()
        self.deleteFrame()
        BoardUI(self.parent, game)

class HomeUI(Frame):
    def __init__(self, root):
        self.parent = root
        Frame.__init__(self, root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.var = IntVar()
        self.initHomeUI()

    def deleteFrame(self):
        self.destroy()

    def create_difficulty_frame(self):
        diff = DifficaltyUI(self.parent)
        self.deleteFrame()
        diff.initDiffUI()

    def initHomeUI(self):
        self.pack()

        canvas = Canvas(self, bg=BG_COLOR, width=WIDTH, height=HEIGHT, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(27, 150, 463, 340, tags='victory', fill='dark orange', outline='orange')
        canvas.create_text(_x, _y, text='Welcome To Sudoku Game!', tags='winner', fill='white', font=TITLE_FONT)
        play_btn = Button(self, text="let's play!", fg='dark orange', bg=BG_COLOR, width=20, font=MSG_FONT,
                          command=self.create_difficulty_frame)
        canvas.create_window(_x, _y + 150, window=play_btn)

class BoardUI(Frame):
    """The Tkinter UI, responsible for drawing the board and accepting user input."""
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        Frame.__init__(self, parent, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.row, self.col = 0, 0

        self.mistakeRow, self.mistakeCol = -1, -1
        #self.isCorrect = True
        self.initBoardUI()

    def initBoardUI(self):
        """Sets up the actual user interface."""
        self.pack()

        self.lbl_mistake = Label(self, text=f'Several mistakes: {self.game.mistakesNum} / 3', pady=15, padx=15, bg=BG_COLOR, font=MSG_FONT)
        self.lbl_mistake.pack(side=TOP)

        self.canvas = Canvas(self,width=WIDTH,bg=BG_COLOR,height=HEIGHT, highlightthickness=0)
        self.canvas.pack(fill=BOTH, side=TOP)
        ans_btn = Button(self,text="Clear answers", fg=BORDER_COLOR, width=45, bg=BG_COLOR, font=MSG_FONT, command=self.clear_answers).pack()
        cell_btn = Button(self,text="Clear cell", fg=BORDER_COLOR, width=45, bg=BG_COLOR, font=MSG_FONT, command=self.clear_cell).pack()
        start_btn = Button(self, text="Start new game", fg=BORDER_COLOR, width=45, bg=BG_COLOR, font=MSG_FONT,
                          command=self.choose_difficalty).pack()

        self.canvas.create_window(_x, _y, tags='ans_btn', window=ans_btn)
        self.canvas.create_window(_x+100, _y, tags='cell_btn', window=cell_btn)
        self.canvas.create_window(_x + 200, _y, tags='start_btn', window=start_btn)
        self.draw_grid()
        self.draw_puzzle()

        self.canvas.bind("<Button-1>", self.cell_clicked)
        self.canvas.bind("<Key>", self.key_pressed)

    def deleteFrame(self):
        self.destroy()

    def draw_grid(self):
        """Draws grid divided with blue lines into 3x3 squares."""
        for i in range(10):
            color = 'dark violet' if i % 3 == 0 else 'gray'
            pix = 3 if i % 3 == 0 else 1

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=pix)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = HEIGHT - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color, width=pix)

    def draw_puzzle(self):
        """Helpful when the user wants to clear out the puzzle and start over.

        first - call delete on the canvas to clear out any previous numbers.
        then - iterate over rows and columns, and create a cell.
        then - grab the same X & Y location of the cell from the game’s puzzle.
        If it isn’t zero, then fill it in with the appropriate number, otherwise just leave it blank.
        """
        self.canvas.delete('numbers')
        for i in range(9):
            for j in range(9):
                answer = self.game.puzzel[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2

                    original = self.game.start_puzzle[i][j]
                    if (self.mistakeRow != -1 and self.mistakeRow == i) and (self.mistakeCol != -1 and self.mistakeCol == j):
                        color = 'red3'
                    else:
                        color = 'black' if answer == original else 'sea green'
                    self.canvas.create_text(x, y, text=answer, tags='numbers', fill=color, font=BOARD_FONT)

    def clear_answers(self):
        """Delete all answers from board"""
        self.game.start()
        self.canvas.delete('victory')
        self.canvas.delete('winner')
        if self.game.mistakesNum == 3:
            self.game.reset_mistakesNum()
        self.lbl_mistake.config(text=f'Several mistakes: {self.game.mistakesNum} / 3')
        self.draw_puzzle()
        self.mistakeRow, self.mistakeCol = -1, -1

    def clear_cell(self):
        """Delete the answer from specific cell"""
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0:
            self.game.puzzel[self.row][self.col] = 0
            self.row, self.col = -1, -1
            if self.mistakeRow > -1 and self.mistakeCol > -1:
                self.mistakeRow, self.mistakeCol = -1, -1
            self.draw_puzzle()
            self.draw_cursor()

    def cell_clicked(self, event):
        """Grab the cell that corresponds with the puzzle"""
        if self.game.game_over:
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()
            row, col = int((y - MARGIN)/SIDE), int((x - MARGIN)/SIDE)
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            else:
                self.row, self.col = row, col
        self.draw_cursor()

    def draw_cursor(self):
        """ Highlights the particular cell that the user has clicked on.
            First delete the "cursor" element, just to clear out the previously highlighted cell.
            Then:
                if self.row and self.col are set - compute the dimensions of the cell,
                                                    create a rectangle attached to our canvas with those dimensions,
                                                    and highlight the outline red.
        """
        self.canvas.delete('cursor')
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1

            self.canvas.create_rectangle(x0, y0, x1, y1, outline='red', tags='cursor')

    def key_pressed(self, event):
        """Set the number of the cell in Sudoku puzzle.

        :param event: bind the "<Key>" event
        :return:
            if self.game.game_over is True -  returning out of the function.
            otherwise, if the cell is selected and the key character is a valid Sudoku number - reset the row & column
                selection that was set and redraw the puzzle with the new numbers, and redraw the cursor.
        """
        if self.game.game_over:
            return
        if self.row >= 0 and self.col >= 0 and event.char in '1234567890':
            if not self.game.checkNewContent(self.row, self.col, int(event.char)):
                self.mistakeRow, self.mistakeCol = self.row, self.col
                self.game.change_mistakesNum()
                self.lbl_mistake.config(text=f'Several mistakes: {self.game.mistakesNum} / 3')

            self.game.puzzel[self.row][self.col] = int(event.char)
            self.row, self.col = -1, -1
            self.draw_puzzle()
            self.draw_cursor()

            #self.res = self.game.check_if_over()
            if self.game.check_if_over():
                self.draw_result()

    def draw_result(self):
        """When the user has successfully completed the puzzle OR he has 3 failed attempts"""
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        res = self.game.check_solution()
        outline = 'orange' if res else 'red3'
        msg = 'You Win!!!' if res else 'GAME OVER!'

        if not res:
            again_btn = Button(self, text="TRY AGAIN", activeforeground='yellow', fg='white', bg=outline, padx=6, font=MSG_FONT,
                   borderwidth=0, command=self.clear_answers)
            self.canvas.create_window(x+60, y+65, tags='winner', window=again_btn)

        new_btn = Button(self, text="NEW GAME", activeforeground='blue', fg='white', bg=outline, font=MSG_FONT,
                         borderwidth=0, command=self.choose_difficalty)
        x_ = x - 60 if not res else x
        self.canvas.create_window(x_, y + 65, tags='winner', window=new_btn)

        self.canvas.create_oval(x0 - 50, y0 - 50, x1 + 50, y1 + 50, tags='victory', fill=outline, outline=outline)
        self.canvas.create_text(x, y-30, text=msg, tags='winner', fill='white', font=('Verdana', 32))
        self.canvas.create_text(x, y + 10, text='What do you wanna do now?', tags='winner', fill='white', font=MSG_FONT)


    def choose_difficalty(self):
        diff = DifficaltyUI(self.parent)
        self.deleteFrame()
        diff.initDiffUI()
        
