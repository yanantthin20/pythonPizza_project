from tkinter import *
import forms

class Root(Tk):
    def __init__(self):
        super().__init__()
        forms.Home_frame(self).pack(fill = 'both', expand = True)

Root().mainloop()
