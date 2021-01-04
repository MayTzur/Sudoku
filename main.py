from tkinter import *
from tkinter import messagebox
from constants import *
from sudokuUI import HomeUI

root = Tk()
root.title('Sudoku Game!')
root.geometry("%dx%d" % (WIDTH, HEIGHT + 150))
root['bg'] = BG_COLOR

def exit_application():
    MsgBox = messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application',
                                        icon='warning')
    if MsgBox == 'yes':
        root.destroy()
    else:
        messagebox.showinfo('Return', 'You will now return to the application screen')

menubar = Menu(root)
root.config(menu=menubar)
fileMenu = Menu(menubar)
fileMenu.add_command(label="Exit", command=exit_application)
menubar.add_cascade(label="File", menu=fileMenu)

HomeUI(root)
root.mainloop()