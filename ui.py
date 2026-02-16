import tkinter as tk
from pathlib import Path
import json

class FRCGUI(tk.Tk):
    #Setting up the GUI, also in this case self=tk.Tk(), so self acts as a window
    def __init__(self):
        super().__init__()
        self.title("FRC Scouting GUI")
        self.minsize(1000, 600)
        self.maxsize(1000, 600)
        self.frame = tk.Frame(self)
        self.label = tk.Label(self, text="hi", background="red")
        self.label1 = tk.Label(self, text="hi", background="blue")
        self.label2 = tk.Label(self, text="hi", background="green")
        self.label3 = tk.Label(self, text="hi", background="yellow")

        #Creating a 3x10 grid system
        for i in range(10):
            self.rowconfigure(i, weight=1)
        for j in range(3):
            self.columnconfigure(j, weight=1)

        self.label.grid(row=5, column=0, columnspan=1, sticky="we")
        self.label1.grid(row=5, column=1, columnspan=1, sticky="we")
        self.label2.grid(row=5, column=2, columnspan=1, sticky="we")
        self.label3.grid(row=5, column=3, columnspan=3, sticky="we")




root = FRCGUI()

root.mainloop()