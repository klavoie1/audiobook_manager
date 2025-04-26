# Acts as the Main window settings

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox


class MainWindow(tk.Tk):
    def __init__(self):

        #main setup for GUI window
        super().__init__()
        self.title('Audiobook Player')
        self.geometry('800x600')

        # Calling the widget class for the UI elements
        self.menu = Menu(self)

        # Running command to for the main window
        self.mainloop()


class Menu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, text='Choose a file')
        self.label.pack(side='left')
