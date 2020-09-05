import tkinter as tk
import tkinter.ttk as ttk


class TabSwitcherRoot(tk.Frame):
    def __init__(self, root: tk.Widget):
        super().__init__(root)
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(column=0, row=0)

    def add(self, component: tk.Widget, name: str):
        self.notebook.add(component, text=name)
