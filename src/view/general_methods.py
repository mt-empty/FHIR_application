
def center_to_win(window, master):
    window.update()
    x = master.winfo_x()
    y = master.winfo_y()
    w = window.winfo_reqwidth()
    h = window.winfo_reqheight()
    total_x = x + (master.winfo_width() // 2) - (w // 2)
    total_y = y + (master.winfo_height() // 2) - (h // 2)
    window.geometry("%dx%d+%d+%d" % (int(w), int(h), int(total_x), int(total_y)))