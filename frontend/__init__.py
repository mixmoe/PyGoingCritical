# flake8:noqa:F401
import tkinter as tk

from .components.tab import TabSwitcherRoot


from .views.SIR import SIRModelRoot
from .views.SIS import SISModelRoot
from .views.SISPlus import SISModelPlusRoot


class MainApplication(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        self.tabView = TabSwitcherRoot(self)
        self.SISModel = SISModelRoot(self)
        self.SIRModel = SIRModelRoot(self)
        self.SISModelPlus = SISModelPlusRoot(self)

        self.tabView.add(self.SISModel, "SIS")
        self.tabView.add(self.SIRModel, "SIR")
        self.tabView.add(self.SISModelPlus, "SISPlus")

        self.tabView.pack()
