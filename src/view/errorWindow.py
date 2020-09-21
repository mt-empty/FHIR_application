import tkinter as tk
from view.general_methods import center_to_win


class ErrorWindow(tk.Toplevel):

    def __init__(self, master, *args, **kwargs):
        super(ErrorWindow, self).__init__(master, *args, **kwargs)
        self.configure(width=250, height=100)
        self.resizable(False, False)
        error_msg = tk.Label(self, text="Error, please check that the values entered are ints/floats")
        error_msg.pack(fill=tk.BOTH)
        center_to_win(self, self.master)