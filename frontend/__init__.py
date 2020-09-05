# flake8:noqa:F401
import tkinter as tk

from .components.tab import TabSwitcherRoot


from .views.SIR import SIRModelRoot
from .views.SIS import SISModelRoot
from .views.SISPlus import SISModelPlusRoot
from .views.intro import FirstIntroRoot, SIRIntroRoot, SISIntroRoot, SISPlusIntroRoot


class FirstView(tk.Frame):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root)
        self.introduce = FirstIntroRoot(self)
        self.introduce.grid(column=0, row=0, sticky=tk.NW)


class SIRView(tk.Frame):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root)
        self.model = SIRModelRoot(self)
        self.introduce = SIRIntroRoot(self)

        self.model.grid(column=0, row=0)
        self.introduce.grid(column=1, row=0, sticky=tk.NW)


class SISView(tk.Frame):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root)
        self.model = SISModelRoot(self)
        self.introduce = SISIntroRoot(self)

        self.model.grid(column=0, row=0)
        self.introduce.grid(column=1, row=0, sticky=tk.NW)


class SISPlusView(tk.Frame):
    def __init__(self, root: tk.Widget) -> None:
        super().__init__(root)
        self.model = SISModelPlusRoot(self)
        self.introduce = SISPlusIntroRoot(self)

        self.model.grid(column=0, row=0)
        self.introduce.grid(column=1, row=0, sticky=tk.NW)


class MainApplication(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        self.tabView = TabSwitcherRoot(self)
        self.firstView = FirstView(self)
        self.SIRView = SIRView(self)
        self.SISView = SISView(self)
        self.SISPlusView = SISPlusView(self)

        self.tabView.add(self.firstView, "前言")
        self.tabView.add(self.SIRView, "SIR模型")
        self.tabView.add(self.SISView, "SIS模型")
        self.tabView.add(self.SISPlusView, "增强SIS模型")

        self.tabView.pack()