# flake8:noqa:F401
import tkinter as tk


from .builder import BuilderRoot


class MainApplication(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        self.pack()

        from . import SIRmodel


BuilderRoot["main"] = MainApplication
