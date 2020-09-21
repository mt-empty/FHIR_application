import tkinter as tk


class ScrolledFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super(ScrolledFrame, self).__init__(master, *args, **kwargs)
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas = canvas = tk.Canvas(self, bd=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        def _config_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _config_interior)

        def _config_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _config_canvas)

        self.canvas.bind_all('<MouseWheel>', self.__mouse_scroll)
        self.bind_all('<MouseWheel>', self.__mouse_scroll)
        self.bind("<Configure>", self.__on_frame_configure)

    def __mouse_scroll(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 100)), "units")
        else:
            if event.num == 5:
                move = 1
            else:
                move = -1
            self.canvas.yview_scroll(move, "units")

    def __on_frame_configure(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox(tk.ALL))
